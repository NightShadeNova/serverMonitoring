#!/bin/bash

available=$(grep "MemAvailable" /proc/meminfo | awk '{print $2}')
total=$(grep "MemTotal" /proc/meminfo | awk '{print $2}')

percent=$((available * 100 / total))

echo $percent
