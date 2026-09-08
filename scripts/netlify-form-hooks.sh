#!/usr/bin/env bash
# Create an email notification hook for every Netlify form on the site that does not have one yet.
# Usage: NETLIFY_AUTH_TOKEN=... scripts/netlify-form-hooks.sh <site-id> <email>
set -euo pipefail
SITE_ID="${1:?site id}"; EMAIL="${2:?email}"
API="https://api.netlify.com/api/v1"
auth=(-H "Authorization: Bearer $NETLIFY_AUTH_TOKEN")
forms=$(curl -s "${auth[@]}" "$API/sites/$SITE_ID/forms")
hooks=$(curl -s "${auth[@]}" "$API/hooks?site_id=$SITE_ID")
python3 - "$forms" "$hooks" <<'EOF' | while read -r form_id form_name; do
import json, sys
forms = json.loads(sys.argv[1]); hooks = json.loads(sys.argv[2])
hooked = {h.get("form_id") for h in hooks if h.get("type") == "email"}
for f in forms:
    if f["id"] not in hooked:
        print(f["id"], f["name"])
EOF
  resp=$(curl -s "${auth[@]}" -H "Content-Type: application/json" -X POST "$API/hooks?site_id=$SITE_ID" \
    -d "{\"type\":\"email\",\"event\":\"submission_created\",\"form_id\":\"$form_id\",\"data\":{\"email\":\"$EMAIL\"}}")
  echo "hook for $form_name: $(echo "$resp" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("id") or d)')"
done
echo "done"
