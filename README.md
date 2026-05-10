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

## Current autonomous status

- ✅ Public rules reviewed from the Superteam listing.
- ✅ Prototype logic and tests prepared locally.
- ✅ No wallet, paid resource, cloud deployment, or platform submission performed.
- ⛔ Blocked for real qualification by Birdeye API key/login and Superteam final submission. The listing says builders must create a free account at `bds.birdeye.so`, use an API key, make at least 50 API calls, post progress on X tagging `@birdeye_data` with `#BirdeyeAPI`, then submit via Superteam Earn.

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

## Submission assets to fill after real API run

- Project name: MemeGuard Radar
- GitHub link: pending repo/push authorization
- X progress post/thread: pending public posting authorization
- Endpoints used: `/defi/v2/tokens/new_listing`, `/defi/token_overview`; optional `/defi/token_security` if the API key has that permission
- Evidence: include CLI output, report screenshot, and note that 50+ Birdeye calls were made

