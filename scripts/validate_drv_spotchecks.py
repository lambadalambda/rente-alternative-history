#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXTRACTED_CSV = ROOT / "data/extracted/drv/allgemeine-rv-cashflows.csv"
WEBSITE_JSON = ROOT / "data/website/allgemeine-rv-cashflows.json"
SPOTCHECKS_JSON = ROOT / "data/quality/drv/allgemeine-rv-cashflow-spotchecks.json"
SOURCE_SHA256 = "f41ad3a1c398ac56ad5ac75898ba5c664aa1ef7e6ad98859cb2a622b6293ee07"

VARIABLE_TO_COLUMN = {
    "contributionsMioEur": "contributions_mio_eur",
    "pensionOutlaysMioEur": "pension_outlays_mio_eur",
}

VARIABLE_PROVENANCE = {
    "contributionsMioEur": ("Einnahmen allg. RV", 244, 246),
    "pensionOutlaysMioEur": ("Ausgaben allg. RV", 245, 247),
}


def load_extracted_rows() -> dict[tuple[int, str], dict[str, str]]:
    with EXTRACTED_CSV.open(newline="", encoding="utf-8") as handle:
        return {
            (int(row["year"]), row["scope"]): row
            for row in csv.DictReader(handle)
        }


def load_website_rows() -> dict[tuple[int, str], dict[str, object]]:
    payload = json.loads(WEBSITE_JSON.read_text(encoding="utf-8"))
    return {
        (int(row["year"]), row["scope"]): row
        for row in payload["records"]
    }


def format_pdf_number(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def main() -> int:
    extracted = load_extracted_rows()
    website = load_website_rows()
    spotchecks = json.loads(SPOTCHECKS_JSON.read_text(encoding="utf-8"))

    if spotchecks["sourceSha256"] != SOURCE_SHA256:
        raise SystemExit("Spot-check source SHA-256 does not match pinned DRV source.")

    for check in spotchecks["checks"]:
        if check.get("result") != "ok":
            raise SystemExit(f"Spot check {check['id']} is not marked ok.")

        expected_table, expected_content_page, expected_pdf_page = VARIABLE_PROVENANCE[check["variable"]]
        if (
            check["sourceTable"] != expected_table
            or check["contentPage"] != expected_content_page
            or check["pdfPage"] != expected_pdf_page
        ):
            raise SystemExit(f"Spot check {check['id']} has inconsistent provenance fields.")

        expected = int(check["expectedMioEur"])
        if format_pdf_number(expected) not in check["pdfRowExcerpt"]:
            raise SystemExit(f"Spot check {check['id']} row excerpt does not contain expected value.")

        key = (check["year"], check["scope"])
        row = extracted.get(key)
        if row is None:
            raise SystemExit(f"Missing extracted row for spot check {check['id']}: {key}")

        website_row = website.get(key)
        if website_row is None:
            raise SystemExit(f"Missing website row for spot check {check['id']}: {key}")

        column = VARIABLE_TO_COLUMN[check["variable"]]
        actual = int(row[column])
        if actual != expected:
            raise SystemExit(
                f"Spot check {check['id']} failed: extracted CSV {actual} != expected {expected}"
            )

        website_actual = int(website_row[check["variable"]])
        if website_actual != expected:
            raise SystemExit(
                f"Spot check {check['id']} failed: website JSON {website_actual} != expected {expected}"
            )

    print(f"drv spotchecks ok ({len(spotchecks['checks'])} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
