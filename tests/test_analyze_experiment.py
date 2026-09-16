from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "revealed-demand"
    / "scripts"
    / "analyze_experiment.py"
)
SPEC = importlib.util.spec_from_file_location("analyze_experiment", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class AnalyzeExperimentTests(unittest.TestCase):
    def test_wilson_interval_contains_observed_rate(self) -> None:
        interval = MODULE.wilson_interval(9, 120)
        self.assertLess(interval[0], 9 / 120)
        self.assertGreater(interval[1], 9 / 120)

    def test_summary_computes_retained_and_contribution(self) -> None:
        summary = MODULE.summarize_cell(
            {
                "label": "A",
                "price": 39,
                "exposures": 120,
                "cta_clicks": 38,
                "checkouts": 15,
                "purchases": 9,
                "refunds": 1,
                "revenue": 312,
                "variable_cost": 72,
            },
            0,
        )
        self.assertAlmostEqual(summary.metrics["purchase_rate"], 0.075)
        self.assertAlmostEqual(summary.metrics["net_retained_rate"], 8 / 120)
        self.assertEqual(summary.metrics["contribution"], 240)

    def test_rejects_non_monotonic_funnel(self) -> None:
        with self.assertRaises(MODULE.InputError):
            MODULE.summarize_cell(
                {
                    "label": "Broken",
                    "exposures": 10,
                    "cta_clicks": 11,
                    "purchases": 1,
                },
                0,
            )

    def test_rejects_purchase_count_above_clicks_without_checkout_data(self) -> None:
        with self.assertRaises(MODULE.InputError):
            MODULE.summarize_cell(
                {
                    "label": "Broken",
                    "exposures": 100,
                    "cta_clicks": 4,
                    "purchases": 5,
                },
                0,
            )


if __name__ == "__main__":
    unittest.main()
