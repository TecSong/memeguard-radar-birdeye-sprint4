# Superteam submission answer — Birdeye endpoints used

MemeGuard Radar uses Birdeye Data as a small, auditable Solana new-token radar.

Live run evidence:
- 52 real Birdeye API calls
- 49 token rows generated
- Mode: `birdeye-live`
- Qualification: `meets 50+ API-call target`

Endpoints used in the live run:
1. `/defi/v2/tokens/new_listing` — fetched fresh Solana token listings with pagination because this endpoint caps `limit` at 20.
2. `/defi/token_overview` — enriched each token with available metadata/market fields under the provided free API key.

Implementation note:
- The original prototype considered `/defi/token_security`, but the provided free key returned `401 insufficient permissions` for that endpoint, so the live evidence run uses `/defi/token_overview` instead of claiming unsupported security data.
- The scoring model is transparent and non-custodial: it never trades, connects a wallet, or signs transactions.

Artifacts in this repo:
- `memeguard_radar.py` — CLI prototype
- `live_report.json` — machine-readable live run evidence
- `live_report.md` — human-readable live report
- `live_dashboard.html` — static dashboard for screenshot/demo
- `test_memeguard.py` — unit tests
