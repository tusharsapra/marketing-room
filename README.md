# The Marketing Room

I am Tushar Sapra, a marketing expert with experience across clients and campaigns. I built this skill to bring marketing specialists into one structured planning room, challenge assumptions, check budgets and dependencies, and deliver one actionable plan for the brief.

An agency war room for any marketing brief, as one skill for Claude Code and Codex.

Give it a client brief. A Project Head breaks it into requirements and decides who needs to be in the room.
Every specialist (Google Ads, Meta Ads, LinkedIn Ads, SEO, UX, UI, Developer, Creative Strategist, Creative
Ops, Measurement, Client Lead, Copywriter, plus TikTok, YouTube, programmatic, Amazon and CRM when the brief
calls for them) writes its own plan without seeing the others. Then they challenge each other, each one
looking through a lens that is not its usual one: analytical, cynical, business, operations, the client's
eyes, the customer's, brand, risk and compliance, competitive, opportunity. A script checks the numbers:
does the budget add up, can Meta leave its learning phase at that CPA, is tracking ready before launch, can
Creative Ops make that many assets, does the dev work fit before the launch date. The seats in each conflict
negotiate until they agree, or the Project Head rules. A neutral Facilitator writes one integrated
deliverable, and the Project Head checks it against every requirement before it ships.

What comes back is one plan the whole room stands behind: the deliverable, who owns what, the debates and
how each was settled, the Project Head's score, and the questions only the client can answer.

**It never touches your files or your ad accounts.** Everything happens inside `.marketing-room/`. The plan
comes back to you, and acting on it is your call.

## What a session looks like

```
brief ──► Project Head: requirements R1..Rn, facts, who is in the room, questions for the client
            │
            ▼
        kickoff: every seat proposes, blind            (its plan, its asks, its forecast, how it hits others)
            │
            ▼
        script: budget roll-up, impact matrix, RACI, feasibility checks  ──► failing checks become items
            │
            ▼
        challenge: each seat questions 2 others through a dealt lens (cynical and client-eyes every round)
            │
            ▼
        respond: CONCEDE (with the change), REBUT (with evidence) or COMPROMISE, then revise
            │
            ▼
        Facilitator: groups what is still disputed into conflicts, proposes a middle ground
            │
            ▼
        resolve: only the parties to each conflict ACCEPT or counter, until settled or escalated
            │
            ▼
        Project Head rules on what the room could not settle
            │
            ▼
        Facilitator writes the integrated deliverable, tagged [R#] and [D#]
            │
            ▼
        Project Head reviews: requirement by requirement, scored, SHIP or REVISE (at most twice)
```

## Who is in the room

| group | seats |
| --- | --- |
| Core | `google-ads`, `meta-ads`, `linkedin-ads`, `seo`, `ux`, `developer`, `ui`, `creative-strategist`, `creative-ops` |
| Standing | `measurement` (cast whenever an ad seat is), `client-lead` (always), `copywriter` |
| Bench | `tiktok-ads`, `youtube-video`, `programmatic`, `amazon-ads`, `crm-email`: cast only when the brief gives a reason |
| Process | `project-head` opens and closes the session; `facilitator` is neutral, moderates and writes the deliverable |

Each seat's file (`skills/marketing-room/references/seats/`) gives it a mandate, the deliverables it is
accountable for, the KPIs it is judged on, its instincts **and its blind spots** (what it over-pushes, which
is what makes the debate real), a dated platform checklist, the red flags it calls out in others' plans, and
its tension partners. `references/tension-map.md` holds the 360 view: 55 seat pairs, each with "if this seat
does X, here is what happens to that seat, and the agreement that usually settles it".

| lens | the test every challenge must answer |
| --- | --- |
| Analytical | The one number that must be true for this plan to work, and whether it holds. |
| Cynical | The most likely way this fails in real life, and the earliest warning sign. |
| Business | What it does to the client's money, and what happens if it underdelivers by 30%. |
| Operations | Who does it, how many hours, what it waits on, the date it is really ready. |
| Client eyes | What the client will push back on or refuse to sign. |
| Customer | The moment the end customer drops off or feels misled. |
| Brand | Where it makes the brand look inconsistent, generic or cheap. |
| Risk & compliance | The policy, law or rule it could break, and what that costs. |
| Competitive | What the strongest competitor does in response. |
| Opportunity | The biggest upside the plan leaves on the table. |

