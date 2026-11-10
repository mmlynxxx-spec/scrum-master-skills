---
name: sprint-plan-summary-builder
description: "Create a clean, shareable sprint plan summary after planning is complete — including the sprint goal, committed work, dependencies, risks, capacity notes, and a stakeholder-friendly overview. Use this skill whenever someone mentions 'sprint summary', 'planning summary', 'sprint plan document', 'what did we commit to', 'sprint commitment summary', 'planning recap', 'sprint kick-off doc', 'stakeholder sprint update', 'sprint plan report', or ANY request to document the outcomes of a sprint planning session. Also trigger when a scrum master wants to communicate what the team committed to, when someone needs to send leadership a summary of the sprint plan, or after a planning meeting when someone says 'can you write this up' or 'summarize what we planned.'"
---

# Sprint Plan Summary Builder

Creates a polished, shareable summary after sprint planning — the single document that tells the team, stakeholders, and leadership what's happening this sprint and why.

## Why this matters

After planning, the outcomes live in people's heads and scattered Jira tickets. A good sprint summary creates alignment — the team has a reference point for what they committed to, leadership gets a concise update without attending planning, and when mid-sprint questions arise ("why are we working on X?"), there's a clear answer.

## How to gather inputs

Accept whatever the user provides — meeting notes, a list of committed stories, or even a verbal dump of what was discussed. If the input is thin, ask for the essentials:

### Required inputs
- **Sprint goal**: What is the team trying to achieve this sprint? (1-2 sentences that capture the "why")
- **Committed work**: List of stories/items the team committed to (titles, estimates, and brief descriptions)
- **Sprint dates**: Start and end date

### Helpful but optional
- **Stretch goals**: Items the team will take on if they finish early
- **Capacity notes**: Any relevant availability info (PTO, support rotations, reduced capacity)
- **Dependencies**: Cross-team or external dependencies
- **Risks**: Known risks identified during planning
- **Carryover**: Items carried over from the previous sprint (and why)
- **Sprint theme or focus area**: If the team organizes work into themes
- **What was explicitly deferred**: Items discussed but intentionally left out (and the reasoning)

If the user doesn't provide a sprint goal, help them craft one. A good sprint goal is:
- Outcome-oriented (what will be true at the end of the sprint, not a list of tasks)
- Concise (1-2 sentences)
- Meaningful to stakeholders (not just "finish the stories in the sprint")

## Document structure

Generate a Word document (.docx) following the docx skill's instructions for creating Word documents using docx-js.

**Title**: Sprint Plan — Sprint [number/name] ([date range])

### Section 1: Sprint Goal
The sprint goal in a prominent callout or highlighted block. This is the most important part of the document.

### Section 2: Key Highlights
3-5 bullet points summarizing the most important things happening this sprint. Written for someone who will only read this section — a VP, a product leader, or a partner team. No jargon, no ticket numbers.

### Section 3: Committed Work
A table of committed items with columns:
- Story/ticket ID (if available)
- Title
- Estimate (points, days, or whatever the team uses)
- Owner/assignee (if known)
- Brief description (1 line)

Group by theme or epic if applicable. Show total commitment at the bottom.

If there are stretch goals, list them separately after the committed work with a clear label.

### Section 4: Carryover from Last Sprint
If applicable, list items carried over and a brief note on why (e.g., "blocked by API team," "underestimated complexity"). This provides transparency and context.

### Section 5: Dependencies
A list of cross-team or external dependencies with:
- What the dependency is
- Who/which team owns it
- Current status (resolved, in progress, at risk)
- Impact if it slips

### Section 6: Risks and Mitigations
Known risks from planning, each paired with a mitigation plan or contingency. Be specific — "production deployment on Wednesday may cause interrupts" is better than "deployment risk."

### Section 7: Capacity Notes
Brief summary of team capacity for this sprint — who's out, who's on support, any reduced-capacity situations. Reference the capacity analysis if one was done.

### Section 8: What Stakeholders Need to Know
A short section (3-5 sentences) written specifically for leadership or cross-functional partners. Answers the questions they actually care about:
- What's the team focused on and why?
- Are there any blockers or risks that need escalation?
- When will key deliverables land?
- Is anything being intentionally deferred?

### Visual dashboard (.html)

In addition to the Word document, also produce a **single-page visual dashboard** using React (JSX) or clean HTML with embedded charts. This is the version that gets shared in Slack or pulled up during standup. The dashboard should include:

- **Sprint goal** displayed prominently as a hero banner at the top
- **Commitment breakdown chart** — a horizontal stacked bar or treemap showing committed work grouped by epic/theme, with story point sizes proportional
- **Workload distribution** — a bar chart showing how work is distributed across team members (if owners are known)
- **Dependency map** — a simple node-and-edge diagram showing cross-team or inter-story dependencies, color-coded by status (resolved = green, in progress = yellow, at risk = red)
- **Risk cards** — color-coded summary cards for each risk with severity indicator
- **Capacity snapshot** — a donut chart showing committed points vs. available capacity, with stretch goals shown as a lighter ring
- **Carryover callout** — if items carried over, a small section highlighting what and why
- **Stakeholder summary** — a clean text block at the bottom with the leadership-ready overview

Use a clean, modern color palette. The dashboard should be self-contained (no external dependencies beyond CDN links) and print well.

### Charts in the Word document

Generate chart images (PNG) using a script and embed them in the Word document so it's self-contained. At minimum, include:

- A **commitment breakdown chart** (pie or bar showing work by epic/theme)
- A **capacity utilization gauge** (committed vs. available)
- A **dependency status chart** (simple visual showing dependency health)

## Formatting guidelines

- Use clean, professional formatting with clear section headers
- Tables should be easy to scan — avoid walls of text in cells
- The sprint goal should visually stand out (larger font, bold, or a shaded box)
- Keep the document to 2-4 pages — concise enough to actually be read
- Use the team's terminology (story points, t-shirt sizes, etc.) consistently
- Charts and diagrams should use consistent colors across the .docx and .html outputs

## Tone and style

Professional but not stiff. This document represents the team's plan to the rest of the organization, so it should be clear and confident. Avoid hedging language unless there's genuine uncertainty worth calling out. When noting risks, be matter-of-fact — state the risk, state the mitigation, move on.
