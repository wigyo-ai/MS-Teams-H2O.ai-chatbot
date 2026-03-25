#!/usr/bin/env bash
# Packages the h2o-local-tool bundle for upload to Enterprise h2oGPTe.
#
# h2oGPTe expects the ZIP to contain a named directory with files inside it:
#
#   h2o-local-tool/server.py
#   h2o-local-tool/description.md
#   h2o-local-tool/requirements.txt
#
# Run this script from the h2o-local-tool directory or its parent.
#
# Usage:
#   chmod +x build.sh
#   ./build.sh           # from inside h2o-local-tool/
#   # or
#   ./h2o-local-tool/build.sh   # from the parent directory
#
# Output: h2o-local-tool.zip (created in the parent directory)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOL_DIR_NAME="$(basename "$SCRIPT_DIR")"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_ZIP="${PARENT_DIR}/${TOOL_DIR_NAME}.zip"

cd "$PARENT_DIR"

zip -r "$OUTPUT_ZIP" \
    "${TOOL_DIR_NAME}/server.py" \
    "${TOOL_DIR_NAME}/description.md" \
    "${TOOL_DIR_NAME}/requirements.txt"

echo "Created: $(realpath "$OUTPUT_ZIP")"
echo ""
echo "Verify structure (files must be inside a named directory):"
unzip -l "$OUTPUT_ZIP"
