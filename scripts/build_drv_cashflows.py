#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SOURCE_URL = "https://www.deutsche-rentenversicherung.de/SharedDocs/Downloads/DE/Statistiken-und-Berichte/statistikpublikationen/rv_in_zeitreihen.pdf?__blob=publicationFile&v=9"
LANDING_PAGE = "https://www.deutsche-rentenversicherung.de/SharedDocs/Downloads/DE/Statistiken-und-Berichte/statistikpublikationen/rv_in_zeitreihen.html"
SOURCE_SHA256 = "f41ad3a1c398ac56ad5ac75898ba5c664aa1ef7e6ad98859cb2a622b6293ee07"
CORRECTIONS_URL = "https://www.deutsche-rentenversicherung.de/SharedDocs/Downloads/DE/Statistiken-und-Berichte/statistikpublikationen/rv_in_zeitreihen_korrekturseiten.pdf?__blob=publicationFile&v=3"
CORRECTIONS_LANDING_PAGE = "https://www.deutsche-rentenversicherung.de/SharedDocs/Downloads/DE/Statistiken-und-Berichte/statistikpublikationen/rv_in_zeitreihen_korrekturseiten.html"

DEFAULT_SOURCE_PDF = ROOT / "data/raw/drv/rv_in_zeitreihen_2025.pdf"
EXTRACTED_CSV = ROOT / "data/extracted/drv/allgemeine-rv-cashflows.csv"
WEBSITE_JSON = ROOT / "data/website/allgemeine-rv-cashflows.json"

PDF_FIRST_PAGE = 246
PDF_LAST_PAGE = 247
EXPECTED_YEARS = [1960, 1965, 1970, 1975, 1980, 1985, 1990, 1991, *range(1995, 2025)]
SENTINELS = {
    1960: ("Alte Bundesländer", 6894, 7286),
    1991: ("Insgesamt", 106822, 108942),
    2004: ("Insgesamt", 168378, 197450),
    2024: ("Insgesamt", 305336, 344351),
}

