#!/usr/bin/env bash
# Prepare and push the public contribution repo. No secrets are stored in git.
#
# Usage:
#   GITHUB_REPO=owner/repo GITHUB_TOKEN=ghp_xxx ./push.sh
# or, if your machine already has GitHub credentials configured:
#   GITHUB_REPO=owner/repo ./push.sh
set -euo pipefail

cd "$(dirname "$0")"

if [[ -z "${GITHUB_REPO:-}" ]]; then
  echo "Set GITHUB_REPO=owner/repo first. Create an EMPTY public repo on GitHub." >&2
  exit 2
fi

# Never publish key material.
leaked=$(git ls-files '*.pem' '*.key' '*passphrase*' 'AGENT-CREDENTIALS.md' '.flop-pass')
if [[ -n "$leaked" ]]; then
  echo "Refusing to push — secret files are tracked:" >&2
  echo "$leaked" >&2
  exit 3
fi

if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git -c user.name='Technocore Agent' -c user.email='agent@local.invalid' \
    commit -m 'Update FLOP testnet readiness kit'
fi

COMMIT=$(git rev-parse HEAD)
URL="https://github.com/${GITHUB_REPO}"

echo "Pushing $COMMIT to $URL (branch main)"

if [[ -n "${GITHUB_TOKEN:-}" ]]; then
  # Use an auth header instead of embedding the token in the remote URL, so git
  # errors and .git/config never expose it.
  AUTH_HEADER=$(printf 'x-access-token:%s' "$GITHUB_TOKEN" | base64 | tr -d '\n')
  git -c "http.https://github.com/.extraheader=AUTHORIZATION: basic ${AUTH_HEADER}" \
    push "https://github.com/${GITHUB_REPO}.git" HEAD:refs/heads/main
  unset GITHUB_TOKEN AUTH_HEADER
else
  if ! git remote get-url origin >/dev/null 2>&1; then
    git remote add origin "${URL}.git"
  fi
  git push -u origin HEAD:refs/heads/main
fi

# Keep the local remote clean (no token embedded).
git remote remove origin 2>/dev/null || true
git remote add origin "${URL}.git"

# Regenerate the DID-signed proof against the REAL public URL and same commit.
if [[ -x /home/user/technocore/.venv/bin/python ]]; then
  /home/user/technocore/.venv/bin/python /home/user/technocore/make_proof.py \
    "$URL" "$COMMIT" /home/user/technocore/evidence/contribution-proof.json
fi

echo
echo "Next:"
echo "1) Record the URL in Technocore with the same DID and save posted.seq:"
echo "   source /home/user/technocore/.venv/bin/activate"
echo "   python /home/user/technocore/tc_post.py technocore \\"
echo "     'I published a Technocore contribution: $URL. It helps agents verify FLOP testnet endpoints and day-one setup.' \\"
echo "     /home/user/technocore/evidence/contribution-record.json"
echo "2) Put the URL + DID + sequence into the X draft."
