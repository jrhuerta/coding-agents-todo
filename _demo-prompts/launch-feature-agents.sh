#!/bin/bash
# Launch tmux with 2 panes, each running cursor-cli agent for a different feature.
# Run from project root after the base app is scaffolded.

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
FEATURES_DIR="$PROJECT_DIR/features"
SESSION_NAME="cursor-features"

# Check agent is available
if ! command -v agent &>/dev/null; then
  echo "Error: 'agent' (Cursor CLI) not found. Install with: curl https://cursor.com/install -fsS | bash"
  exit 1
fi

PROMPT_FILES=("$FEATURES_DIR"/*.md)
NUM_AGENTS=${#PROMPT_FILES[@]}

if [[ $NUM_AGENTS -eq 0 ]]; then
  echo "Error: No .md prompt files found in $FEATURES_DIR"
  exit 1
fi

# Create tmux session with the first feature
tmux new-session -d -s "$SESSION_NAME" -c "$PROJECT_DIR"
tmux send-keys -t "$SESSION_NAME:0.0" \
  "agent '$(cat "${PROMPT_FILES[0]}")'" C-m

# Split for each remaining feature
for ((i = 1; i < NUM_AGENTS; i++)); do
  tmux split-window -h -t "$SESSION_NAME" -c "$PROJECT_DIR"
  tmux send-keys -t "$SESSION_NAME:0.$i" \
    "agent '$(cat "${PROMPT_FILES[$i]}")'" C-m
done

tmux select-layout -t "$SESSION_NAME" even-horizontal

echo "Attaching to tmux session '$SESSION_NAME' ($NUM_AGENTS agents)..."
tmux attach-session -t "$SESSION_NAME"
