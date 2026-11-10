---
name: planning-readiness-checker
description: "Review backlog items before sprint planning and score each Ready, Almost ready, Needs refinement or Not ready, checking scope clarity, acceptance criteria, business context, size, estimation, dependencies and testability. Use for 'check our stories before planning', 'are these stories ready', 'planning readiness', 'pre-planning review' or 'Definition of Ready check'."
---

Planning Readiness Checker
Reviews backlog items before sprint planning to catch common problems — vague scope, missing acceptance criteria, oversized stories, hidden dependencies — so the team doesn't waste planning time on items that aren't ready.
Why this matters
Sprint planning goes sideways when the team tries to commit to stories that haven't been properly refined. Vague stories lead to mid-sprint scope creep. Missing acceptance criteria create different mental models of "done." Oversized items carry hidden risk. This skill does the pre-flight check so planning stays focused and productive.
How to gather inputs
Accept stories in whatever format the user provides — pasted text, a table, a list of titles with descriptions, or even a screenshot. Be flexible about format. If the input is sparse (just titles), note that the review will be limited and suggest the user provide descriptions and acceptance criteria for a more useful analysis.
Ask the user:
What's your team's typical story point scale? (Fibonacci, T-shirt sizes, etc.)
Do you have a formal Definition of Ready? If so, what are its criteria?
Any context about the sprint goal or theme? (helps assess relevance)
What's the team's comfort zone for story size? (e.g., "we try to keep things under 8 points")
If the user doesn't have a formal Definition of Ready, use these sensible defaults:
Clear description of what needs to happen
Acceptance criteria defined
Business value or context articulated
Estimated by the team
No unresolved blockers or dependencies
Small enough to complete in one sprint
Analysis to perform
For each story/item, evaluate against these dimensions:
1. Scope clarity
Is it clear what the team needs to build or do?
Are there ambiguous phrases like "improve," "optimize," "handle edge cases" without specifics?
Could two developers read this and build the same thing?
Flag: Vague scope — explain what's ambiguous and suggest clarifying questions.
2. Acceptance criteria
Are there explicit acceptance criteria or conditions of satisfaction?
Are they testable/verifiable (not subjective like "works well")?
Do they cover the happy path AND key edge cases?
Flag: Missing acceptance criteria — note what's missing and suggest 2-3 example criteria based on the story description.
3. Business context
Is it clear WHY this work matters?
Is there a user persona, use case, or business outcome tied to it?
Would a developer understand the priority and intent?
Flag: Missing business context — suggest a "so that..." clause or ask what user problem this solves.
4. Size and complexity
Based on the description, does this feel like it could be completed in one sprint?
Are there multiple distinct deliverables bundled together?
Does it touch many systems or require coordination across teams?
Flag: Oversized item — suggest how to split it (by user journey, by technical layer, by scenario, etc.).
5. Estimation status
Has the item been estimated?
If estimated, does the estimate seem reasonable given the description?
Are there high-uncertainty items that might benefit from a spike first?
Flag: Unestimated or Risky estimate — recommend estimation or spike work.
6. Dependencies
Does this item depend on work from another team, an external API, a design deliverable, or another story in the same sprint?
Are those dependencies resolved or still in progress?
Flag: Dependency risk — name the dependency and suggest mitigation (reorder, parallelize, or defer).
7. Testability
Can QA (or the team) verify this is done?
Are there test data or environment requirements that need setup?
Flag: Testability concern — note what's needed.
Scoring
Give each story a readiness score:
Ready — meets all criteria, can go into planning as-is
Almost ready — 1-2 minor issues that can be resolved quickly (during planning or with a 5-minute conversation)
Needs refinement — significant gaps that should be addressed before committing
Not ready — major issues; should not be brought into planning
Output format
Produce two deliverables for every analysis:
Word document (.docx) — the detailed report. Follow the docx skill's instructions for creating Word documents using docx-js.
Visual dashboard (.html) — a single-page React or HTML infographic with charts and diagrams. Use Recharts, Chart.js, or inline SVG for the visuals.
Generate chart images (PNG) using a script and embed them in the Word document as well, so the .docx is self-contained with visuals.
Word document structure
Title: Planning Readiness Review — Sprint [number/name]
Section 1: Executive Summary A quick snapshot: X stories reviewed, Y ready, Z need refinement. Overall readiness percentage. Key themes in the issues found. Include a donut chart showing the distribution of readiness scores (Ready / Almost Ready / Needs Refinement / Not Ready) with counts and percentages.
Section 2: Story-by-Story Review For each story, a block containing:
Story title/ID
Readiness score (Ready / Almost Ready / Needs Refinement / Not Ready)
Issues found (with specific, actionable feedback — not generic checklists)
Suggested improvements
Use a table or structured layout that's easy to scan. Include a readiness scorecard visual — a matrix/heatmap showing each story (rows) against each quality dimension (columns: scope, acceptance criteria, business context, size, estimation, dependencies, testability) with green/yellow/red cells.
Section 3: Cross-Cutting Issues Patterns that affect multiple stories:
Common gaps (e.g., "4 of 7 stories lack acceptance criteria")
Dependency clusters (stories that depend on each other)
Sizing concerns (too many large items for the sprint's capacity)
Include a bar chart showing issue frequency by category (e.g., "Missing AC: 4 stories, Vague Scope: 3 stories"). If there are dependency clusters, include a dependency diagram showing which stories link to each other.
Section 4: Refinement Action Items A prioritized list of what needs to happen before planning:
Which stories need the most work
Who should be involved in clarifying them
Suggested order of refinement
Section 5: Recommendations 2-3 practical suggestions for the planning session (e.g., "Consider time-boxing the discussion on Story X since scope is still fluid" or "Story Y and Z are tightly coupled — plan them together").
Visual dashboard (.html)
Create a single-page infographic-style dashboard using React (JSX) or clean HTML with embedded charts. The dashboard should include:
Header with sprint name and overall readiness score as a large percentage/gauge
Readiness distribution — donut or pie chart showing Ready/Almost/Needs Refinement/Not Ready counts
Quality heatmap — a matrix grid with stories on rows and quality dimensions on columns, color-coded green/yellow/red
Issue frequency chart — horizontal bar chart showing how many stories are affected by each issue type
Dependency graph — a simple node-and-edge diagram showing which stories depend on each other (use SVG or a simple force layout)
Story cards — expandable cards for each story showing its score, issues, and suggested fixes
Use color coding consistently: green = Ready, yellow = Almost Ready, orange = Needs Refinement, red = Not Ready. The dashboard should be self-contained and print well.
Tone and style
Write as a helpful teammate, not an auditor. The goal is to make planning better, not to grade anyone's writing. When flagging issues, be specific and constructive — "The acceptance criteria say 'handles errors gracefully' but doesn't specify which errors or what 'gracefully' means. Consider listing the 2-3 most likely error scenarios and the expected behavior for each."
 