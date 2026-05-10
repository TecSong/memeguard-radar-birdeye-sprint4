import unittest
from memeguard_radar import SAMPLE_LISTINGS, SAMPLE_SECURITY, RunEvidence, build_report, normalize_listing, render_html, score_token

class MemeGuardTests(unittest.TestCase):
    def test_normalize_listing_variants(self):
        row = normalize_listing({"tokenAddress":"abc", "tokenSymbol":"ABC", "tokenName":"Alpha", "liquidityUSD":"42", "priceChange24h":"7"})
        self.assertEqual(row["address"], "abc")
        self.assertEqual(row["symbol"], "ABC")
        self.assertEqual(row["liquidity"], 42.0)
        self.assertEqual(row["priceChange24hPercent"], 7.0)

    def test_risky_token_is_downgraded(self):
        token = SAMPLE_LISTINGS[1]
        row = score_token(token, SAMPLE_SECURITY[token["address"]])
        self.assertEqual(row.action, "avoid")
        self.assertIn("mintable", row.risk_flags)
        self.assertIn("freezable", row.risk_flags)

    def test_report_sorted_by_score(self):
        rows = build_report(SAMPLE_LISTINGS, SAMPLE_SECURITY)
        scores = [r.score for r in rows]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertEqual(rows[0].action, "watch")

    def test_html_dashboard_contains_evidence_and_actions(self):
        rows = build_report(SAMPLE_LISTINGS, SAMPLE_SECURITY)
        evidence = RunEvidence("2026-05-10T00:00:00+00:00", "sample/no-api-key", len(rows), 0, [], "sample/unqualified until API key run")
        html = render_html(rows, evidence)
        self.assertIn("MemeGuard Radar", html)
        self.assertIn("Birdeye API calls", html)
        self.assertIn("sample/unqualified", html)
        self.assertIn("watch", html)
        self.assertIn("avoid", html)

if __name__ == "__main__":
    unittest.main()
