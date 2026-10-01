---
name: marketing-room
description: >-
  Run an agency war room on any marketing brief. A Project Head breaks the brief into requirements and
  casts specialist seats (Google, Meta, LinkedIn, TikTok, YouTube, programmatic and Amazon ads, SEO, UX,
  UI, developer, creative strategist, creative ops, copywriter, measurement, client lead, CRM and email).
  Each seat proposes on its own, then challenges the others through a dealt lens (analytical, cynical,
  business, operations, client, customer, brand, risk, competitive, opportunity). A script checks budgets,
  learning phases, tracking and timelines; the seats negotiate every conflict; the Project Head checks
  each requirement and ships one integrated deliverable: a media plan, an audit, a pitch, a creative and
  landing-page brief, or a custom task. Use for campaign and media plans, paid media audits, RFP
  responses, creative briefs, or when the user says marketing room, war room, agency kickoff, or asks to
  get the whole team on a marketing problem.
license: MIT
compatibility: Needs Python 3.8+ (standard library only). Uses sub-agents where the host has them (Claude Code Agent tool, Codex spawn_agent); otherwise runs solo.
metadata:
  short-description: An agency war room that debates a brief and ships one plan
  version: "1.0.0"
---

# The Marketing Room

A marketing agency in a box. Before a project starts, the departments sit together: the Project Head
reads the brief and decides who is in the room; every specialist writes its own plan without seeing the
others; then they challenge each other, each through a lens that is not their usual one; a script checks
the numbers; the people in a conflict negotiate until they agree or the Project Head rules; a neutral
Facilitator writes one integrated deliverable; and the Project Head checks it against every requirement
before it ships.

You are the producer. You run the session. You never play a seat, never write a challenge, never rule on
a conflict and never write the deliverable.

What the user typed after the skill name: `$ARGUMENTS`

If that is blank, or still reads literally as a placeholder, nothing was passed: take the task from the
conversation.

## The tool

Every piece of bookkeeping goes through `scripts/room.py` in this skill's folder (the folder that holds
this SKILL.md; in Claude Code it is `${CLAUDE_SKILL_DIR}`, and if that text is unexpanded, use the base
directory the host printed for this skill or the path you loaded this file from):

```bash
python3 "<this skill's folder>/scripts/room.py" <command>
```

Below, `ROOM` means exactly that command. Every command the tool prints after that is a complete command
with the absolute path, so copy what it prints. The state lives in `.marketing-room/<run>/room.json` in the
current directory, and every command after `init` finds it through `.marketing-room/LATEST`.

## Step 1: size it, and get a yes if nobody asked for it

Read the flags out of the request. Everything that is not a flag is the task.

| flag | meaning |
| --- | --- |
| `--quick` | At most 5 seats, 1 challenge round, no resolve rounds. About 20 sub-agent calls. |
| (none) | The Project Head casts 4 to 10 seats. 1 challenge round, up to 2 resolve rounds. About 35. |
| `--deep` | A bigger room, 2 challenge rounds, 2 resolve rounds. About 75. |
| `--all` | Every one of the 17 seats. |
| `--seats a,b,c` | Exactly these seats. `--add` / `--drop` adjust the Project Head's cast instead. |
| `--type T` | Force the work type: campaign, audit, pitch, creative or custom. |
| `--rounds N`, `--resolve N` | Override the number of challenge or resolve rounds (0 to 3). |
| `--no-questions` | Never stop to ask the client; use the Project Head's defaults. |
| `--solo` | No sub-agents: you run every job yourself, one at a time. Defaults to `--quick`. |
| `--wave W` | Sub-agents per wave. Default 10. |
| `--seed S` | Fixes the lens deal and the pairings. |

Run `ROOM plan` with the same flags. It prints the sub-agent calls and writes nothing. `--quick` suits a
narrow brief (one to three channels); a quick room holds five seats including client-lead and measurement,
so on a wider brief some channels get no specialist. After intake, `collect` prints the room and any seats
the Project Head wanted but could not seat: tell the user in one line, and offer the default room instead.

