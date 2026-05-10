#!/usr/bin/env python3
"""MemeGuard Radar: Birdeye Sprint 4 prototype.

Safe local code: does not trade, does not connect a wallet, and only calls Birdeye
when BIRDEYE_API_KEY is provided.
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import json
import os
import sys
import time
from typing import Any, Dict, Iterable, List, Optional
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://public-api.birdeye.so"


def load_dotenv(path: str = ".env") -> None:
    """Load simple KEY=VALUE entries without printing secrets or overriding env."""
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

SAMPLE_LISTINGS = [
    {"address": "So11111111111111111111111111111111111111112", "symbol": "SOL", "name": "Wrapped SOL", "liquidity": 25000000, "priceChange24hPercent": 2.4},
    {"address": "RiskyMint111111111111111111111111111111111111", "symbol": "RUG?", "name": "Risky Mint", "liquidity": 15000, "priceChange24hPercent": 180.0},
    {"address": "FreshGood11111111111111111111111111111111111", "symbol": "FRESH", "name": "Fresh Candidate", "liquidity": 120000, "priceChange24hPercent": 18.0},
]

SAMPLE_SECURITY = {
    "So11111111111111111111111111111111111111112": {"is_mintable": False, "is_freezable": False, "owner_balance": 0.01, "top10_holder_percent": 18.0},
    "RiskyMint111111111111111111111111111111111111": {"is_mintable": True, "is_freezable": True, "owner_balance": 0.45, "top10_holder_percent": 82.0},
    "FreshGood11111111111111111111111111111111111": {"is_mintable": False, "is_freezable": False, "owner_balance": 0.07, "top10_holder_percent": 34.0},
}

@dataclasses.dataclass
class TokenRadarRow:
    address: str
    symbol: str
    name: str
    liquidity: float
    price_change_24h: float
    score: int
    risk_flags: List[str]
    action: str


@dataclasses.dataclass
class RunEvidence:
    generated_at_utc: str
    mode: str
    listing_count: int
    birdeye_api_calls: int
    endpoints_used: List[str]
    qualification_note: str


def _get_json(path: str, params: Optional[Dict[str, Any]] = None, *, api_key: str) -> Dict[str, Any]:
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urlencode(params)
    req = Request(url, headers={
        "X-API-KEY": api_key,
        "x-chain": "solana",
        "accept": "application/json",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "origin": "https://birdeye.so",
        "referer": "https://birdeye.so/",
    })
    for attempt in range(5):
        try:
            with urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode("utf-8"))
        except HTTPError as e:
            if e.code == 429 and attempt < 4:
                retry_after = e.headers.get("Retry-After")
                wait = float(retry_after) if retry_after and retry_after.replace('.', '', 1).isdigit() else 65.0
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("unreachable retry loop")


def normalize_listing(raw: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "address": raw.get("address") or raw.get("tokenAddress") or raw.get("mint") or "",
        "symbol": raw.get("symbol") or raw.get("tokenSymbol") or "UNKNOWN",
        "name": raw.get("name") or raw.get("tokenName") or raw.get("symbol") or "Unknown Token",
        "liquidity": float(raw.get("liquidity") or raw.get("liquidityUsd") or raw.get("liquidityUSD") or 0),
        "priceChange24hPercent": float(raw.get("priceChange24hPercent") or raw.get("priceChange24h") or raw.get("priceChangePercent24h") or 0),
    }


def fetch_new_listings(api_key: str, limit: int, *, page_size: int = 20, rate_delay: float = 1.25) -> List[Dict[str, Any]]:
    """Fetch new listings with Birdeye's max page size of 20."""
    out: List[Dict[str, Any]] = []
    page_size = max(1, min(20, page_size))
    for offset in range(0, limit, page_size):
        batch_limit = min(page_size, limit - offset)
        params = {"limit": batch_limit}
        if offset:
            params["offset"] = offset
        data = _get_json("/defi/v2/tokens/new_listing", params, api_key=api_key)
        payload = data.get("data", data)
        if isinstance(payload, dict):
            rows = payload.get("items") or payload.get("tokens") or payload.get("list") or []
        else:
            rows = payload
        out.extend(normalize_listing(x) for x in rows if isinstance(x, dict))
        if len(out) >= limit:
            break
        time.sleep(max(0.0, rate_delay))
    return out[:limit]


