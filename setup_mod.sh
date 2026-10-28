#!/usr/bin/env sh
# Compatibility entry point. The generator always writes to a new directory.
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$SCRIPT_DIR/setup_mod.py" "$@"
