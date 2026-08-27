#!/bin/bash
#Change INTERVAL_SECONDS value for how often you want the script to send metrics.
#Change PROJECT_ROOT to where the project is located
INTERVAL_SECONDS=15
PROJECT_ROOT="/home/nova/projects" 

PY_EXEC="$PROJECT_ROOT/server-monitoring/venv/bin/python" 
PUSH="$PROJECT_ROOT/metrics_push.py"

chmod +x "$PUSH" 
chmod +x "$PROJECT_ROOT/scripts/cpu.sh"
chmod +x "$PROJECT_ROOT/scripts/disk.sh"
chmod +x "$PROJECT_ROOT/scripts/memory.sh"

echo "Set up done"
while true; do
    echo "Started"
    "$PY_EXEC" "$PUSH"
    sleep "$INTERVAL_SECONDS"
done