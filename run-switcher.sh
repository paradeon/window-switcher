#!/bin/bash

# Get the directory of the script itself
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# echo "Script Directory: $SCRIPT_DIR"

# Define paths relative to the script's location
VENV_DIR="$SCRIPT_DIR/venv"
SCRIPT_NAME="window-switcher.py"
SCRIPT_PATH="$SCRIPT_DIR/$SCRIPT_NAME"

# Log file paths
LOG_PATH="$SCRIPT_DIR/log"
STDOUT_LOG="$SCRIPT_DIR/stdout.log"
STDERR_LOG="$SCRIPT_DIR/stderr.log"

mkdir -p $LOG_PATH

# Create the log files if they do not exist
touch "$STDOUT_LOG"
touch "$STDERR_LOG"

# Command to activate virtual environment and run Python script detached
(
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"

    # Run Python script detached using nohup
    nohup python "$SCRIPT_PATH" > "$STDOUT_LOG" 2> "$STDERR_LOG" &
) &

# Done
# echo "Python script is running in the background and detached from the terminal."