The dealer gives every seat one lens per round: never its native lens, never one it already wore, cynical
and client-eyes in every round, the rest spread evenly.

## What the script checks, so the models don't have to

The models argue and write. `room.py` owns every id, every sum and every status it can decide mechanically.

- **Budget:** the seats' media asks against the brief's budget (over budget is a BLOCKER that names every seat
  that asked), unallocated money, currency mismatches, percentage splits that do not add up to 100.
- **Learning phase:** for example, Meta needs about 50 optimisation events per ad set per week, so a budget
  and CPA support a fixed number of ad sets; TikTok is similar; Google Smart Bidding wants about 30
  conversions a month per campaign.
- **Minimum daily budgets:** LinkedIn and TikTok minimums per campaign or ad group.
- **Funnel:** the seats' forecasts rolled up into conversions and a blended cost, against the KPI targets.
  A shortfall becomes a decision for the client: more budget, a lower target, or accept the gap.
- **Tracking:** conversion bidding without defined conversion events, consent signals in the EEA and UK, or
  server-side signals (Conversions API, Enhanced Conversions) that nobody has planned or that land after launch.
- **Timeline:** lead times (dev builds, production, legal) against the working days before launch.
- **Creative volume:** the assets the channel plans burn per week against Creative Ops' capacity.
- **Ownership:** exactly one accountable seat per deliverable, and no need addressed to a seat that is not
  in the room.
- **Honesty:** a concession that changes nothing stays contested; more than 80% of serious challenges
  conceded is flagged as possible groupthink; every number in a seat's summary needs a source
  (brief, data file or assumption); every requirement's quote must appear in the brief word for word.
- **Shipping:** the deliverable ships only if every must requirement is met (named heading plus `[R#]`
  tag), no blocker stands, the integrated budget fits, the weighted score is at least 70 and no criterion
  is under 5. The gates overrule the Project Head in both directions.

The thresholds are in `references/benchmarks.json`, each with a source note and a date (October 2026).
Platforms change them, so every check is a warning to verify, not a proof.

## What you get

In `.marketing-room/<run>/final/`:

| file | what it is |
| --- | --- |
| `deliverable.md` | The integrated deliverable, in the outline for its work type |
| `report.md` | The session: the room, the lenses, every conflict and how it was settled, the requirement-by-requirement review, the scores, the checks |
| `budget.csv`, `raci.csv`, `timeline.csv` | The plan's numbers, owners and dates, ready for a spreadsheet |
| `assumptions.csv` | Every assumption the room made, and who made it |
| `client-questions.md` | What only the client can decide, with options and a recommended default |

Work types: **campaign** (campaign or media plan), **audit** (accounts, campaigns, a site or a funnel, from
exports; CSVs from Google Ads, Meta and others are summarised into one shared table), **pitch** (pitch or RFP
response; never invents credentials), **creative** (concepts, the ad-to-page journey, a landing-page spec, an
asset matrix), and **custom** (anything else you describe).

## Install

It needs Python 3.8 or newer. Nothing to pip install.

**Claude Code and Codex together**, from a clone:

```bash
git clone <this repo> marketing-room && cd marketing-room
./install.sh            # links the skill into ~/.claude/skills, ~/.agents/skills (and ~/.codex/skills)
./install.sh --copy     # copy instead of link
./install.sh --project /path/to/repo   # only for one project
```

**As a Claude Code plugin:** `/plugin marketplace add <owner>/<repo>` then `/plugin install
marketing-room@marketing-room`. Claude Code namespaces plugin skills, so it shows up as
`/marketing-room:marketing-room`. Use `install.sh` if you want plain `/marketing-room`.

**As a Codex plugin:** `codex plugin marketplace add <owner>/<repo>`. The repo ships `.codex-plugin/plugin.json`
and `.agents/plugins/marketplace.json` next to the Claude manifests, over the same `skills/` folder.

**With the skills CLI:** `npx skills add <owner>/<repo> -a claude-code -a codex`.

**By hand:** copy `skills/marketing-room` into `~/.claude/skills/` (Claude Code) and `~/.agents/skills/`
(Codex). Claude Code does not read `.agents/`, which is why both are needed.

## Use it

```
/marketing-room                                   (the brief from this conversation)
/marketing-room --quick plan Q1 paid media for this brief: ...
/marketing-room --type audit audit our Google and Meta accounts, exports attached
/marketing-room --deep we have an RFP from a bank, here it is: ...
/marketing-room --seats meta-ads,creative-strategist,creative-ops,copywriter,ux concepts for the spring launch
```

