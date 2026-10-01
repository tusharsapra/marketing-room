#!/bin/sh
# Install The Marketing Room for Claude Code and Codex (and any agent that reads .agents/skills).
#
#   ./install.sh                  link the skill into ~/.claude/skills, ~/.agents/skills (and ~/.codex/skills
#                                 if ~/.codex exists)
#   ./install.sh --copy           copy instead of linking (Windows, or if you want a frozen copy)
#   ./install.sh --project DIR    install into DIR/.claude/skills and DIR/.agents/skills instead
#   ./install.sh --claude-only    only Claude Code
#   ./install.sh --codex-only     only Codex and other .agents/skills readers
#   ./install.sh --uninstall      remove what this script installed
#   ./install.sh --force          replace an existing marketing-room folder that this script did not create
set -eu

NAME="marketing-room"
HERE=$(cd "$(dirname "$0")" && pwd)
SRC="$HERE/skills/$NAME"
MODE=link
CLAUDE=1
CODEX=1
PROJECT=""
UNINSTALL=0
FORCE=0

while [ $# -gt 0 ]; do
  case "$1" in
    --copy) MODE=copy ;;
    --project) shift; PROJECT="${1:?--project needs a directory}" ;;
    --claude-only) CODEX=0 ;;
    --codex-only) CLAUDE=0 ;;
    --uninstall) UNINSTALL=1 ;;
    --force) FORCE=1 ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

[ -f "$SRC/SKILL.md" ] || { echo "cannot find $SRC/SKILL.md" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || echo "warning: python3 not found; the room needs Python 3.8 or newer" >&2

if [ -n "$PROJECT" ]; then
  BASE=$(cd "$PROJECT" && pwd)
  CLAUDE_DIR="$BASE/.claude/skills"
  AGENTS_DIR="$BASE/.agents/skills"
  CODEX_DIR=""
else
  CLAUDE_DIR="$HOME/.claude/skills"
  AGENTS_DIR="$HOME/.agents/skills"
  CODEX_DIR=""
  [ -d "$HOME/.codex" ] && CODEX_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
fi

targets=""
[ "$CLAUDE" = 1 ] && targets="$targets $CLAUDE_DIR"
[ "$CODEX" = 1 ] && targets="$targets $AGENTS_DIR"
[ "$CODEX" = 1 ] && [ -n "$CODEX_DIR" ] && targets="$targets $CODEX_DIR"

ours() {
  # true if $1 is a link to this repo's skill, or a copy this script made
  [ -L "$1" ] && [ "$(cd "$1" && pwd -P)" = "$(cd "$SRC" && pwd -P)" ] && return 0
  [ -f "$1/.installed-by-marketing-room" ] && return 0
  return 1
}

for dir in $targets; do
  dest="$dir/$NAME"
  if [ "$UNINSTALL" = 1 ]; then
    if [ -e "$dest" ] || [ -L "$dest" ]; then
      if ours "$dest"; then rm -rf "$dest"; echo "removed $dest"; else echo "left $dest alone: this script did not install it"; fi
    fi
    continue
  fi
  mkdir -p "$dir"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    if ours "$dest" || [ "$FORCE" = 1 ]; then
      rm -rf "$dest"
    else
      echo "skipped $dest: something else is already there (use --force to replace it)"
      continue
    fi
  fi
  if [ "$MODE" = copy ]; then
    cp -R "$SRC" "$dest"
    touch "$dest/.installed-by-marketing-room"
    echo "copied  $dest"
  else
    ln -s "$SRC" "$dest"
    echo "linked  $dest -> $SRC"
  fi
done

if [ "$UNINSTALL" = 0 ]; then
  echo ""
  echo "Claude Code: /$NAME <your brief>      Codex: \$$NAME <your brief>"
  echo "Restart the agent (or start a new session) so it picks up the skill."
fi
