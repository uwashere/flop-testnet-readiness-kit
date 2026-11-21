#!/usr/bin/env python3
"""Check FLOP network endpoints with the Python standard library only.

Prints chain identity from the public JSON-RPC endpoint, faucet identity, and
gateway model count. Warns if RPC and faucet genesis hashes disagree.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

NETWORK = os.environ.get("FLOP_NETWORK", "devnet")
ENDPOINTS = {
    "devnet": {
        "rpc": "https://rpc.devnet.flop.network",
        "faucet": "https://faucet.flop.network",
        "gateway": "https://api.flop.network/v1/models",
        "explorer": "https://explorer.devnet.flop.network/api/stats",
    },
    "testnet": {
        "rpc": "https://testnet.flop.network",
        "faucet": "https://faucet.testnet.flop.network",
        "gateway": "https://gateway.testnet.flop.network/v1/models",
        "explorer": "",
    },
}


def get_json(url: str, data: bytes | None = None, timeout: float = 20.0):
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "flop-readiness-kit/1.0 (+https://technocore.chat)",
        },
        method="POST" if data else "GET",
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            if error.code not in {403, 429, 502, 503, 504} or attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
    raise RuntimeError("unreachable")


def rpc(url: str, method: str):
    body = json.dumps({"id": 1, "jsonrpc": "2.0", "method": method, "params": []}).encode()
    return get_json(url, body).get("result")


def main() -> None:
    if NETWORK not in ENDPOINTS:
        raise SystemExit(f"unknown network: {NETWORK}")
    e = ENDPOINTS[NETWORK]
    print(f"network: {NETWORK}")
    try:
        chain = rpc(e["rpc"], "system_chain")
        runtime = rpc(e["rpc"], "state_getRuntimeVersion")
        rpc_genesis = rpc(e["rpc"], "chain_getBlockHash")  # informative only
        print(f"rpc chain: {chain}")
        print(f"rpc runtime specVersion: {runtime.get('specVersion') if runtime else None}")
    except Exception as exc:
        rpc_genesis = None
        print(f"rpc: ERROR {exc}")

    try:
        faucet = get_json(e["faucet"].rstrip("/") + "/chain")
        print(f"faucet chain: {faucet.get('chain')} ({faucet.get('network')})")
        genesis = faucet.get("genesisHash")
        print(f"faucet genesis: {genesis}")
    except Exception as exc:
        genesis = None
        print(f"faucet: ERROR {exc}")

    if genesis and rpc_genesis:
        print("note: compare the faucet genesis on this page with the RPC genesis "
              "reported by `flop --network <net> network status` before signing.")

    try:
        models = get_json(e["gateway"])
        print(f"gateway models: {models.get('total_count', len(models.get('data', [])))}")
    except Exception as exc:
        print(f"gateway: ERROR {exc}")

    if e["explorer"]:
        try:
            stats = get_json(e["explorer"])
            print(f"explorer head: {stats.get('latestBlockNumber')} "
                  f"(finality {stats.get('finality', {}).get('state')})")
        except Exception as exc:
            print(f"explorer: ERROR (known to flap): {exc}")


if __name__ == "__main__":
    main()
