#!/usr/bin/env sh
set -euo pipefail

exec $@ --port ${PORT:-80}
