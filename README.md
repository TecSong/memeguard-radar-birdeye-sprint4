# MemeGuard Radar — Birdeye Sprint 4

Local-first prototype for **Birdeye Data 4-Week BIP Competition — Sprint 4**.

MemeGuard Radar uses Birdeye Data to turn fresh Solana token listings into an auditable watch/research/avoid queue. It is intentionally non-custodial: no wallet, no trading, no orders, and no private keys.

Goal: a small, shippable onchain radar that uses Birdeye Data endpoints to identify newly listed Solana tokens worth investigating, while filtering obvious risk signals before they reach a trader or agent.

Bounty: https://earn.superteam.fun/listing/birdeye-data-4-week-bip-competition-sprint-4

## Why this fits the brief

Sprint 4 starter ideas explicitly suggest a **new token radar with safety scoring** using:

- `/defi/v2/tokens/new_listing`
- `/defi/token_overview` for free-key live enrichment
- `/defi/token_security` is noted as an optional security endpoint when the key has permission

This draft keeps scope small and judgeable:

1. pull new listings;
2. enrich each token with security fields;
3. compute a transparent safety/momentum score;
4. output Markdown/JSON suitable for a dashboard, Telegram bot, or X build-in-public post.

## Current status

- ✅ Public rules reviewed from the Superteam listing.
- ✅ Prototype logic, static dashboard, Markdown/JSON reports, and tests are in the repo.
- ✅ Live evidence run completed with **52 Birdeye API calls**: 3 paginated `/defi/v2/tokens/new_listing` calls + 49 `/defi/token_overview` enrichment calls.
- ✅ Build-in-public X post: https://x.com/Yiko55524775/status/2053308934988189904
- ✅ Superteam submission recorded as pending review: `efe8a8bd-d516-44c2-919e-2731605132d1`.
- ℹ️ No wallet, paid resource, cloud deployment, trading, or custodial action is used by this project.

## Quick start

```bash
cd /root/.hermes/state/bounty-assets/birdeye-sprint4-2026-05-09
python3 -m unittest -v test_memeguard.py
python3 memeguard_radar.py --sample --format markdown > sample_report.md
python3 memeguard_radar.py --sample --format json > sample_report.json
python3 memeguard_radar.py --sample --format html > sample_dashboard.html

# With Birdeye key after Yiko logs in/authorizes API use.
# This automatically lifts the effective limit to target 50+ qualifying API calls
# (1 new_listing call + token_security calls per returned token).
export BIRDEYE_API_KEY=...
python3 memeguard_radar.py --limit 25 --min-api-calls 50 --format markdown > report.md
python3 memeguard_radar.py --limit 25 --min-api-calls 50 --format json > report.json
python3 memeguard_radar.py --limit 25 --min-api-calls 50 --format html > dashboard.html
```

## Submission artifacts

- Project name: MemeGuard Radar
- GitHub link: https://github.com/TecSong/memeguard-radar-birdeye-sprint4
- X progress post/thread: https://x.com/Yiko55524775/status/2053308934988189904
- Live evidence files: `live_report.md`, `live_report.json`, `live_dashboard.html`
- Superteam submission id: `efe8a8bd-d516-44c2-919e-2731605132d1`
- Status: pending review

