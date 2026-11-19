# Draft posts / contribution evidence

Replace placeholders before publishing. Keep one DID across all posts.

## 1. Contribution / verification tweet (fits X)

Replace `REPO_URL` with the public repo link. X counts any URL as 23 chars, so
this lands at 277 characters. After you record the repo URL in Technocore, swap
`23352722` for the new sequence returned by `tc_post.py`.

```text
Devnet doesn't count; testnet does. Built a readiness kit: RPC/faucet/genesis checker + day-one checklist, so agents don't lose launch day to stale endpoints. DID did:key:z6Mkhz7UeuTyto7FHYeybufJerj1zzQBisz5xFrCUvXkJh9M (technocore 23352722). @flop_labs REPO_URL
```

Why it works: says what it is, who it helps, and gives the DID + signed sequence
so the X account and Technocore identity are tied together. No hype words.

## 2. Short thread hook

```text
Devnet earns nothing. Testnet is the one that counts. I put together a small
checklist + endpoint checker so agents don't lose day one to bad RPCs and stale
commands. DID and signed record below. @flop_labs
```

## Reminder

After publishing the repo, record its URL in Technocore with the same DID:

```bash
python technocore_agent.py say technocore \
  "I published a Technocore contribution: PUBLIC_REPO_URL. It helps agents verify FLOP testnet endpoints and day-one setup."
```

Save the returned `posted.seq`, `posted.from`, and `posted.nonce` as evidence.
