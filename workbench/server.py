#!/usr/bin/env python3
"""Scrum Master Skill Workbench: use the skill library from a web page on your own computer.

    python3 workbench/server.py            # opens http://127.0.0.1:8765
    python3 workbench/server.py --port 9000 --no-browser

Pick a skill, then chat with Claude using that skill's instructions. You can also
read each skill in full, or copy it to paste into another chat tool.

Needs Python 3.9+ and, for chatting, the Anthropic SDK (`pip install anthropic`)
plus an API key (set ANTHROPIC_API_KEY, or paste a key into the page). Without a
key you can still browse and copy every skill.

The server listens on 127.0.0.1 only, so nothing is reachable from other machines.
"""
import argparse
import json
import os
import shutil
import sys
import threading
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parent
CACHE = HERE / ".cache"
KEY_FILE = HERE / ".api_key"
sys.path.insert(0, str(KIT / "tools"))
import export_skill  # noqa: E402
import install_library  # noqa: E402

try:
    import anthropic
except ImportError:  # browsing still works without the SDK
    anthropic = None

MODELS = [
    {"id": "claude-opus-5-5", "label": "Claude Opus 5.5 (default)"},
    {"id": "claude-sonnet-5-5", "label": "Claude Sonnet 5.5 (faster, cheaper)"},
    {"id": "claude-haiku-5-5", "label": "Claude Haiku 5.5 (fastest, cheapest)"},
]
MODEL_IDS = {m["id"] for m in MODELS}
EFFORTS = ["low", "medium", "high", "xhigh", "max"]
# Server-side refusal fallback: if the model declines a request, the API retries on another model.
FALLBACK_MODELS = {"claude-opus-5-5", "claude-sonnet-5-5"}

LIB = json.loads((KIT / "library.json").read_text(encoding="utf-8"))
SKILLS = {s["install_name"]: s for s in LIB["skills"]}

_skill_lock = threading.Lock()
_skill_text = {}          # name -> dict(meta, body, plain, system)
_convs = {}               # conv_id -> {"skill": name, "messages": [...]}
_conv_lock = threading.Lock()
_api_key = None

_orig_fetch_remote = install_library.fetch_remote


def _fetch_remote_with_fallback(repo, ref, base, dest, skip):
    """Download the whole skill folder; if GitHub's API is unavailable (rate limit, firewall),
    fall back to just SKILL.md, which comes from raw.githubusercontent.com without the API."""
    try:
        _orig_fetch_remote(repo, ref, base, dest, skip)
    except Exception:
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "SKILL.md").write_bytes(install_library.raw(repo, ref, base.rstrip("/") + "/SKILL.md"))


install_library.fetch_remote = _fetch_remote_with_fallback


# ---------- skills ----------

def load_skill(name):
    """Stage a skill (local copy, or download at the pinned commit) and build its texts."""
    with _skill_lock:
        if name in _skill_text:
            return _skill_text[name]
        skill = SKILLS[name]
        staged = CACHE / name
        if not (staged / "SKILL.md").is_file():
            CACHE.mkdir(exist_ok=True)
            tmp = CACHE / f".stage-{uuid.uuid4().hex}"
            try:
                install_library.stage(skill, tmp)
                if staged.exists():
                    shutil.rmtree(staged)
                (tmp / name).rename(staged)
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
        meta, body = export_skill.parse_skill(staged)
        full = export_skill.build_body(body, export_skill.collect_refs(staged), True)
        has_scripts = (staged / "scripts").is_dir()
        note = ("\n> This skill also ships Python scripts. They don't run in the workbench; "
                "install the skill into Claude Code to use them.\n" if has_scripts else "")
        plain = (f"Use these instructions for this whole conversation.\n"
                 f"Apply them when: {meta['description']}\n{note}\n{full}")
        system = (
            "You are helping a Scrum Master. Follow the skill below for this whole conversation. "
            "It was written for an assistant that can read files and run scripts; you can't do either "
            "here, so if a step needs a script or file, ask the user for the data or do the reasoning "
            "yourself. Answer in Markdown.\n\n"
            f"<skill name=\"{name}\">\n{full}\n</skill>"
        )
        out = {"meta": meta, "markdown": full, "plain": plain, "system": system,
               "has_scripts": has_scripts}
        _skill_text[name] = out
        return out


