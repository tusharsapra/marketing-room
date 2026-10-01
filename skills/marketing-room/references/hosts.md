# Running the room on each host

The room needs three things from its host: a shell that can run `python3`, permission to write files inside
the current directory, and, ideally, a way to start sub-agents. Everything else is in `room.py`.

## Claude Code

- **Install:** the skill folder goes in `~/.claude/skills/marketing-room/` (personal) or
  `.claude/skills/marketing-room/` (one project). As a plugin it shows up as `/marketing-room:marketing-room`.
- **Invoke:** `/marketing-room <brief or request>`, or just describe a marketing brief and ask for the room.
- **Sub-agents:** the Agent tool (called Task in older versions). One message with one call per job runs a
  wave in parallel:
  - `subagent_type`: `general-purpose`
  - `description`: `room <job id>`
  - `prompt`: `Read <brief path> and follow it exactly. It is your whole brief.`
  - keep the calls in the foreground (`run_in_background: false` where the tool has it) so the wave returns
    together.
- **Waves:** Claude Code runs up to 10 tool calls at once by default (`CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY`).
  Leave `--wave` at 10 unless the user raised that limit.
- **Permissions:** every job writes one or two files under `.marketing-room/`. In the default permission
  mode that is one approval per file; accept-edits mode (Shift+Tab) avoids it.
- **Paths:** `${CLAUDE_SKILL_DIR}` in SKILL.md expands to the skill folder.

## Codex (CLI and IDE)

- **Install:** the skill folder goes in `~/.agents/skills/marketing-room/` (personal) or
  `.agents/skills/marketing-room/` (one repository). Older Codex versions read `~/.codex/skills/`.
  `install.sh` links all of them.
- **Invoke:** `$marketing-room <brief or request>`, pick it from `/skills`, or describe a marketing brief.
- **Sub-agents:** Codex's multi-agent tools. For each job in a wave call `spawn_agent` with the message
  `Read <brief path> and follow it exactly. It is your whole brief.`; then `wait_agent` until every agent in
  the wave has finished; then close them before the next wave. The skill's instructions count as the
  explicit request Codex needs before it spawns agents.
- **Waves:** set `--wave` to your concurrent-agent limit (`agents.max_concurrent_threads_per_session` in
  `~/.codex/config.toml`; older versions call it `max_threads`). If you do not know it, use `--wave 4`.
- **Sandbox:** the workspace-write sandbox is enough: every file the room writes is inside the current
  directory. The room never needs the network.
- **Paths:** Codex does not expand `${CLAUDE_SKILL_DIR}` or `$ARGUMENTS`. Resolve `scripts/room.py`
  relative to the folder that holds SKILL.md, and take the task from the conversation.
- **Unattended (`codex exec`):** pass `--no-questions`, or answer the gate with `answer --assume`.

## Hosts without sub-agents (or `--solo`)

The room still works, one job at a time, in your own context:

1. `ROOM next`, then `ROOM prompts --one`. It writes exactly one brief and names it.
2. Read that brief and do exactly what it says, as that role. Write only the files it names.
3. `ROOM next` again. Repeat until it says collect, then `ROOM collect`.

What still holds in solo mode: every brief is generated from the same client brief; the kickoff proposals
are written before any seat reads another's; the lens deal, the routing, the checks, the caps and the ship
gates are all enforced by the script. What is lost: true independence, because one context plays every seat.
The report says so ("independence is structural only"), and solo defaults to `--quick` to keep the context
small.

## Other agents that read Agent Skills

Cursor, Gemini CLI, OpenCode and other hosts that load `SKILL.md` folders from `.agents/skills/` can run the
room the same way: with their sub-agent tool if they have one (one job per sub-agent, the same one-line
prompt), or in solo mode.

## Troubleshooting

- **"no room here"**: run every command from the directory where you ran `init`, or pass `--dir <run folder>`.
- **A job keeps failing:** `ROOM check` shows what is missing; after two failures `ROOM skip <job>` records
  it as NO OUTPUT and the room carries on (a missing seat is reported as absent).
- **The context was compacted:** `ROOM status`, then `ROOM next`. All state is on disk.
- **A brief looks wrong:** fix `.marketing-room/brief.md` and start a new run with `init`; never edit a
  generated brief.