- **The user asked for the room** (named the skill, said "marketing room" or "war room", or asked to get
  the whole team on it): tell them in one line how big it is, for example "Marketing Room: about 35
  sub-agent calls", and start.
- **This skill fired on its own** because the request looks like a marketing brief: ask once before
  spending anything. Offer the full room, `--quick`, or an ordinary single answer. Wait for the answer.

Sub-agents write their work into `.marketing-room/` in the current directory. In Claude Code's default
permission mode that is one approval per file; suggest accept-edits mode (Shift+Tab) for the run. In
Codex, the workspace-write sandbox is enough. Do not change the user's settings yourself.

## Step 2: write the brief

This is the step that decides the result. **Sub-agents cannot see this conversation.** Every seat knows
only what is in the brief, so write `.marketing-room/brief.md` from `assets/brief-template.md` (in this
skill's folder), keeping its headings:

- The client's own words wherever you can. Every requirement, number, date and constraint the user stated
  anywhere in the conversation.
- Never invent a fact. Write `unknown` where a fact is missing, and "no budget given" if there is none
  (the seats then plan in percentages).
- If a critical field (client and offer, work type, business goal, KPIs, budget, timeline, geography) is
  missing, ask the user once, in one message, for all of them together. If they do not know, write
  `unknown` and carry on.
- Data: list the absolute paths of any exports, reports or screenshots under "Data files and links", and
  pass the same files to `init` with `--data`. CSV exports are summarised by the script into one shared
  table. For a URL, fetch the page yourself if you can and save it as a `.md` snapshot under
  `.marketing-room/sources/`, then pass that file with `--data`. Seats never browse.
- Do not write your own view of the right answer into the brief. That pushes every seat the same way,
  which defeats the room.

## Step 3: init

```bash
ROOM init --brief .marketing-room/brief.md [flags] [--data FILE ...]
```

It copies the brief and the data into a new run folder, prints any critical brief fields that are still
empty, and opens the intake. If it flags a critical field and you have not asked the user yet, ask now,
once, fix the brief and run `init` again.

## Step 4: the loop

Always drive it with `ROOM next`. It reads the state on disk and prints the next step and the exact
commands.

Every step that runs sub-agents works the same way:

1. `ROOM prompts` writes one brief per job into the run folder and lists the jobs in waves.
2. Launch **one wave at a time** and wait until every job in the wave has replied:
   - **Claude Code:** one message with one Agent tool call per job (called Task in older versions):
     `subagent_type` `general-purpose`, `description` `room <job id>`, `prompt`
     `Read <brief path> and follow it exactly. It is your whole brief.` Keep them in the foreground so
     the wave comes back together.
   - **Codex:** `spawn_agent` once per job with that same one-line message, then `wait_agent` until all
     of them are done, then close them. Set `--wave` to your concurrent-agent limit.
   - **No sub-agent tool, or `--solo`:** run `ROOM prompts --one`, read the one brief it names, do
     exactly what it says as that role, write only the files it names, then `ROOM next`. One job at a
     time; do not read ahead.

   `references/hosts.md` has the details for each host.
3. Run `ROOM next`. If an output is missing, it sends you back to the same step and `prompts` lists only
   the missing jobs: re-run those once. If a job fails twice, run `ROOM skip <job id>` and move on.
4. When `next` says collect, run `ROOM collect`. It validates every output. Anything it rejects is listed
   with the reasons; run those jobs again (`prompts` puts the reasons into their briefs).

The order `next` takes you through: **intake** (the Project Head breaks the brief down and casts the
room), then **kickoff** (every seat proposes, blind), then per round **challenge** → **respond** →
**moderate**, then **resolve** rounds (only the seats in open conflicts), then **ruling** (only if
something was escalated), **integrate** (the Facilitator writes the deliverable), **review** (the
Project Head ships it or sends it back, at most twice), then DONE.

**Questions for the client.** If `next` prints questions instead of jobs, the Project Head cannot start
without answers. Ask the user those questions in one message, with the default for each. Write their
answers to `.marketing-room/answers.md` and run `ROOM answer --file .marketing-room/answers.md`. If they
want to go ahead on the defaults, or you are running unattended, run `ROOM answer --assume`.

After each `collect`, give the user one line, such as "Kickoff done: 9 seats on the table, 3 checks
failing." Nothing more. Never paste proposals, challenges or verdicts into the chat during the run.

## Step 5: the result

Run `ROOM report`, then read `final/deliverable.md` and `final/report.md` in the run folder. Those are the
only outputs you read in the whole run. Give the user:

1. **The deliverable.** In full if it is under about 2,500 words; otherwise its executive summary, its
   section list and the path.
2. **Who owns what.** A short table from `final/raci.csv`.
3. **The debate.** Three to six bullets: the conflicts that mattered, who argued what, and how each was
   settled (by the parties, by the Project Head, or left to the client).
4. **The verdict.** SHIPPED or SHIPPED_WITH_CAVEATS and the score. If there are caveats, list them as the
   report states them. Never round a caveat away.
5. **What the client must decide or confirm.** From `final/client-questions.md`, plus the assumptions that
   matter most.
6. **Where everything is:** the `final/` folder, including `budget.csv`, `raci.csv`, `timeline.csv` and
   `assumptions.csv`.

The deliverable is advice. Do not act on it (no ad account changes, no site edits, no emails to anyone)
unless the user asks you to.

## Rules for the producer

- You run the session. You do not propose, challenge, moderate, rule or write the deliverable. `collect`
  records what the roles decided; the script applies the rules.
- Every brief is generated by `prompts` from the one client brief, byte for byte the same for everyone.
  Never paraphrase the brief for one job, add a hint to one job's call, or edit a generated brief.
- Do not read proposals, challenges or verdicts during the run. `next`, `status` and `show` are all you
  need. In solo mode you do each job yourself: read only the files that job's brief names, write its
  files, and carry nothing from one seat into the next beyond what the brief tells you to read.
- If your context gets compacted mid-run, nothing is lost. Run `ROOM status`, then `ROOM next`.
- Run every command from the directory you ran `init` in.
- Sub-agents only write inside the run folder. If one wrote anywhere else, tell the user.
- If the user says stop, stop. `ROOM status` shows where it got to and `ROOM next` resumes it later.
- Platform numbers in the seat files and in `references/benchmarks.json` are dated October 2026 and the
  volatile ones are marked "(verify)". The script's checks are warnings to verify, not proof.

## Who is in the building

- **Core seats:** `google-ads`, `meta-ads`, `linkedin-ads`, `seo`, `ux`, `developer`, `ui`,
  `creative-strategist`, `creative-ops`.
- **Standing seats:** `measurement`, `client-lead` (always in the room), `copywriter`.
- **Bench, called in when the brief needs them:** `tiktok-ads`, `youtube-video`, `programmatic`,
  `amazon-ads`, `crm-email`.
- **Process roles:** `project-head` (opens and closes the session), `facilitator` (neutral; moderates and
  writes the deliverable).
- **Lenses:** analytical, cynical, business, operations, client-eyes, customer, brand, risk-compliance,
  competitive, opportunity. Cynical and client-eyes are dealt every round; nobody wears their own native
  lens or the same lens twice.

Each seat's expertise is in `references/seats/<id>.md`, the cross-department impacts in
`references/tension-map.md`, the deliverable outlines in `references/work-types/`, the Project Head's
scoring in `references/rubric.md`, and every brief the roles receive in `references/templates.md`. You do
not need to read them to run the room; the script pastes the right parts into each brief.
