---
name: "backlog-refinement-readiness"
description: "Check Jira user stories (keys or a JQL filter) against the team's Definition of Ready, score each Ready, Almost Ready or Not Ready, and draft fixes and PO questions."
---

# Backlog Refinement Readiness

Check each user story against the Definition of Ready (DoR), score it, and return a short table the user can share with the Product Owner, followed by draft fixes for the gaps.

## 1. Get the stories from Jira

The user usually gives you Jira issue keys (e.g. HRT-101, HRT-102) or a JQL filter (e.g. `project = HRT AND sprint in futureSprints() AND status = "Ready for Refinement"`).

- Use the Jira connector. Get the cloudId once, then fetch the issues with `searchJiraIssuesUsingJql`, or `getJiraIssue` for single keys.
- Ask for the full fields (`view: evidence` or `full`) so you get the description, acceptance criteria, **story points** (a custom field), issue links and comments.
- Read the issue links (blocks / is blocked by / depends on) and the recent comments as well: dependencies and open decisions often only show up there.
- If the Jira connector isn't connected, say so in one line and ask the user to paste the stories instead. Pasted text is fine as a fallback.
- Judge only what is in the issue. Don't assume something is done because it is likely.

## 2. Definition of Ready (6 checks)

Each check is **Pass**, **Vague** (it's there but not specific enough) or **Fail** (it's missing).

1. **Clear user story**: says who (role), what (the capability) and why (the benefit).
2. **Business context**: explains why it matters, such as the customer impact, the goal or the problem it solves. A "so that" that says nothing real counts as Vague.
3. **Testable acceptance criteria**: written in Given/When/Then, testable, and **including at least one failure or edge case**. Criteria that only cover the happy path fail. A loose line like "handle errors" counts as Vague.
4. **Estimated**: has story points, **8 or less**. No estimate, or more than 8, fails.
5. **Dependencies identified and resolved**: dependencies are listed in links or the description, or the issue says there are none, and none are still pending. If dependencies aren't mentioned anywhere, that's Vague.
6. **No open decisions**: nothing is waiting on someone (TBD, "waiting on Finance", "PO to confirm", or open questions in the comments).

## 3. Scoring

- **Ready**: all 6 checks pass.
- **Almost Ready**: no hard blockers, and either 1–2 checks Fail, or any number are only **Vague**. A Vague item always caps the story at Almost Ready, never Ready.
- **Not Ready**: 3 or more checks Fail, OR any hard blocker: no clear who/what/why, no acceptance criteria at all, more than 8 points, an unresolved dependency, or an open decision waiting on someone.

When in doubt between two scores, pick the lower one.

## 4. Output

The output is shared with the PO, so the wording should be neutral and helpful ("needs", "to confirm"), never blaming. Keep it short.

**Part A: one table**, with at most one summary line above it (for example: "5 stories checked: 2 Ready, 2 Almost Ready, 1 Not Ready").

| Story | Score | What's missing | Question to ask the PO |
|---|---|---|---|
| HRT-101 Room selection | ✅ Ready | — | — |
| HRT-103 Seasonal pricing | 🟡 Almost Ready | Failure-case AC is vague | What should happen if no price rule matches the selected dates? |
| HRT-104 Group booking | 🔴 Not Ready | 13 pts; waiting on Finance for pricing rules | Can we split this, and when will Finance confirm the rules? |

Rules for the table:
- **Story**: the Jira key plus a short title (3–5 words). Link the key to the issue if you have its URL.
- **Score**: ✅ Ready / 🟡 Almost Ready / 🔴 Not Ready.
- **What's missing**: only the checks that are Fail or Vague, a few words each, separated by semicolons. Use "—" for Ready.
- **Question to ask the PO**: one concrete, polite question about the actual content of the story, ready to paste into a message to the PO. Use "—" for Ready.

**Part B: suggested fixes** (only for stories that aren't Ready). Keep it to a few lines per story, under a heading with the Jira key:
- **Draft acceptance criteria**: when the AC check is Vague or Fail, write 1–3 missing Given/When/Then criteria, focused on failure and edge cases. Mark them clearly as *drafts for the PO to confirm*.
- **Split suggestion**: when the story is over 8 points, propose 2–3 smaller stories, each with a one-line title and a rough idea of its scope (by workflow step, business rule, user type, or happy path vs. edge cases). Each split should deliver value on its own.
- Skip anything else: no rewritten stories and no per-check breakdown unless the user asks.

## 5. Don't write to Jira

This skill only reads from Jira. Never edit issues, add comments or change fields unless the user explicitly asks you to.