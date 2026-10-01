# The Project Head's rubric

The Project Head scores the integrated deliverable against this page. `room.py` does the arithmetic and
applies the ship gates. The deliverable ships only when it passes every gate.

## The six criteria

Each criterion is scored 0 to 10. The weight is its share of the 100-point total.

| criterion | weight | the question |
| --- | --- | --- |
| brief_fit | 25 | Does it do what the brief asked, for the client and audience the brief describes, within the brief's budget, dates and mandatories? |
| strategy | 20 | Is the thinking sound? Does the channel mix follow from the objective, and do the numbers support the targets? Is there a clear reason for each big choice? |
| coherence | 20 | Does it hold together as one plan? No section contradicts another. Budget lines add up. Every dependency between departments has an owner and a date. Decisions from the debate are reflected. |
| feasibility | 15 | Could the team deliver it on these dates with this capacity? Lead times, production volume, learning phases, approvals and tracking readiness are accounted for. |
| measurability | 10 | Is every KPI tied to a tracking source, a reporting cadence and a named owner? Would the client know by week 4 whether it is working? |
| clarity | 10 | Could the client's marketing director act on it on Monday? Plain language, decisions up front, no padding. |

Weighted total = (brief_fit x 25 + strategy x 20 + coherence x 20 + feasibility x 15 + measurability x 10 + clarity x 10) / 10.
That gives a number from 0 to 100.

## Anchors

Use the whole scale. A 7 is not a polite default.

**brief_fit**
- 10: every requirement met, within every stated constraint.
- 7: every requirement touched, one thin.
- 4: a stated requirement or constraint missed or broken.
- 0 to 2: it answers a different brief.

**strategy**
- 10: every major choice has a reason tied to the objective and the numbers, and the obvious alternatives were weighed.
- 7: sound overall, with one choice that is asserted rather than argued.
- 4: the channel mix or budget split does not follow from the objective, or the numbers do not support the targets.
- 0 to 2: generic tactics with no strategy.

**coherence**
- 10: one plan. Numbers reconcile across sections, every hand-off has an owner and date, every decision is reflected.
- 7: one inconsistency a careful reader would catch.
- 4: two sections contradict each other, or budget lines do not add up.
- 0 to 2: a stack of department plans stapled together.

**feasibility**
- 10: every date survives the stated lead times, capacity and learning-phase needs.
- 7: one date or volume is tight but there is a fallback.
- 4: something cannot be ready in time, or the creative or dev load exceeds capacity with no answer.
- 0 to 2: it cannot be delivered as written.

**measurability**
- 10: each KPI has a source, an owner, a cadence and a first read date; tracking gaps have a fix and a date.
- 7: one KPI lacks a source or owner.
- 4: the primary KPI cannot be measured as the plan stands.
- 0 to 2: no measurement plan.

**clarity**
- 10: the client sees what to decide and what happens next within the first page. No padding.
- 7: fine, with some padding or one hard-to-follow section.
- 4: the client has to dig for the decisions.
- 0 to 2: hard to follow at all.

## The ship gates (applied by room.py)

The deliverable ships only if all of these hold:

1. Every must requirement has status **met**. A requirement counts as met only if you name the heading where
   it is met, that heading exists in the deliverable, and the deliverable carries its tag, like `[R3]`.
   Otherwise the script records it as partial.
2. You list no blockers.
3. No BLOCKER check fails on the integrated plan (for example, the budget lines add up to more than the brief allows).
4. The weighted total is at least 70.
5. No criterion scores below 5.

Your SHIP or REVISE line does not override the gates. If you say SHIP and a gate fails, the script sends it back.
If you say REVISE and every gate passes, the script ships it and keeps your required changes as recommendations.
So make your scores and your blockers say what you mean.

## What the Project Head does not reward

- **Length.** A tight plan that meets every requirement beats a long one that meets the same requirements.
- **Confidence.** "This robust, data-driven plan" earns nothing. Check the numbers yourself.
- **Consensus for its own sake.** A room that conceded everything may have watered the plan down. Check that
  what the specialists gave up was worth giving up.
- **Invented facts.** Client results, case studies, benchmarks presented as the client's own data: each one is
  a blocker until labelled as an assumption.
- **Your own taste** where the brief does not ask for it.
