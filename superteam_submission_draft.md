# Superteam submission draft — Birdeye Sprint 4

Project name: MemeGuard Radar

Brief description:
MemeGuard Radar is a small Solana new-token discovery tool powered by Birdeye Data. It pulls fresh listings, enriches each token with available market metadata, and produces a transparent watch/research/avoid score so builders and agents can filter early-token noise before spending time on a new mint.

Birdeye endpoints used:
- `/defi/v2/tokens/new_listing`
- `/defi/token_overview`

Permission note: the provided free key returned `401 insufficient permissions` for `/defi/token_security`, so the live evidence run uses `/defi/token_overview` enrichment. Security endpoint can be added if the key is upgraded/enabled.

GitHub link: https://github.com/TecSong/memeguard-radar-birdeye-sprint4
X post link: https://x.com/Yiko55524775/status/2053308934988189904
Demo/report: live evidence artifacts exist in the repo: `live_report.md`, `live_report.json`, and `live_dashboard.html` from a 52-call Birdeye run.

Public listing checks:
- Region: Global
- Agent access: AGENT_ALLOWED
- Reward: 500 USDC + API credits for Sprint 4
- Deadline: 2026-05-16 16:59:59 UTC
- Superteam asks for GitHub repo link (optional) and a required brief description of Birdeye Data endpoints used.

Notes for submission paragraph:
This project targets the Sprint 4 starter idea “New token radar with safety scoring.” It emphasizes Product Utility and Technical Depth through an auditable scoring model rather than a black-box signal.
