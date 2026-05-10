# Birdeye Sprint 4 live API progress — 2026-05-10

## Credential handling
- User authorized writing the Birdeye API key to local `.env`.
- `.env` permissions set to `600`.
- `.gitignore` excludes `.env` and live report artifacts from accidental commit.
- The key is not printed in generated reports.

## Fixes made
- Added `.env` loader to `memeguard_radar.py`.
- Corrected new-listing endpoint from `/v2/tokens/new_listing` to `/defi/v2/tokens/new_listing`.
- Added Birdeye pagination because new-listing limit must be `1-20`.
- Added browser-like headers for Cloudflare compatibility.
- Added 429 retry/backoff.
- Switched live enrichment from `/defi/token_security` to `/defi/token_overview` because the provided free key returned `401 insufficient permissions` for token security.
- Updated README, Superteam submission draft, and X progress draft to reflect actual endpoints.

## Live evidence run
- Mode: `birdeye-live`
- Rows: 49 tokens
- Birdeye API calls: 52
- Qualification: meets 50+ API-call target
- Endpoints used:
  - `/defi/v2/tokens/new_listing`
  - `/defi/token_overview`

## Artifacts
- `live_report.json`
- `live_report.md`
- `live_dashboard.html`
- Existing sample artifacts remain:
  - `sample_report.json`
  - `sample_report.md`
  - `sample_dashboard.html`

## Verification
```text
Ran 4 tests in 0.000s
OK
LIVE_ARTIFACTS_OK 49 52 meets 50+ API-call target
ENDPOINTS /defi/v2/tokens/new_listing, /defi/token_overview
```

## Remaining authorization boundaries
- GitHub repo creation/push.
- Public X build-in-public post/thread.
- Superteam final submission.
- Wallet, payout, KYC, terms, paid/cloud resources.
