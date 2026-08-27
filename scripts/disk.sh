#!/bin/bash
set -euo pipefail
disk=$(df --total | grep "total" | awk '{print $5}' | cut -d'%' -f1)
echo $disk
