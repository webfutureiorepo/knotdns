#!/usr/bin/env bash

# fail fast
set -e

# We expect `kresctl` command to exist in $PATH
command -v knot-resolver > /dev/null