# ---------- API key ----------

def current_key():
    if _api_key:
        return _api_key
    if os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"):
        return None  # SDK reads it from the environment
    if KEY_FILE.is_file():
        return KEY_FILE.read_text().strip() or None
    return None


def key_status():
    if anthropic is None:
        return "no-sdk"
    if _api_key or KEY_FILE.is_file():
        return "saved"
    if os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"):
        return "env"
    return "missing"


def make_client():
    key = current_key()
    return anthropic.Anthropic(api_key=key) if key else anthropic.Anthropic()


def echo_content(content):
    """Turn a response's content into what we send back next turn.

    Blocks go back unchanged (thinking included) so the conversation history stays intact.
    After a mid-answer fallback, model-internal blocks before the last fallback marker are dropped,
    as the API requires.
    """
    blocks = [b.model_dump(exclude_none=True) for b in content]
    last_fb = max((i for i, b in enumerate(blocks) if b.get("type") == "fallback"), default=-1)
    if last_fb < 0:
        return blocks
    drop = {"thinking", "redacted_thinking", "tool_use"}
    return [b for i, b in enumerate(blocks) if i >= last_fb or b.get("type") not in drop]


# ---------- HTTP ----------

class Handler(BaseHTTPRequestHandler):
    server_version = "SkillWorkbench/1.0"

    def log_message(self, fmt, *args):
        if "/api/" in (args[0] if args else ""):
            sys.stderr.write("  %s\n" % (fmt % args))

    # helpers
    def send_json(self, obj, status=200):
        data = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def read_json(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def same_origin(self):
        # Block other web pages from driving this local server.
        origin = self.headers.get("Origin")
        host = self.headers.get("Host", "")
        return origin is None or origin in (f"http://{host}",)

    # routes
    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            data = (HERE / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)
        elif path in ("/vendor/marked.min.js", "/vendor/purify.min.js"):
            data = (HERE / path.lstrip("/")).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/javascript; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "max-age=86400")
            self.end_headers()
            self.wfile.write(data)
        elif path == "/api/library":
            skills = []
            for s in LIB["skills"]:
                src = s["source"]
                skills.append({
                    "name": s["install_name"], "category": s["category"], "job": s["job"],
                    "level": s["level"], "needs": s["needs"], "license": s["license"],
                    "optional": bool(s.get("optional")), "try_prompt": s.get("try_prompt", ""),
                    "local": "local" in src,
                    "author": s.get("author") or src.get("repo") or "",
                    "source_url": (f"https://github.com/{src['repo']}/tree/{src['ref']}/{src['path']}"
                                   if "repo" in src else ""),
                })
            self.send_json({"skills": skills, "models": MODELS, "efforts": EFFORTS,
                            "key": key_status()})
        elif path.startswith("/api/skill/"):
            name = path.rsplit("/", 1)[1]
            if name not in SKILLS:
                return self.send_json({"error": "unknown skill"}, 404)
            try:
                s = load_skill(name)
            except Exception as e:
                return self.send_json({"error": f"Couldn't load this skill: {e}. "
                                       "Skills from other authors download from GitHub, so check "
                                       "your internet connection."}, 502)
            self.send_json({"markdown": s["markdown"], "plain": s["plain"],
                            "description": s["meta"]["description"],
                            "has_scripts": s["has_scripts"]})
        else:
            self.send_json({"error": "not found"}, 404)

    def do_POST(self):
        if not self.same_origin():
            return self.send_json({"error": "forbidden"}, 403)
        path = self.path.split("?")[0]
        if path == "/api/key":
            global _api_key
            body = self.read_json()
            key = (body.get("key") or "").strip()
            if body.get("forget"):
                _api_key = None
                KEY_FILE.unlink(missing_ok=True)
                return self.send_json({"key": key_status()})
            if not key:
                return self.send_json({"error": "empty key"}, 400)
            _api_key = key
            if body.get("remember"):
                KEY_FILE.write_text(key)
                os.chmod(KEY_FILE, 0o600)
            return self.send_json({"key": key_status()})
        if path == "/api/reset":
            with _conv_lock:
                _convs.pop(self.read_json().get("conv_id"), None)
            return self.send_json({"ok": True})
        if path == "/api/chat":
            return self.chat(self.read_json())
        self.send_json({"error": "not found"}, 404)

    def chat(self, body):
        if anthropic is None:
            return self.send_json({"error": "The Anthropic SDK isn't installed. Run: pip install anthropic"}, 500)
        name, text = body.get("skill"), (body.get("message") or "").strip()
        model = body.get("model") if body.get("model") in MODEL_IDS else MODELS[0]["id"]
        effort = body.get("effort") if body.get("effort") in EFFORTS else "medium"
        conv_id = body.get("conv_id") or uuid.uuid4().hex
        if name not in SKILLS or not text:
            return self.send_json({"error": "pick a skill and type a message"}, 400)
        try:
            skill = load_skill(name)
        except Exception as e:
            return self.send_json({"error": f"Couldn't load this skill: {e}"}, 502)

        with _conv_lock:
            conv = _convs.get(conv_id)
            if conv is None or conv["skill"] != name:
                conv = {"skill": name, "messages": []}
                _convs[conv_id] = conv
            history = list(conv["messages"])
        history.append({"role": "user", "content": text})

        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        def emit(obj):
            self.wfile.write((json.dumps(obj) + "\n").encode())
            self.wfile.flush()

        kwargs = dict(
            model=model,
            max_tokens=64000,
            system=[{"type": "text", "text": skill["system"], "cache_control": {"type": "ephemeral"}}],
            messages=history,
            output_config={"effort": effort},
        )
        if model in FALLBACK_MODELS:
            kwargs["betas"] = ["server-side-fallback-2026-07-01"]
            kwargs["extra_body"] = {"fallbacks": "default"}

        try:
            client = make_client()
            emit({"t": "start", "conv_id": conv_id})
            api = client.beta.messages if "betas" in kwargs else client.messages
            with api.stream(**kwargs) as stream:
                for chunk in stream.text_stream:
                    emit({"t": "text", "v": chunk})
                final = stream.get_final_message()
        except BrokenPipeError:
            return
        except anthropic.AuthenticationError:
            return emit({"t": "error", "v": "Your API key was rejected. Check it and paste it again."})
        except anthropic.PermissionDeniedError:
            return emit({"t": "error", "v": "This API key isn't allowed to use that model."})
        except anthropic.NotFoundError:
            return emit({"t": "error", "v": f"Model {model} wasn't found for this key. Try another model."})
        except anthropic.RateLimitError:
            return emit({"t": "error", "v": "Rate limited. Wait a minute and try again."})
        except anthropic.BadRequestError as e:
            return emit({"t": "error", "v": f"The API rejected the request: {e.message}"})
        except anthropic.APIStatusError as e:
            return emit({"t": "error", "v": f"API error {e.status_code}: {e.message}"})
        except anthropic.APIConnectionError:
            return emit({"t": "error", "v": "Couldn't reach the Anthropic API. Check your internet connection."})
        except Exception as e:
            msg = str(e).lower()
            if any(w in msg for w in ("authentication", "credential", "api_key")):
                return emit({"t": "error", "v": "No API key found. Paste one at the top of the page."})
            if isinstance(e, TypeError):  # SDK too old for a parameter
                return emit({"t": "error", "v": f"Your Anthropic SDK may be out of date ({e}). "
                                                "Run: pip install -U anthropic"})
            return emit({"t": "error", "v": f"Something went wrong: {e}"})

        if final.stop_reason == "refusal":
            emit({"t": "notice", "v": "Claude declined to answer this one. Try rephrasing."})
        elif final.stop_reason == "max_tokens":
            emit({"t": "notice", "v": "The answer hit the length limit and was cut off."})
        if final.stop_reason != "refusal":
            history.append({"role": "assistant", "content": echo_content(final.content)})
            with _conv_lock:
                conv["messages"] = history
        u = final.usage
        emit({"t": "done", "model": final.model, "stop": final.stop_reason,
              "usage": {"in": u.input_tokens, "out": u.output_tokens,
                        "cache_read": getattr(u, "cache_read_input_tokens", 0) or 0}})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    url = f"http://127.0.0.1:{a.port}"
    print(f"Scrum Master Skill Workbench running at {url}")
    if anthropic is None:
        print("Note: the Anthropic SDK isn't installed, so chat is off. To turn it on: pip install anthropic")
    print("Press Ctrl+C to stop.")
    if not a.no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
