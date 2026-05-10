# Superteam submission draft — Birdeye Sprint 4

Project name: MemeGuard Radar

Brief description:
MemeGuard Radar is a small Solana new-token discovery tool powered by Birdeye Data. It pulls fresh listings, enriches tokens with security metadata, and produces a transparent watch/research/avoid score so builders and agents can focus on early opportunities without ignoring mint/freeze/holder concentration risks.

Birdeye endpoints used:
- `/defi/v2/tokens/new_listing`
- `/defi/token_overview`

Permission note: the provided free key returned `401 insufficient permissions` for `/defi/token_security`, so the live evidence run uses `/defi/token_overview` enrichment. Security endpoint can be added if the key is upgraded/enabled.

GitHub link: https://github.com/TecSong/memeguard-radar-birdeye-sprint4
X post link: TODO after public posting authorization
Demo/report: TODO after real API-key run with 50+ calls. Local sample artifacts already exist: `sample_report.md`, `sample_report.json`, `sample_dashboard.html`.

Public listing checks:
- Region: Global
- Agent access: AGENT_ALLOWED
- Reward: 500 USDC + API credits for Sprint 4
- Deadline: 2026-05-16 16:59:59 UTC
- Superteam asks for GitHub repo link (optional) and a required brief description of Birdeye Data endpoints used.

Notes for submission paragraph:
This project targets the Sprint 4 starter idea “New token radar with safety scoring.” It emphasizes Product Utility and Technical Depth through an auditable scoring model rather than a black-box signal.
