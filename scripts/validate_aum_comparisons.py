#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPARISON_PATH = ROOT / "data/website/aum-comparisons.json"


def main() -> int:
    payload = json.loads(COMPARISON_PATH.read_text(encoding="utf-8"))
    rates = payload["fxReference"]["ratesPerEur"]

    for record in payload["records"]:
        rate = rates[record["currency"]]
        expected = round(record["valueNative"] / rate / 1_000_000)
        actual = record["valueMioEur"]
        if actual != expected:
            raise SystemExit(
                f"{record['id']} valueMioEur mismatch: {actual} != {expected}"
            )

    blackrock = next(record for record in payload["records"] if record["id"] == "blackrock")
    if "Kundengeld" not in blackrock["interpretationNote"] and "Kunden" not in blackrock["interpretationNote"]:
        raise SystemExit("BlackRock comparison must be framed as managed client assets.")

    print("aum comparison values ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
