#!/bin/sh
# Deploy dist/ to Netlify through the Netlify API (no CLI or Node required).
#
# Usage:
#   NETLIFY_AUTH_TOKEN=... scripts/deploy-netlify.sh <site-name>
#
# - Creates the site <site-name>.netlify.app if it does not exist yet.
# - Zips the contents of dist/ and uploads it as a production deploy.
# - Waits until Netlify reports the deploy as ready and prints the URL.
#
# The token is read from the environment only; it is never written to disk.
set -eu
NAME="${1:?site name required, e.g. evolve2026-review}"
: "${NETLIFY_AUTH_TOKEN:?NETLIFY_AUTH_TOKEN is required (Netlify > User settings > Applications > Personal access tokens)}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
API="https://api.netlify.com/api/v1"
AUTH="Authorization: Bearer $NETLIFY_AUTH_TOKEN"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

json() { python3 -c 'import json,sys; d=json.load(sys.stdin); print(d'"$1"')' 2>/dev/null; }

echo "Building site..."
(cd "$ROOT" && python3 build.py && python3 check.py)

echo "Looking up site $NAME..."
SITE_JSON="$(curl -s -H "$AUTH" "$API/sites/$NAME.netlify.app" || true)"
SITE_ID="$(printf '%s' "$SITE_JSON" | json '["id"]' || true)"
if [ -z "$SITE_ID" ]; then
  echo "Creating site $NAME.netlify.app..."
  SITE_JSON="$(curl -s -H "$AUTH" -H "Content-Type: application/json" -X POST "$API/sites" -d "{\"name\":\"$NAME\"}")"
  SITE_ID="$(printf '%s' "$SITE_JSON" | json '["id"]' || true)"
  if [ -z "$SITE_ID" ]; then
    echo "Could not create the site. Netlify said:"; printf '%s\n' "$SITE_JSON"; exit 1
  fi
fi
SITE_URL="$(printf '%s' "$SITE_JSON" | json '["ssl_url"]')"
echo "Site id: $SITE_ID ($SITE_URL)"

echo "Enabling form detection..."
curl -s -o /dev/null -H "$AUTH" -H "Content-Type: application/json" -X PATCH "$API/sites/$SITE_ID" \
  -d '{"processing_settings":{"html":{"pretty_urls":true}}}' || true

echo "Packaging dist/..."
(cd "$ROOT/dist" && zip -qr "$TMP/site.zip" . -x '.DS_Store')
echo "Uploading $(du -h "$TMP/site.zip" | cut -f1) to Netlify..."
DEPLOY_JSON="$(curl -s -H "$AUTH" -H "Content-Type: application/zip" -X POST "$API/sites/$SITE_ID/deploys" --data-binary "@$TMP/site.zip")"
DEPLOY_ID="$(printf '%s' "$DEPLOY_JSON" | json '["id"]' || true)"
if [ -z "$DEPLOY_ID" ]; then
  echo "Upload failed. Netlify said:"; printf '%s\n' "$DEPLOY_JSON"; exit 1
fi

printf "Waiting for deploy %s" "$DEPLOY_ID"
for i in $(seq 1 60); do
  STATE="$(curl -s -H "$AUTH" "$API/deploys/$DEPLOY_ID" | json '["state"]')"
  case "$STATE" in
    ready) echo; echo "Deploy is live: $SITE_URL"; exit 0 ;;
    error) echo; echo "Deploy failed. Check the Deploys tab in Netlify."; exit 1 ;;
    *) printf "."; sleep 3 ;;
  esac
done
echo; echo "Timed out waiting for the deploy; check the Netlify dashboard."; exit 1