In Codex, use `$marketing-room` the same way. Both can also reach for it without the name when you describe a
marketing brief; when it starts on its own like that, it asks before spending anything.

| flag | what it does |
| --- | --- |
| `--quick` | At most 5 seats, 1 challenge round, no resolve rounds |
| `--deep` | A bigger room, 2 challenge rounds, 2 resolve rounds |
| `--all` | All 17 seats |
| `--seats a,b` / `--add a` / `--drop b` | Pick the room yourself, or adjust the Project Head's cast |
| `--type` | campaign, audit, pitch, creative or custom |
| `--rounds N`, `--resolve N` | Challenge and resolve rounds, 0 to 3 |
| `--no-questions` | Never stop to ask the client; go on the Project Head's defaults |
| `--solo` | No sub-agents; the orchestrator plays each role in turn |
| `--wave W` | Sub-agents per wave (default 10) |
| `--seed S` | Same seed, same lens deal and pairings |

## What it costs

The skill is free. The tokens are yours. `python3 skills/marketing-room/scripts/room.py plan [flags]` prints
the numbers before anything runs, and the skill shows them before it starts.

| profile | seats | sub-agent calls, typical (max) |
| --- | --- | --- |
| `--quick` | 5 | 20 (24) |
| default | 8 | 35 (50) |
| `--deep` | 12 | 75 (95) |
| `--all` | 17 | 68 (95) |

Pick `--quick` for a narrow brief (one to three channels, or one question). A quick room holds five seats
including the Client Lead and Measurement, so on a brief with five channels in scope some channels have no
specialist behind them; the Project Head lists those seats and the producer tells you before kickoff.

Every call reads the brief and a few proposals, so the bill grows with the size of the brief and the data.

## How it is built

The Marketing Room uses an orchestrating `SKILL.md` and a standard-library Python state machine that keeps
session state in one JSON file. Each specialist receives a generated brief, writes its work to disk, and
returns a short status. The main session keeps the results and can resume after context compaction.

```
skills/marketing-room/SKILL.md                 the orchestration steps (Agent Skills format)
skills/marketing-room/scripts/room.py          the state machine: casting, lens deal, routing, checks, gates
skills/marketing-room/references/templates.md  the exact brief every role receives
skills/marketing-room/references/seats/        19 role files: 17 seats, Project Head, Facilitator
skills/marketing-room/references/lenses.json   the 10 lenses
skills/marketing-room/references/tension-map.md  the 360 view: what each seat's choices do to the others
skills/marketing-room/references/work-types/   deliverable outlines and acceptance criteria per work type
skills/marketing-room/references/benchmarks.json  the thresholds behind the checks, with sources
skills/marketing-room/references/rubric.md     the Project Head's scoring and the ship gates
skills/marketing-room/references/hosts.md      Claude Code, Codex and solo mode in detail
skills/marketing-room/assets/brief-template.md the intake checklist
skills/marketing-room/agents/openai.yaml       Codex display metadata
tests/test_room.py                             whole sessions with fake sub-agents, plus unit tests
examples/                                      a B2B lead-gen brief and an e-commerce audit with CSV exports
```

Everything in `references/` is plain text or JSON. Add a seat, a lens, a work type or a tension pair and
the script picks it up.

## The fine print

**The seats are sub-agents of the model you run.** What makes them different is their role file, their lens
and what they are allowed to see. In solo mode one context plays every seat, and the report says so.

**The checks are arithmetic on the seats' own numbers.** They catch a plan that does not add up. They do not
know your account's real CPAs unless the brief or the data says so.

**Platform facts are dated.** Seat checklists and benchmarks are as of October 2026, with volatile ones marked
"(verify)".

**It does not fix a vague brief.** The room asks once for the critical fields, and works from `unknown` where
you do not know. Vague brief in, carefully argued vague plan out.

**It never invents client facts.** Every number is tagged as coming from the brief, a data file or an
assumption, and the assumptions come back to you in a list.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

They run whole sessions (default, quick, deep, all seats, solo, with questions for the client, with failing
outputs) with fake sub-agents, and check the lens dealer across every room size, the routing, every
deterministic check, the ship gates in both directions, the revision cap, and the file formats.

## License

MIT.
