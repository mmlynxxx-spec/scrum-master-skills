---
name: risk-tradeoff-advisor
description: "Help an overloaded team decide what to cut, defer, split, or classify as stretch during sprint planning. Provides structured tradeoff analysis with recommendations and discussion points for the team. Use this skill whenever someone mentions 'we have too much work', 'overcommitted', 'what should we cut', 'what to defer', 'sprint is overloaded', 'can't fit everything', 'tradeoff discussion', 'prioritize the sprint', 'what's stretch', 'scope the sprint down', 'we need to drop something', 'sprint negotiation', or ANY situation where a team has more work than capacity and needs help deciding what stays and what goes. Also trigger when a scrum master or PM is preparing tradeoff options for the team or product owner, when someone asks 'how do we fit all this in', or when planning reveals the committed work exceeds available capacity."
---

# Risk and Tradeoff Advisor

When the team has more work than capacity, this skill helps structure the conversation: what to keep, what to cut, what to defer, what to split, and what to classify as stretch — with clear reasoning the team can discuss and decide on together.

## Why this matters

Every sprint planning session hits this moment: the team looks at the backlog, looks at their capacity, and realizes something has to give. Without a structured approach, the loudest voice or the most recent request wins. This skill provides a framework for making those tradeoffs deliberately, with the team's goals and constraints in mind.

## How to gather inputs

Accept whatever the user provides about the overcommitment situation. The more context, the better the recommendations. Ask for what's missing:

### The work
- What items are being considered for the sprint? (titles, estimates, brief descriptions)
- What's the total estimated effort?
- What's the available capacity? (points, days, or hours — whatever the team uses)
- How much are they over by?

### The context
- What's the sprint goal? (this is the anchor for prioritization)
- Are there hard deadlines or external commitments on any items?
- Which items have dependencies that affect other teams' plans?
- Are there items that were already committed to stakeholders?
- Which items are partially started or carry over from last sprint?
- Is there a product owner or stakeholder who has expressed priority preferences?

### The constraints
- Are there items that absolutely cannot be cut (regulatory, contractual, safety)?
- Are there items that lose value if delayed (time-sensitive, tied to a release)?
- Are there items where partial delivery is valuable vs. all-or-nothing?

## Analysis framework

### Step 1: Categorize each item

For every item under consideration, assess:

**Value alignment**: How closely does this item support the sprint goal?
- Core — directly delivers the sprint goal
- Supporting — enables or enhances a core item
- Adjacent — valuable but not tied to the sprint goal
- Maintenance — keeps the lights on (bugs, tech debt, support)

**Urgency**: What happens if this waits one sprint?
- Critical — real consequences if delayed (deadline, blocker for others, SLA)
- Important — noticeable impact but manageable
- Can wait — no meaningful harm from a 2-week delay

**Splittability**: Can this be broken into a smaller "must have" and a "nice to have"?
- Unsplittable — it's all or nothing
- Splittable — there's a meaningful smaller version
- Already minimal — it's already been cut down

**Risk profile**: How confident is the team in the estimate?
- Low risk — well-understood, team has done similar work
- Medium risk — some unknowns but manageable
- High risk — significant unknowns, estimate could be way off

### Step 2: Generate recommendations

Based on the categorization, produce specific recommendations in these buckets:

**Keep (committed)**
Items that are core to the sprint goal, have hard deadlines, or block other teams. These stay.

**Cut (remove from sprint)**
Items that are adjacent to the sprint goal, can wait without consequences, and don't block anything. Explain why each can be safely cut and where it should go (next sprint's backlog, icebox, etc.).

**Defer (move to next sprint with intent)**
Items that are important but not urgent this sprint. Different from "cut" — these should be explicitly planned for the next sprint, not just sent back to the backlog. Note any risks of deferral.

**Split (reduce scope)**
Items where a smaller version delivers most of the value. For each, suggest the specific split — what's the MVP version that should stay in the sprint, and what can be a follow-up story.