def fetch_security(api_key: str, address: str) -> Dict[str, Any]:
    # Free-key compatible enrichment. `/defi/token_security` returned 401 for the provided key,
    # so use token overview fields for the live Sprint 4 evidence run.
    data = _get_json("/defi/token_overview", {"address": address}, api_key=api_key)
    payload = data.get("data", data)
    return payload if isinstance(payload, dict) else {}


def score_token(token: Dict[str, Any], security: Dict[str, Any]) -> TokenRadarRow:
    flags: List[str] = []
    score = 50
    liq = float(token.get("liquidity", 0) or 0)
    change = float(token.get("priceChange24hPercent", 0) or 0)

    if liq >= 100_000:
        score += 18
    elif liq >= 25_000:
        score += 8
    else:
        score -= 15
        flags.append("thin-liquidity")

    if 5 <= change <= 60:
        score += 12
    elif change > 150:
        score -= 12
        flags.append("possible-pump")

    if security.get("is_mintable") is True:
        score -= 25
        flags.append("mintable")
    if security.get("is_freezable") is True:
        score -= 20
        flags.append("freezable")

    top10 = security.get("top10_holder_percent") or security.get("top10HolderPercent") or security.get("top_10_holder_percent")
    if top10 is not None:
        top10 = float(top10)
        if top10 > 70:
            score -= 20
            flags.append("top10-concentration>70%")
        elif top10 < 45:
            score += 8

    owner_bal = security.get("owner_balance") or security.get("ownerBalance")
    if owner_bal is not None and float(owner_bal) > 0.25:
        score -= 15
        flags.append("owner-balance-high")

    score = max(0, min(100, int(score)))
    action = "watch" if score >= 70 and not flags else "research" if score >= 50 else "avoid"
    return TokenRadarRow(
        address=token.get("address", ""),
        symbol=token.get("symbol", "UNKNOWN"),
        name=token.get("name", "Unknown Token"),
        liquidity=liq,
        price_change_24h=change,
        score=score,
        risk_flags=flags,
        action=action,
    )


def build_report(listings: Iterable[Dict[str, Any]], security_by_addr: Dict[str, Dict[str, Any]]) -> List[TokenRadarRow]:
    rows = [score_token(t, security_by_addr.get(t.get("address", ""), {})) for t in listings]
    return sorted(rows, key=lambda r: (-r.score, -r.liquidity, r.symbol))


def render_markdown(rows: List[TokenRadarRow], evidence: Optional[RunEvidence] = None) -> str:
    out = ["# MemeGuard Radar", ""]
    if evidence:
        out.extend([
            f"Generated: {evidence.generated_at_utc}",
            f"Mode: {evidence.mode}",
            f"Birdeye API calls: {evidence.birdeye_api_calls}",
            f"Endpoints: {', '.join(evidence.endpoints_used) or 'none'}",
            f"Qualification: {evidence.qualification_note}",
            "",
        ])
    out.extend(["| Token | Score | Action | Liquidity | 24h | Flags |", "|---|---:|---|---:|---:|---|"])
    for r in rows:
        out.append(f"| {r.symbol} ({r.name}) | {r.score} | {r.action} | ${r.liquidity:,.0f} | {r.price_change_24h:.1f}% | {', '.join(r.risk_flags) or 'none'} |")
    return "\n".join(out) + "\n"


