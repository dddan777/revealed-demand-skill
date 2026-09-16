#!/usr/bin/env python3
"""Summarize demand-experiment cells without choosing a winner."""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


COUNT_FIELDS = (
    "exposures",
    "cta_clicks",
    "checkouts",
    "purchases",
    "refunds",
    "repeat_buyers",
)
MONEY_FIELDS = ("price", "revenue", "variable_cost")


class InputError(ValueError):
    """Raised when an experiment file violates the input contract."""


@dataclass(frozen=True)
class CellSummary:
    label: str
    counts: dict[str, int | None]
    price: float | None
    revenue: float | None
    variable_cost: float | None
    metrics: dict[str, float | list[float] | None]
    cautions: list[str]


def _number(value: Any, field: str, label: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InputError(f"{label}: {field} must be a non-negative number")
    if not math.isfinite(float(value)) or value < 0:
        raise InputError(f"{label}: {field} must be a finite non-negative number")
    return float(value)


def _count(value: Any, field: str, label: str) -> int | None:
    number = _number(value, field, label)
    if number is None:
        return None
    if not number.is_integer():
        raise InputError(f"{label}: {field} must be a whole number")
    return int(number)


def _rate(numerator: int | None, denominator: int | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def _ratio(numerator: float | None, denominator: int | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def wilson_interval(successes: int, trials: int, z: float = 1.959963984540054) -> list[float]:
    if trials <= 0:
        raise InputError("Wilson interval requires a positive trial count")
    if successes < 0 or successes > trials:
        raise InputError("Wilson interval successes must be between zero and trials")
    proportion = successes / trials
    z2 = z * z
    denominator = 1 + z2 / trials
    center = (proportion + z2 / (2 * trials)) / denominator
    spread = (
        z
        * math.sqrt(
            (proportion * (1 - proportion) + z2 / (4 * trials)) / trials
        )
        / denominator
    )
    return [max(0.0, center - spread), min(1.0, center + spread)]


def _require_order(
    higher_name: str,
    higher: int | None,
    lower_name: str,
    lower: int | None,
    label: str,
) -> None:
    if higher is not None and lower is not None and lower > higher:
        raise InputError(
            f"{label}: {lower_name} cannot exceed {higher_name} "
            f"({lower} > {higher})"
        )


def summarize_cell(raw: dict[str, Any], index: int) -> CellSummary:
    label = str(raw.get("label") or f"Cell {index + 1}").strip()
    if not label:
        raise InputError(f"Cell {index + 1}: label cannot be blank")

    counts = {field: _count(raw.get(field), field, label) for field in COUNT_FIELDS}
    money = {field: _number(raw.get(field), field, label) for field in MONEY_FIELDS}

    exposures = counts["exposures"]
    clicks = counts["cta_clicks"]
    checkouts = counts["checkouts"]
    purchases = counts["purchases"]
    refunds = counts["refunds"]
    repeats = counts["repeat_buyers"]

    if exposures is None or purchases is None:
        raise InputError(f"{label}: exposures and purchases are required")
    _require_order("exposures", exposures, "cta_clicks", clicks, label)
    _require_order("cta_clicks", clicks, "checkouts", checkouts, label)
    _require_order("checkouts", checkouts, "purchases", purchases, label)
    if clicks is None:
        _require_order("exposures", exposures, "checkouts", checkouts, label)
        _require_order("exposures", exposures, "purchases", purchases, label)
    if checkouts is None and clicks is not None:
        _require_order("cta_clicks", clicks, "purchases", purchases, label)
    if refunds is not None and refunds > purchases:
        raise InputError(f"{label}: refunds cannot exceed purchases")
    if repeats is not None and repeats > purchases:
        raise InputError(f"{label}: repeat_buyers cannot exceed purchases")

    retained = purchases - (refunds or 0)
    revenue = money["revenue"]
    variable_cost = money["variable_cost"]
    contribution = None
    if revenue is not None and variable_cost is not None:
        contribution = revenue - variable_cost

    metrics: dict[str, float | list[float] | None] = {
        "cta_rate": _rate(clicks, exposures),
        "checkout_rate_from_click": _rate(checkouts, clicks),
        "purchase_rate": _rate(purchases, exposures),
        "purchase_rate_wilson_95": wilson_interval(purchases, exposures)
        if exposures > 0
        else None,
        "net_retained_rate": _rate(retained, exposures),
        "net_retained_rate_wilson_95": wilson_interval(retained, exposures)
        if exposures > 0
        else None,
        "refund_rate": _rate(refunds, purchases),
        "repeat_buyer_rate": _rate(repeats, retained),
        "revenue_per_exposure": _ratio(revenue, exposures),
        "contribution": contribution,
        "contribution_per_exposure": _ratio(contribution, exposures),
    }

    cautions: list[str] = []
    if exposures < 100:
        cautions.append("Fewer than 100 exposures; intervals may be wide.")
    interval = metrics["purchase_rate_wilson_95"]
    if isinstance(interval, list) and interval[1] - interval[0] > 0.10:
        cautions.append("Purchase-rate uncertainty spans more than 10 percentage points.")
    if refunds is None:
        cautions.append("Refunds were not supplied; net demand evidence is incomplete.")
    if revenue is None:
        cautions.append("Revenue was not supplied; price-cell economics cannot be compared.")
    if variable_cost is None:
        cautions.append("Variable cost was not supplied; contribution cannot be computed.")

    return CellSummary(
        label=label,
        counts=counts,
        price=money["price"],
        revenue=revenue,
        variable_cost=variable_cost,
        metrics=metrics,
        cautions=cautions,
    )


def summarize_document(document: dict[str, Any]) -> dict[str, Any]:
    cells = document.get("cells")
    if not isinstance(cells, list) or not cells:
        raise InputError("The top-level cells field must be a non-empty array")
    if not all(isinstance(cell, dict) for cell in cells):
        raise InputError("Every cells entry must be an object")
    summaries = [summarize_cell(cell, index) for index, cell in enumerate(cells)]
    return {
        "title": str(document.get("title") or "Demand experiment"),
        "cells": [asdict(summary) for summary in summaries],
        "interpretation_boundary": (
            "These descriptive metrics do not prove causality or identify an automatic winner. "
            "Compare cohorts only when offer, audience, channel, timing, and assignment are compatible."
        ),
    }


def _percent(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.1f}%"


def _money(value: float | None) -> str:
    return "—" if value is None else f"{value:.2f}"


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        f"# {summary['title']}",
        "",
        "| Cell | Price | Exposures | Purchases | Purchase rate | 95% interval | "
        "Refund rate | Net retained rate | Revenue / exposure | Contribution / exposure |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for cell in summary["cells"]:
        metrics = cell["metrics"]
        interval = metrics["purchase_rate_wilson_95"]
        interval_text = (
            "—"
            if interval is None
            else f"{_percent(interval[0])}–{_percent(interval[1])}"
        )
        lines.append(
            "| {label} | {price} | {exposures} | {purchases} | {purchase_rate} | "
            "{interval} | {refund_rate} | {net_rate} | {rpe} | {cpe} |".format(
                label=cell["label"],
                price=_money(cell["price"]),
                exposures=cell["counts"]["exposures"],
                purchases=cell["counts"]["purchases"],
                purchase_rate=_percent(metrics["purchase_rate"]),
                interval=interval_text,
                refund_rate=_percent(metrics["refund_rate"]),
                net_rate=_percent(metrics["net_retained_rate"]),
                rpe=_money(metrics["revenue_per_exposure"]),
                cpe=_money(metrics["contribution_per_exposure"]),
            )
        )

    lines.extend(["", "## Cautions", ""])
    for cell in summary["cells"]:
        if cell["cautions"]:
            for caution in cell["cautions"]:
                lines.append(f"- {cell['label']}: {caution}")
        else:
            lines.append(f"- {cell['label']}: No automatic data-quality caution was triggered.")
    lines.extend(["", f"Boundary: {summary['interpretation_boundary']}", ""])
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize demand-experiment cells without declaring a winner."
    )
    parser.add_argument("input", type=Path, help="Path to an experiment JSON file")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        document = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise InputError("The top-level JSON value must be an object")
        summary = summarize_document(document)
    except (OSError, json.JSONDecodeError, InputError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
