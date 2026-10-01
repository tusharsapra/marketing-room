# Work type: Audit

## What the client is buying
An independent, evidence-based diagnosis of what is wrong with an account, campaign, site or funnel, what it is costing them, and the order in which to fix it. Every finding must point to the evidence behind it, and the audit must say plainly what it could not see. The client should finish reading knowing the biggest problems, who fixes each one and by when, and how they will know each fix worked.

## What intake must pull out of the brief
- What is being audited (accounts, platforms, campaigns, site sections or funnel steps) and what is explicitly out of scope.
- The symptom that triggered the audit, in the client's words, with numbers and dates (for example ROAS down from 3.8 to 2.1 over six months).
- The KPI and target the account should be judged against, including break-even or target ROAS, CPA or CPL if the client knows it.
- Every data file, screenshot and URL supplied, with its date range, currency, attribution setting and the metrics it contains.
- Known changes in the period: new campaign types, structure or budget moves, site or checkout changes, pricing, tracking changes, team or agency changes.
- Tracking status: conversion events and their sources, possible double counting, Enhanced Conversions, CAPI, consent mode and CMP per market, and backend (store or CRM) figures for the same period.
- Budget, markets, languages and any regulated-category rules that limit the fixes.
- Who can make fixes and how fast: account access, developer or freelancer days, creative capacity.
- The deadline for the audit, the length of the fix period, and any peak trading period the fixes must land before.

## What each seat's kickoff should focus on
- Every seat: findings, not plans. Each finding states what was observed, the evidence (file name plus row or column, or the screenshot), the likely cause, the business impact in the brief's currency where it can be estimated, a proposed severity and a confidence level (high, medium, low).
- Severity scale, used by every seat. Critical: broken tracking, policy or legal exposure, or money lost now at a scale that changes the result; fix this week. High: clear, material waste or missed return; fix in the first two weeks. Medium: a real but smaller inefficiency; fix within the fix period. Low: hygiene and good practice; fix when convenient. Severity measures impact and urgency, not certainty; confidence is stated separately.
- Every seat: recompute key ratios (CTR, CPC, CPA, ROAS, conversion rate, share of spend) from the raw columns instead of trusting a summary, and flag any figure that does not reconcile with the brief.
- Every seat: list what it needed to see but could not, and how that limits its findings.
- Ad seats: structure, budget distribution against return, bidding and learning status, audience or keyword overlap and cannibalisation, feed or catalogue health, creative volume and fatigue signals such as frequency.
- measurement: whether the conversion data can be trusted at all, since every other finding depends on it; double counting, missing server-side signals, consent gaps, and the gap between platform-reported and backend figures.
- ux, developer and seo (when the site or funnel is in scope): friction and drop-off points, page speed and Core Web Vitals, broken or mismatched landing pages, technical errors.
- client-lead: which findings the client will contest, which fixes need client approval or money, and how to present bad news without overstating it.
- Usually essential: measurement, client-lead and the ad seat for each audited platform. Add ux and developer for site or funnel audits, seo for organic search, and creative-strategist or creative-ops when creative fatigue is suspected.

## Deliverable outline
1. Executive summary: a health verdict (Healthy, Needs attention, Underperforming or Broken), a separate evidence-coverage note (Strong, Partial or Thin, with one line on why), the three findings that matter most, and the estimated impact of fixing them.
2. Scope and sources reviewed: what was audited, each file or screenshot with its date range, currency and attribution setting, and what was out of scope.
3. Performance snapshot: headline metrics recomputed from the supplied data, compared with the client's target and with earlier periods where data allows.
4. Findings by severity: every finding grouped under Critical, High, Medium and Low, each with an ID, area, observation, evidence reference, likely cause, impact, confidence and owning seat.
5. Tracking and data integrity: whether conversions are counted correctly, the gap between platform and backend figures, consent and server-side status, and how far the other findings can be trusted as a result.
6. Structure, bidding and budget: account and campaign structure, budget distribution against return, bidding strategies and learning status, overlap and cannibalisation.
7. Creative, audiences and landing experience: creative volume and fatigue, audience quality and reach, and the ad-to-page experience where evidence exists.
8. Prioritised fix plan: fixes ordered by severity and then by effort, each with owner, effort estimate, dependency, start and finish dates, expected effect and the metric that confirms it worked, laid out week by week across the fix period in the brief.
9. Evidence and data gaps: everything that could not be verified and why, the data that would close each gap, and which findings would change if it did.
10. Owners and responsibilities: a table of each fix with the accountable seat, the client-side owner and the due date.
11. Risks and mitigations: risks from making the fixes (learning resets, short-term volume drops, tracking changes that shift reported numbers) and from not making them, each with a mitigation and owner.
12. Assumptions: every assumption behind the impact estimates and the health verdict, with its source.
13. Decisions and open questions for the client: approvals needed to start the fixes, each with a recommendation and needed-by date, followed by questions whose answers would close evidence gaps.

## Acceptance criteria
- Every finding cites specific evidence (file and row or column, or a named screenshot), or is labelled as an inference with its reasoning shown.
- Every finding carries exactly one severity from Critical, High, Medium or Low, and one confidence level.
- The executive summary gives the health verdict and the evidence-coverage note as two separate statements, and a Thin coverage note is never paired with a confident verdict without saying so.
- Recomputed metrics match the source data, and any number that does not reconcile with the client's stated figures is flagged, not smoothed over.
- Every Critical and High finding has a fix in the fix plan with an owner, a date and a success metric.
- The fix plan fits the stated period and capacity (developer days, account access) and puts tracking fixes before any optimisation that depends on them.
- Evidence and data gaps lists every source that was needed but not supplied, and no finding claims more than its evidence supports.
- Impact estimates are in the brief's currency with the calculation shown.
- Fixes that reset learning or change reported numbers are flagged, with their timing relative to any peak period in the brief.
