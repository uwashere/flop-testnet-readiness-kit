# FLOP Testnet Readiness Kit

A small, dependency-free toolkit and checklist for agents preparing for the FLOP
testnet. Built while preparing an agent for the 24 November 2026 target.

**Technocore DID used for this contribution:** `did:key:z6Mkhz7UeuTyto7FHYeybufJerj1zzQBisz5xFrCUvXkJh9M`

## What is verified (as of 2026-11-19)

- Devnet activity has **no airdrop weight**; testnet is where usage counts.
- Testnet launch is a **target** of 24 Nov 2026, subject to readiness, ~90 days.
- Airdrop is usage-based; draft rules say locked agent airdrop unlocks 1 FLOP for
  every 3 FLOP spent on inference.
- No FLOP token exists. Never buy a "testnet FLOP" token or enter a seed phrase
  on a claim site.

Sources: [official links](https://docs.flop.network/docs/official-links),
[testnet FAQ](https://docs.flop.network/docs/testnet-and-timeline),
[airdrop conversion](https://docs.flop.network/docs/airdrop-and-testnet-conversion).

## Endpoint check

```bash
python3 check_endpoints.py            # devnet
FLOP_NETWORK=testnet python3 check_endpoints.py
```

Uses only the Python standard library. It prints chain identity, faucet identity,
gateway model count, and warns if the RPC/faucet genesis hashes disagree.

## Day-one checklist

1. Confirm the announcement on @flop_labs and the official-links page.
2. Use the **same SS58 key** as devnet — do not mint a new identity.
3. Point tooling at testnet: `--network testnet`.
4. Check `check_endpoints.py` before funding; compare genesis hashes.
5. Claim faucet immediately; re-create agent wallet and capped session key.
6. Do one `session run` the same day with a reachable, opted-in miner endpoint.
7. Keep a consistent daily loop for the full window; archive logs as evidence.

## Repo contents

- `check_endpoints.py` — read-only endpoint/genesis checker
- `day-one.md` — condensed checklist with commands
- `x-posts.md` — draft posts for public evidence trail
- `LICENSE` — MIT

## Caveat

Nothing here guarantees an allocation. Eligibility and rewards remain subject to
rules published by Flop Labs.
