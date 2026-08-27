#!/bin/bash
set -euo pipefail

available=$(grep "MemAvailable" /proc/meminfo | awk '{print $2}')
total=$(grep "MemTotal" /proc/meminfo | awk '{print $2}')

percent=$(( (total - available) * 100 / total ))

echo $percent