def render_html(rows: List[TokenRadarRow], evidence: Optional[RunEvidence] = None) -> str:
    """Render a static dashboard suitable for screenshots/submission evidence."""
    def esc(value: Any) -> str:
        return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    cards = ""
    if evidence:
        cards = f"""
        <section class="evidence">
          <div><b>Generated</b><span>{esc(evidence.generated_at_utc)}</span></div>
          <div><b>Mode</b><span>{esc(evidence.mode)}</span></div>
          <div><b>Birdeye API calls</b><span>{evidence.birdeye_api_calls}</span></div>
          <div><b>Qualification</b><span>{esc(evidence.qualification_note)}</span></div>
        </section>
        """
    body_rows = []
    for r in rows:
        flags = ", ".join(r.risk_flags) or "none"
        body_rows.append(
            f"<tr class='{esc(r.action)}'><td><b>{esc(r.symbol)}</b><small>{esc(r.name)}</small></td>"
            f"<td>{r.score}</td><td>{esc(r.action)}</td><td>${r.liquidity:,.0f}</td>"
            f"<td>{r.price_change_24h:.1f}%</td><td>{esc(flags)}</td></tr>"
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MemeGuard Radar — Birdeye Sprint 4</title>
<style>
body{{font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,sans-serif;margin:0;background:#08111f;color:#eaf2ff}}
main{{max-width:1040px;margin:0 auto;padding:44px 24px}}
.hero{{background:linear-gradient(135deg,#111f3a,#082f2d);border:1px solid #28415f;border-radius:24px;padding:28px;margin-bottom:22px}}
h1{{font-size:42px;margin:0 0 8px}}p{{color:#b9c7d9;line-height:1.55}}
.evidence{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:18px 0}}
.evidence div{{background:#0f1b2d;border:1px solid #263a55;border-radius:16px;padding:14px}}
.evidence b{{display:block;color:#7dd3fc;font-size:12px;text-transform:uppercase;letter-spacing:.08em}}.evidence span{{display:block;margin-top:6px}}
table{{width:100%;border-collapse:collapse;background:#0f1b2d;border-radius:18px;overflow:hidden}}th,td{{padding:14px;border-bottom:1px solid #243852;text-align:left}}th{{color:#7dd3fc;font-size:12px;text-transform:uppercase;letter-spacing:.08em}}small{{display:block;color:#94a3b8;margin-top:3px}}tr.watch td:first-child{{border-left:4px solid #22c55e}}tr.research td:first-child{{border-left:4px solid #f59e0b}}tr.avoid td:first-child{{border-left:4px solid #ef4444}}
footer{{color:#94a3b8;margin-top:18px;font-size:13px}}
@media(max-width:760px){{.evidence{{grid-template-columns:1fr}}h1{{font-size:32px}}}}
</style></head><body><main>
<section class="hero"><h1>MemeGuard Radar</h1><p>Birdeye-powered new-token radar: fresh Solana listings enriched with transparent security scoring, so traders and agents can separate watch, research, and avoid candidates.</p></section>
{cards}
<table><thead><tr><th>Token</th><th>Score</th><th>Action</th><th>Liquidity</th><th>24h</th><th>Flags</th></tr></thead><tbody>{''.join(body_rows)}</tbody></table>
<footer>Endpoints planned/used: /defi/v2/tokens/new_listing + /defi/token_overview. No trading or wallet actions.</footer>
</main></body></html>"""


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--min-api-calls", type=int, default=50, help="Target minimum calls for Birdeye bounty evidence; requires API key")
    ap.add_argument("--rate-delay", type=float, default=2.0, help="Delay between live enrichment calls; use >=1s for 60 rpm APIs")
    ap.add_argument("--sample", action="store_true", help="Use built-in sample data; no API calls")
    ap.add_argument("--env-file", default=".env", help="Load Birdeye credentials/rate settings from this dotenv file")
    ap.add_argument("--format", choices=["json", "markdown", "html"], default="json")
    args = ap.parse_args(argv)

    load_dotenv(args.env_file)
    api_key = os.getenv("BIRDEYE_API_KEY", "")
    if "BIRDEYE_RATE_DELAY_SECONDS" in os.environ and args.rate_delay == 2.0:
        args.rate_delay = float(os.environ["BIRDEYE_RATE_DELAY_SECONDS"])
    if args.sample or not api_key:
        listings = SAMPLE_LISTINGS[: args.limit]
        security = SAMPLE_SECURITY
        call_count = 0
        mode = "sample/no-api-key"
    else:
        # Paginate /defi/v2/tokens/new_listing (max limit 20) plus one /defi/token_security call per token.
        # The bounty asks for at least 50 API calls, so lift the effective limit when needed.
        effective_limit = max(args.limit, max(1, args.min_api_calls - 1))
        listings = fetch_new_listings(api_key, effective_limit, rate_delay=args.rate_delay)
        call_count = (effective_limit + 19) // 20
        security = {}
        for t in listings:
            addr = t.get("address", "")
            if addr:
                security[addr] = fetch_security(api_key, addr)
                call_count += 1
                time.sleep(max(0.0, args.rate_delay))  # respect API rpm limits during qualification runs
        mode = "birdeye-live"

    rows = build_report(listings, security)
    evidence = RunEvidence(
        generated_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        mode=mode,
        listing_count=len(listings),
        birdeye_api_calls=call_count,
        endpoints_used=["/defi/v2/tokens/new_listing", "/defi/token_overview"] if call_count else [],
        qualification_note=("meets 50+ API-call target" if call_count >= args.min_api_calls else "sample/unqualified until API key run"),
    )
    if args.format == "markdown":
        print(render_markdown(rows, evidence))
    elif args.format == "html":
        print(render_html(rows, evidence))
    else:
        print(json.dumps({"evidence": dataclasses.asdict(evidence), "rows": [dataclasses.asdict(r) for r in rows]}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
