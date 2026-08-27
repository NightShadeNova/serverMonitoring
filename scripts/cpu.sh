#!/bin/bash
set -euo pipefail
read -r _ user nice system idle _ < /proc/stat
total=$((user + nice + system + idle))
used=$((user + nice + system))
echo $((used * 100 / total))