NUMBER_TOKEN = re.compile(r"-\s*\d{1,3}(?:\.\d{3})*|-\s*\d+|\d{1,3}(?:\.\d{3})*|\d+|x|-")
ROW_START = re.compile(r"^\s*(\d{4})\s+(.*)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build allg. RV cashflow website data from the DRV Zeitreihen PDF."
    )
    parser.add_argument(
        "--source-pdf",
        type=Path,
        default=DEFAULT_SOURCE_PDF,
        help=f"Path to the DRV PDF. Default: {DEFAULT_SOURCE_PDF.relative_to(ROOT)}",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Fail instead of downloading the source PDF when it is missing.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify generated files are up to date without writing outputs. Also avoids PDF download by default.",
    )
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_source_pdf(path: Path, allow_download: bool) -> None:
    if not path.exists():
        if not allow_download:
            raise SystemExit(f"Missing source PDF: {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = path.with_suffix(path.suffix + ".download")
        with urllib.request.urlopen(SOURCE_URL, timeout=120) as response, temporary_path.open("wb") as target:
            shutil.copyfileobj(response, target)

        downloaded_hash = sha256(temporary_path)
        if downloaded_hash != SOURCE_SHA256:
            temporary_path.unlink(missing_ok=True)
            raise SystemExit(
                f"Unexpected SHA-256 for downloaded source: {downloaded_hash}. Expected {SOURCE_SHA256}."
            )
        temporary_path.replace(path)

    actual_hash = sha256(path)
    if actual_hash != SOURCE_SHA256:
        raise SystemExit(
            f"Unexpected SHA-256 for {path}: {actual_hash}. Expected {SOURCE_SHA256}."
        )


def extract_pdf_text(path: Path) -> str:
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise SystemExit("Missing required tool: pdftotext")

    result = subprocess.run(
        [pdftotext, "-f", str(PDF_FIRST_PAGE), "-l", str(PDF_LAST_PAGE), "-layout", str(path), "-"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def table_between(text: str, start: str, end: str | None = None) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index) if end else len(text)
    return text[start_index:end_index]


def parse_number(token: str) -> int | None:
    normalized = token.replace(" ", "").replace(".", "")
    if normalized in {"x", "-"}:
        return None
    return int(normalized)


def parse_table_value_by_scope(table_text: str) -> dict[tuple[str, int], int]:
    scope = None
    values: dict[tuple[str, int], int] = {}

    for line in table_text.splitlines():
        stripped = line.strip()
        if stripped in {"Alte Bundesländer", "Neue Bundesländer", "Insgesamt"}:
            scope = stripped
            continue

        match = ROW_START.match(line)
        if not match or scope is None:
            continue

        year = int(match.group(1))
        tokens = NUMBER_TOKEN.findall(match.group(2))
        if len(tokens) < 2:
            continue

        # In both DRV tables, the model variable is the second numeric column:
        # Beiträge in Einnahmen allg. RV and Rentenausgaben in Ausgaben allg. RV.
        value = parse_number(tokens[1])
        if value is not None:
            values[(scope, year)] = value

    return values


def select_scope(year: int, contributions: dict[tuple[str, int], int], outlays: dict[tuple[str, int], int]) -> str | None:
    if ("Insgesamt", year) in contributions and ("Insgesamt", year) in outlays:
        return "Insgesamt"
    if year <= 1990 and ("Alte Bundesländer", year) in contributions and ("Alte Bundesländer", year) in outlays:
        return "Alte Bundesländer"
    return None


def build_records(text: str) -> list[dict[str, object]]:
    income_text = table_between(text, "Einnahmen allg. RV", "Ausgaben allg. RV")
    expense_text = table_between(text, "Ausgaben allg. RV")

    contributions = parse_table_value_by_scope(income_text)
    outlays = parse_table_value_by_scope(expense_text)
    candidate_years = sorted({year for _, year in contributions} & {year for _, year in outlays})

    records: list[dict[str, object]] = []
    for year in candidate_years:
        scope = select_scope(year, contributions, outlays)
        if not scope:
            continue
        records.append(
            {
                "year": year,
                "scope": scope,
                "contributionsMioEur": contributions[(scope, year)],
                "pensionOutlaysMioEur": outlays[(scope, year)],
            }
        )

    extracted_years = [record["year"] for record in records]
    if extracted_years != EXPECTED_YEARS:
        raise SystemExit(f"Unexpected extracted years: {extracted_years}")

    records_by_year = {record["year"]: record for record in records}
    for year, (scope, contributions_mio_eur, pension_outlays_mio_eur) in SENTINELS.items():
        record = records_by_year[year]
        actual = (record["scope"], record["contributionsMioEur"], record["pensionOutlaysMioEur"])
        expected = (scope, contributions_mio_eur, pension_outlays_mio_eur)
        if actual != expected:
            raise SystemExit(f"Unexpected sentinel for {year}: {actual}. Expected {expected}.")

    return records


def csv_text(records: list[dict[str, object]]) -> str:
    buffer = io.StringIO()
    fieldnames = [
        "year",
        "scope",
        "contributions_mio_eur",
        "pension_outlays_mio_eur",
        "contributions_source_table",
        "contributions_source_page",
        "pension_outlays_source_table",
        "pension_outlays_source_page",
        "data_status",
        "selection_note",
    ]
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for record in records:
        writer.writerow(
            {
                "year": record["year"],
                "scope": record["scope"],
                "contributions_mio_eur": record["contributionsMioEur"],
                "pension_outlays_mio_eur": record["pensionOutlaysMioEur"],
                "contributions_source_table": "Einnahmen allg. RV",
                "contributions_source_page": 244,
                "pension_outlays_source_table": "Ausgaben allg. RV",
                "pension_outlays_source_page": 245,
                "data_status": "amtliche_zahl_pdf_text_extraktion",
                "selection_note": "Alte Bundesländer bis 1990; Insgesamt ab 1991; Neue Bundesländer nicht separat modelliert.",
            }
        )
    return buffer.getvalue()


def website_json_text(records: list[dict[str, object]]) -> str:
    payload = {
        "schemaVersion": 2,
        "status": "generated_from_drv_pdf_text_extraction",
        "language": "de",
        "title": "Website-Daten: allgemeine RV, Beiträge und Rentenausgaben",
        "warning": "Diese Datei ist generiert. Nicht manuell bearbeiten. Die Quelle ist die DRV-PDF-Publikation; Korrekturseiten sind noch nicht automatisiert abgeglichen. Die aktuelle Datenrechnung beginnt 1960; Lücken zwischen vorhandenen Stützjahren werden in der Website linear interpoliert.",
        "generatedBy": "scripts/build_drv_cashflows.py",
        "source": {
            "datasetId": "DRV_RV_ZEITREIHEN_2025_PDF",
            "publisher": "Deutsche Rentenversicherung",
            "title": "Rentenversicherung in Zeitreihen 2025",
            "landingPage": LANDING_PAGE,
            "pdfUrl": SOURCE_URL,
            "retrievedAt": "2026-05-04",
            "pdfSha256": SOURCE_SHA256,
            "extractionTool": "pdftotext -layout; version not pinned, see README checks",
            "pdfPageRange": [PDF_FIRST_PAGE, PDF_LAST_PAGE],
            "knownCorrectionsSource": {
                "datasetId": "DRV_RV_ZEITREIHEN_2025_CORRECTIONS",
                "landingPage": CORRECTIONS_LANDING_PAGE,
                "pdfUrl": CORRECTIONS_URL,
                "status": "not_automatically_checked",
            },
            "tables": [
                {"page": 244, "title": "Einnahmen allg. RV", "variable": "Beiträge"},
                {"page": 245, "title": "Ausgaben allg. RV", "variable": "Rentenausgaben"},
            ],
        },
        "scope": {
            "institution": "allgemeine RV",
            "geographyNote": "Alte Bundesländer bis 1990; ab 1991 Insgesamt, soweit in der geprüften Tabelle ausgewiesen.",
            "unit": "Mio. EUR, nominal",
            "dataStatus": "amtliche Zahl aus PDF-Text-Extraktion; Korrekturseiten noch nicht geprüft",
        },
        "records": records,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def write_or_check(path: Path, content: str, check: bool) -> bool:
    if check:
        if not path.exists():
            print(f"Missing generated file: {path.relative_to(ROOT)}", file=sys.stderr)
            return False
        existing = path.read_text(encoding="utf-8")
        if existing != content:
            print(f"Generated file is stale: {path.relative_to(ROOT)}", file=sys.stderr)
            return False
        return True

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    args = parse_args()
    source_pdf = args.source_pdf if args.source_pdf.is_absolute() else ROOT / args.source_pdf
    ensure_source_pdf(source_pdf, allow_download=not args.no_download and not args.check)
    text = extract_pdf_text(source_pdf)
    records = build_records(text)

    ok_csv = write_or_check(EXTRACTED_CSV, csv_text(records), args.check)
    ok_json = write_or_check(WEBSITE_JSON, website_json_text(records), args.check)
    if args.check and not (ok_csv and ok_json):
        return 1

    verb = "Verified" if args.check else "Wrote"
    print(f"{verb} {len(records)} allg. RV cashflow records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
