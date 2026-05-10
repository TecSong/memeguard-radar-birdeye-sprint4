# X progress thread draft — needs Yiko public-post authorization

1/ I’m building MemeGuard Radar for the Birdeye Data BIP Sprint 4: a new-token radar that combines fresh listings with transparent security scoring before a token reaches a trader or agent. #BirdeyeAPI @birdeye_data

2/ The core loop is intentionally small: pull `/defi/v2/tokens/new_listing`, enrich each mint with `/defi/token_overview`, score liquidity + 24h momentum + token metadata, then output a watch/research/avoid list.

3/ Why this matters: early token discovery is noisy. A radar should not just say “new” or “trending”; it should explain *why this is safe enough to inspect* and *which risks made it fail*.

4/ Current prototype runs locally with sample data and is ready for a real Birdeye API-key run. Next step is 50+ real API calls, screenshot/report evidence, GitHub repo, and Superteam submission.
