# Testnet day-one (condensed)

Assumes the official CLI 0.5.0+ with Node 22 and an existing encrypted key.

```bash
# 0. Verify announcement + endpoints BEFORE signing
python3 check_endpoints.py

# 1. Same key, testnet profile
export FLOP_PASS='...'   # from your offline backup, never typed into a site
flop --network testnet network status --json
flop --network testnet health --json

# 2. Fund immediately (day-one claims + verified tier if available)
flop --network testnet faucet request <your-ss58> --json

# 3. Recreate caps on testnet
flop --network testnet --keystore agent.json --password-env FLOP_PASS \
  agent wallet create <agent-ss58> --daily-cap 15 --tx-limit 1 --json
flop --network testnet --keystore agent.json --password-env FLOP_PASS \
  session create --delegate <delegate-ss58> --daily-cap 15 --tx-limit 1 --ttl 86400 --json

# 4. First settled inference same day — use a live opted-in HTTPS endpoint
flop --network testnet --keystore agent.json --password-env FLOP_PASS \
  session run --miner <miner-ss58> --model <slug-from-model-list> \
  --prompt "Day one heartbeat." --max-flop 0.01 --max-tokens 64 \
  --via auto --endpoint https://<miner-endpoint> --json
```

Then repeat one small, verifiable action daily for the whole window. Consistency
and early participation matter more than bursts; no published leaderboard rules
exist, so treat "top active" as a goal, not a guarantee.