**Classify as stretch**
Items that are valuable and ready but only if the team finishes committed work early. Stretch items should be independent (not blocking other work) and self-contained (no dangling state if they don't get done).

### Step 3: Identify key tradeoff discussion points

Surface the 2-4 decisions that the team actually needs to discuss. Not everything is a tradeoff — some cuts are obvious. Focus on the genuinely hard calls:

- Items where value and urgency conflict (high value but not urgent, or low value but urgent)
- Items where cutting affects a stakeholder relationship
- Items where the team disagrees on priority
- Items where splitting changes the user experience

For each discussion point, frame both sides clearly so the team can have a productive conversation.

### Step 4: Show the math

After recommendations, show:
- Original total: X points
- After cuts/deferrals/splits: Y points
- Available capacity: Z points
- Buffer: Z - Y points (ideally 10-20% for unplanned work)

If the recommendations still leave the team overcommitted, say so and suggest a second round of cuts.

## Output format

Produce **two deliverables** for every analysis:

1. **Word document (.docx)** — the detailed report. Follow the docx skill's instructions for creating Word documents using docx-js.
2. **Visual dashboard (.html)** — a single-page React or HTML infographic with charts and diagrams. Use Recharts, Chart.js, or inline SVG for the visuals.

Generate chart images (PNG) using a script and embed them in the Word document as well, so the .docx is self-contained with visuals.

### Word document structure

**Title**: Sprint Tradeoff Analysis — Sprint [number/name]

### Section 1: Situation Summary
The overcommitment in one paragraph: how much work is on the table, how much capacity exists, and the gap. Include the sprint goal for reference. Include a **before/after waterfall chart** showing original commitment → cuts → deferrals → splits → final commitment vs. capacity line.

### Section 2: Recommendations
Organized by action (Keep / Cut / Defer / Split / Stretch), with each item showing:
- Item title and estimate
- Recommendation and reasoning
- For splits: the proposed smaller scope and the deferred portion
- For deferrals: when it should come back and any risks

Use a table format for easy scanning. Include a **priority matrix diagram** (2×2 grid: value vs. urgency) with each item plotted, color-coded by recommendation (keep = green, cut = red, defer = yellow, split = blue, stretch = gray).

### Section 3: Tradeoff Discussion Points
The 2-4 genuinely hard calls, framed as questions for the team:
- "Should we keep [X] given that it's not aligned with the sprint goal but was promised to [stakeholder]?"
- "Is the reduced version of [Y] still valuable, or should we defer the whole thing?"

For each, present the arguments on both sides concisely. Include a **tradeoff comparison visual** — a simple side-by-side or pros/cons chart for each decision point.

### Section 4: Revised Sprint Math
A simple before/after table showing the capacity math and remaining buffer. Include a **stacked bar chart** showing the composition of the revised sprint (committed + stretch + buffer) against available capacity.

### Section 5: Next Steps
What needs to happen after the tradeoff discussion — who to notify about deferrals, which stories need to be re-scoped, any follow-up conversations with stakeholders.

### Visual dashboard (.html)

Create a single-page infographic-style dashboard using React (JSX) or clean HTML with embedded charts. The dashboard should include:

- **Header** with sprint name and the overcommitment gap displayed as a large callout (e.g., "32 points committed / 24 points available — 8 points over")
- **Waterfall chart** — showing original total → each reduction action → final committed total vs. capacity line
- **Priority matrix** — interactive or static 2×2 scatter plot (value × urgency) with items color-coded by recommendation
- **Action breakdown** — a grouped bar or sankey-style diagram showing how many points are in each bucket (Keep / Cut / Defer / Split / Stretch)
- **Before/after comparison** — side-by-side donut charts or stacked bars showing sprint composition before and after tradeoffs
- **Tradeoff cards** — the key discussion points presented as decision cards with both sides of the argument
- **Revised capacity math** — a clean summary bar showing committed + stretch + buffer = capacity

Use a clean, modern color palette with consistent meaning: green = keep, red = cut, yellow = defer, blue = split, gray = stretch. The dashboard should be self-contained and print well.

## Tone and style

Neutral and structured — this document facilitates a team decision, it doesn't make the decision. Present options clearly without being prescriptive about what the team "should" do (except for obvious cases). When there's a strong recommendation, say so and explain why, but acknowledge it's the team's call. Avoid emotional language around cutting work — frame it as making space to deliver well on what matters most.
