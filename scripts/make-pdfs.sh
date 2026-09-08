#!/usr/bin/env bash
# Render the five lead-magnet PDFs from the built Insight pages with headless Chrome.
# Run after `python3 build.py`; then run build.py again so dist/ picks up public/downloads/.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
PORT="${PORT:-8765}"
OUT="$ROOT/public/downloads"
mkdir -p "$OUT"

# source insight URL -> output file (must match LEAD_MAGNETS in data.py)
MAP=$(python3 - <<'EOF'
import sys; sys.path.insert(0, ".")
import data as D
for m in D.LEAD_MAGNETS:
    print("%s %s" % (m["source"], m["pdf"].split("/")[-1]))
EOF
)

cd "$ROOT/dist"
python3 -m http.server "$PORT" >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null || true' EXIT
sleep 1

echo "$MAP" | while read -r url file; do
  [ -z "$url" ] && continue
  target="$OUT/$file"
  rm -f "$target"
  prof=$(mktemp -d /tmp/evolve-pdf.XXXX)
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --user-data-dir="$prof" \
    --run-all-compositor-stages-before-draw --virtual-time-budget=6000 --timeout=15000 \
    --print-to-pdf="$target" "http://localhost:$PORT$url?pdf=1" >/dev/null 2>&1 &
  pid=$!
  for i in $(seq 1 60); do [ -s "$target" ] && break; sleep 0.5; done
  sleep 1; kill $pid 2>/dev/null || true; wait $pid 2>/dev/null || true
  rm -rf "$prof"
  if [ -s "$target" ]; then echo "ok   $file ($(stat -f %z "$target") bytes)"; else echo "FAIL $file"; exit 1; fi
done
