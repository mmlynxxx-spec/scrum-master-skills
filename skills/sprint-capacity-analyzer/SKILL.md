---
name: sprint-capacity-analyzer
description: Calculate team sprint capacity using SAFe normalized story points (8 points per developer per 2-week sprint, minus 1 point per PTO or holiday day), shown person by person with names, plus overcommitment warnings and planning risks. Use this skill whenever someone mentions 'sprint capacity', 'team availability', 'how much can we take on', 'capacity planning', 'normalized story points', 'sprint commitment', 'are we overcommitted', 'how many points this sprint', 'team bandwidth', 'PTO impact on sprint', or ANY question about whether a team can handle a given amount of work in an upcoming sprint or iteration.
---

# Sprint Capacity Analyzer

Calculates a team's capacity for the sprint person by person, using normalized story points, so the team can see exactly who is available and how much work fits.

## The method: normalized story points

This is the SAFe normalized estimating approach. Use it as the primary capacity number every time.

1. **Start each developer at 8 points** for a 2-week (10-day) sprint. Count developers and testers; don't count the Product Owner or Scrum Master unless the user says they do delivery work.
2. **Subtract 1 point for each day of PTO or holiday** for that person.
3. **Capacity per person = 8 − PTO days.** Never go below 0.
4. **Total capacity = the sum** of everyone's capacity.

Adjust the starting points only when the user tells you to:
- Sprint length other than 2 weeks: scale the starting points (for example, 1-week sprint = 4 points).
- Part-time members: scale by their allocation (for example, 50% = 4 points).
- People on support rotation or new to the team: subtract the days or points the user specifies.

## How to gather inputs

Accept a table, a list, a spreadsheet or a Jira ticket. You need:
- **Team members by name**
- **PTO or holiday days** for each person this sprint
- Sprint length (default: 2 weeks)

If names aren't given, use the labels the user gives (Developer A, B…). If the user also has candidate stories with points, total them so you can compare against capacity.

Historical velocity is optional. Only mention it if the user provides it, and then only as a single comparison line (see below). Never replace the normalized number with a velocity-based one.

## Output

Lead with the capacity table, laid out exactly like this:

**Capacity Calculation – Sprint [number/name]**

| Team Member | Initial 8 Points | Holidays/PTO | Capacity per Iteration |
|---|---|---|---|
| [Name] | 8 | [days or blank] | [8 − PTO] |
| … | | | |
| | | **Total Capacity** | **[sum]** |

Then, in short plain sentences:
1. **Total capacity** in one line: "The team has [X] points of capacity this sprint."
2. **Who is reduced and why**: "[Name] is out [n] days, so [name] has [x] points."
3. **Backlog comparison** (only if stories were provided): "The candidate backlog is [Y] points, [Y − X] over capacity." Flag anything above capacity as overcommitment.
4. **Velocity check** (only if velocity was provided): one line, e.g. "Recent velocity averages [V] points; plan with that in mind if it's well below [X]."
5. **Risks** (2–4 bullets, each with a suggestion), such as:
   - More than 30% of the team out at once
   - Several people out on the same days
   - Work that depends on someone who's out
   - Commitment above total capacity

Keep it short. No extra charts, gauges or statistics unless the user asks.

## Files

If the user asks for a file:
- **Spreadsheet (.xlsx):** a single sheet with the capacity table above. Use formulas (Capacity = Initial − PTO, Total = SUM) so editing PTO recalculates everything. No extra sections.
- **Word document (.docx):** the capacity table plus the short summary and risks.

## Tone

Plain and direct, written for a Scrum Master or RTE to share with the team. Use names and concrete numbers.
