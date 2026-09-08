#!/bin/sh
# Produce optimized JPEG derivatives for the site from the raw photo staging folder.
# Usage: scripts/process-images.sh /path/to/raw
# Raw sources (not committed): Evolve project photography extracted from the
# August 2026 qualification decks plus the Evolve Website Build folder.
set -e
RAW="${1:?raw folder required}"
OUT="$(cd "$(dirname "$0")/.." && pwd)/public/img"
mkdir -p "$OUT"
Q=78

emit() { # emit <src> <basename> <width...>
  src="$1"; name="$2"; shift 2
  for w in "$@"; do
    sips -s format jpeg -s formatOptions $Q -Z "$w" "$src" --out "$OUT/$name-$w.jpg" >/dev/null
  done
}

emit "$RAW/shop.jpg" evolve-fabrication-shop 1920 1280 800
emit "$RAW/frame.jpg" evolve-module-steel-frame 1600 1000 640
emit "$RAW/crane-lift.jpg" evolve-module-crane-lift 990 640
emit "$RAW/crane-set.jpg" evolve-module-crane-set 990 640
emit "$RAW/yard.png" evolve-equipment-yard 1600 1000 640
emit "$RAW/module-wall.jpg" evolve-module-cooling-wall 1050 640
emit "$RAW/module-entry.jpg" evolve-module-entry 688
emit "$RAW/module-exterior.jpg" evolve-module-exterior 552
emit "$RAW/power-louvers.jpg" evolve-power-module-louvers 542
emit "$RAW/power-aerial.jpg" evolve-power-modules-aerial 570
emit "$RAW/switchgear.jpg" evolve-switchgear-lineup 306
emit "$RAW/electrical-room.jpg" evolve-electrical-room 307
emit "$RAW/data-hall-aisle.jpg" evolve-data-hall-aisle 306
emit "$RAW/data-hall-grated.jpg" evolve-data-hall-grated 306

# Open Graph share image: 1200x630 center crop of the fabrication shop.
sips -s format jpeg -s formatOptions 80 -Z 1200 "$RAW/shop.jpg" --out "$OUT/og-evolve.jpg" >/dev/null
sips -c 630 1200 "$OUT/og-evolve.jpg" >/dev/null

ls -la "$OUT"
