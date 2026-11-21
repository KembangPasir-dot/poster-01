#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
CHROME_PROFILE="$(mktemp -d /tmp/poster-01-chrome.XXXXXX)"
trap 'rm -rf -- "$CHROME_PROFILE"' EXIT
cd -- "$SCRIPT_DIR"
/home/hatch/workspace/.browser-cache/chrome-linux64/chrome \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --hide-scrollbars \
  --force-device-scale-factor=1 \
  --window-size=1024,1024 \
  --user-data-dir="$CHROME_PROFILE" \
  --screenshot=entry.png \
  "file://${SCRIPT_DIR}/poster.html"
