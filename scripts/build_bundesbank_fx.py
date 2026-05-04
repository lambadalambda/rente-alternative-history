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
import tempfile
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SOURCE_URL = "https://www.bundesbank.de/resource/blob/844844/3c013bcde6fa7164d956999d8d16a761/mL/i-10-wechselkurse-data.pdf"
SOURCE_PAGE = "https://www.bundesbank.de/en/statistics/time-series-databases"
SOURCE_TITLE = "Long time series on economic development in Germany, X. Exchange rates"
SOURCE_PRINTED_DATE = "05-03-2026"
SOURCE_SHA256 = "f1ad66a9dc0501358fa31851066ee698b6fb64f056df725e95aeece2b9f24f15"
SOURCE_RETRIEVED_AT = "2026-05-04"

DEFAULT_SOURCE_PDF = ROOT / "data/raw/bundesbank/i-10-wechselkurse.pdf"
PROCESSED_CSV = ROOT / "data/processed/fx/bundesbank-usd-annual-fx.csv"
PROCESSED_JSON = ROOT / "data/processed/fx/bundesbank-usd-annual-fx.json"
QUALITY_JSON = ROOT / "data/quality/fx/bundesbank-usd-annual-fx-check.json"
FORBIDDEN_PUBLISHED_OUTPUTS = [
    ROOT / "data/website/fx-rates.json",
    ROOT / "data/extracted/fx/bundesbank-usd-annual-fx.csv",
]
FORBIDDEN_PUBLISHED_PATTERNS = [
    ROOT / "data/website/*fx*",
    ROOT / "data/website/*exchange*",
    ROOT / "data/website/*wechsel*",
    ROOT / "data/extracted/fx/*.csv",
    ROOT / "data/extracted/fx/*.json",
]
FORBIDDEN_GIT_TRACKED_OUTPUTS = [
    PROCESSED_CSV,
    PROCESSED_JSON,
    *FORBIDDEN_PUBLISHED_OUTPUTS,
]

DEM_PER_EUR = 1.95583
EXPECTED_YEARS = list(range(1948, 2026))
SENTINELS = {
    1960: ("DEM", 0.2398, 4.170141784820684, 2.132159638015924),
    1998: ("DEM", 0.5684, 1.7593244194229416, 0.8995282920412008),
    1999: ("EUR", 1.0658, 0.9382623381497466, 0.9382623381497466),
    2008: ("EUR", 1.4708, 0.6799020940984498, 0.6799020940984498),
    2024: ("EUR", 1.0824, 0.9238728750923872, 0.9238728750923872),
}

TEMPORARY_DIRECTORIES: list[tempfile.TemporaryDirectory[str]] = []
ROW_START = re.compile(r"^\s*(\d{4})\s+([0-9]+(?:\.[0-9]+)?)\b")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build annual Bundesbank USD exchange-rate data for DM/EUR conversion checks."
    )
    parser.add_argument(
        "--source-pdf",
        type=Path,
        default=DEFAULT_SOURCE_PDF,
        help=f"Path to the Bundesbank long-time-series PDF. Default: {DEFAULT_SOURCE_PDF.relative_to(ROOT)}",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Fail instead of downloading the source PDF when it is missing.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the tracked quality artifact without writing outputs. Downloads to a temporary file if the source is missing unless --no-download is set.",
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
                f"Unexpected SHA-256 for downloaded Bundesbank FX PDF: {downloaded_hash}. "
                f"Expected {SOURCE_SHA256}."
            )
        temporary_path.replace(path)

    actual_hash = sha256(path)
    if actual_hash != SOURCE_SHA256:
        raise SystemExit(f"Unexpected SHA-256 for {path}: {actual_hash}. Expected {SOURCE_SHA256}.")


def download_source_to_temp() -> Path:
    temporary_directory = tempfile.TemporaryDirectory(prefix="rente-bundesbank-fx-")
    temporary_path = Path(temporary_directory.name) / "i-10-wechselkurse.pdf"
    with urllib.request.urlopen(SOURCE_URL, timeout=120) as response, temporary_path.open("wb") as target:
        shutil.copyfileobj(response, target)

    downloaded_hash = sha256(temporary_path)
    if downloaded_hash != SOURCE_SHA256:
        temporary_directory.cleanup()
        raise SystemExit(
            f"Unexpected SHA-256 for downloaded Bundesbank FX PDF: {downloaded_hash}. Expected {SOURCE_SHA256}."
        )

    TEMPORARY_DIRECTORIES.append(temporary_directory)
    return temporary_path


def source_path_for_args(args: argparse.Namespace) -> Path:
    source_pdf = args.source_pdf if args.source_pdf.is_absolute() else ROOT / args.source_pdf
    if args.check and not source_pdf.exists() and not args.no_download:
        return download_source_to_temp()
    ensure_source_pdf(source_pdf, allow_download=not args.no_download and not args.check)
    return source_pdf


def extract_pdf_text(path: Path) -> str:
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise SystemExit("Missing required tool: pdftotext")

    result = subprocess.run(
        [pdftotext, "-layout", str(path), "-"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def table_between(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index)
    return text[start_index:end_index]


def parse_usd_column(table_text: str, currency: str) -> dict[int, dict[str, object]]:
    records: dict[int, dict[str, object]] = {}
    for line in table_text.splitlines():
        match = ROW_START.match(line)
        if not match:
            continue
        year = int(match.group(1))
        usd_per_local_currency = float(match.group(2))
        reciprocal_local_currency_per_usd = 1 / usd_per_local_currency
        reciprocal_eur_equivalent_per_usd = (
            reciprocal_local_currency_per_usd / DEM_PER_EUR if currency == "DEM" else reciprocal_local_currency_per_usd
        )
        records[year] = {
            "year": year,
            "currency": currency,
            "usdPerLocalCurrency": usd_per_local_currency,
            "reciprocalLocalCurrencyPerUsd": reciprocal_local_currency_per_usd,
            "reciprocalEurEquivalentPerUsd": reciprocal_eur_equivalent_per_usd,
            "sourceTable": "Exchange rates for the Deutsche Mark" if currency == "DEM" else "Euro foreign exchange reference rates",
            "dataStatus": "amtliche_zahl_pdf_text_extraktion",
        }
    return records


def build_records(text: str) -> list[dict[str, object]]:
    if SOURCE_PRINTED_DATE not in text:
        raise SystemExit(f"Missing expected printed source date in Bundesbank PDF text: {SOURCE_PRINTED_DATE}")

    dem_text = table_between(
        text,
        "1. Exchange rates for the Deutsche Mark",
        "Sources: Bundesbank calculations from daily exchange rates of the Bank",
    )
    eur_text = table_between(
        text,
        "2. Euro foreign exchange reference rates",
        "Source: Bundesbank calculations from daily exchange rates of the European Central Bank.",
    )
    records_by_year = parse_usd_column(dem_text, "DEM") | parse_usd_column(eur_text, "EUR")
    records = [records_by_year[year] for year in sorted(records_by_year)]

    years = [int(record["year"]) for record in records]
    if years != EXPECTED_YEARS:
        raise SystemExit(f"Unexpected Bundesbank FX years: {years[:3]} ... {years[-3:]} ({len(years)} rows)")

    for year, expected in SENTINELS.items():
        record = records_by_year[year]
        actual = (
            record["currency"],
            float(record["usdPerLocalCurrency"]),
            float(record["reciprocalLocalCurrencyPerUsd"]),
            float(record["reciprocalEurEquivalentPerUsd"]),
        )
        if actual[0] != expected[0] or any(abs(actual[index] - expected[index]) > 1e-12 for index in range(1, 4)):
            raise SystemExit(f"Unexpected Bundesbank FX sentinel for {year}: {actual}")

    return records


def format_decimal(value: object) -> str:
    return f"{float(value):.15g}"


def csv_text(records: list[dict[str, object]]) -> str:
    buffer = io.StringIO()
    fieldnames = [
        "year",
        "currency",
        "usd_per_local_currency",
        "reciprocal_local_currency_per_usd",
        "reciprocal_eur_equivalent_per_usd",
        "dem_per_eur_conversion",
        "source_table",
        "data_status",
        "source_note",
    ]
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for record in records:
        writer.writerow(
            {
                "year": record["year"],
                "currency": record["currency"],
                "usd_per_local_currency": format_decimal(record["usdPerLocalCurrency"]),
                "reciprocal_local_currency_per_usd": format_decimal(record["reciprocalLocalCurrencyPerUsd"]),
                "reciprocal_eur_equivalent_per_usd": format_decimal(record["reciprocalEurEquivalentPerUsd"]),
                "dem_per_eur_conversion": DEM_PER_EUR if record["currency"] == "DEM" else "",
                "source_table": record["sourceTable"],
                "data_status": record["dataStatus"],
                "source_note": "Bundesbank-Jahresdurchschnitt; Quelleneinheit: 1 DM/EUR = ... USD; EUR-Äquivalent vor 1999 mit festem Umrechnungskurs 1 EUR = 1,95583 DM.",
            }
        )
    return buffer.getvalue()


def processed_json_text(records: list[dict[str, object]]) -> str:
    payload = {
        "schemaVersion": 1,
        "status": "generated_from_bundesbank_long_time_series_pdf",
        "language": "de",
        "title": "Verarbeitete Daten: Bundesbank USD-Jahresdurchschnittskurse für DM/EUR",
        "warning": "Diese Datei ist generiert und liegt unter data/processed/. Vor Veröffentlichung sind Bundesbank-Nutzungshinweise und die genaue Wechselkursmethodik für das Modell zu prüfen.",
        "generatedBy": "scripts/build_bundesbank_fx.py",
        "source": {
            "datasetId": "BUNDESBANK_LONG_TIME_SERIES_FX_I10_2026_03_05",
            "publisher": "Deutsche Bundesbank",
            "title": SOURCE_TITLE,
            "landingPage": SOURCE_PAGE,
            "pdfUrl": SOURCE_URL,
            "retrievedAt": SOURCE_RETRIEVED_AT,
            "printedDate": SOURCE_PRINTED_DATE,
            "pdfSha256": SOURCE_SHA256,
            "extractionTool": "pdftotext -layout; Python stdlib parser for first USD column in the DM and euro annual-average tables",
        },
        "series": {
            "id": "bundesbank_usd_annual_dm_eur_fx",
            "label": "USD-Jahresdurchschnittskurse für DM/EUR nach Bundesbank",
            "sourceUnit": "1 DM/EUR = ... USD",
            "derivedFields": {
                "reciprocalLocalCurrencyPerUsd": "1 / usdPerLocalCurrency; reciprocal of an annual average, not an annual average of inverse daily rates",
                "reciprocalEurEquivalentPerUsd": "DEM je USD / 1.95583 bis 1998; EUR je USD ab 1999; reciprocal-derived",
            },
            "dataYears": [records[0]["year"], records[-1]["year"]],
            "modelReadiness": {
                "readyForModelIntegration": False,
                "ratePeriod": "calendar_year_average",
                "quoteBasis": "annual_average_usd_per_local_currency",
                "inverseRateBasis": "reciprocal_of_annual_average_not_average_of_inverse_daily_rates",
                "cashflowTiming": "not_decided",
                "allowedReturnPairing": "not_approved",
            },
        },
        "records": [
            {
                "year": record["year"],
                "currency": record["currency"],
                "usdPerLocalCurrency": record["usdPerLocalCurrency"],
                "reciprocalLocalCurrencyPerUsd": record["reciprocalLocalCurrencyPerUsd"],
                "reciprocalEurEquivalentPerUsd": record["reciprocalEurEquivalentPerUsd"],
                "dataStatus": record["dataStatus"],
            }
            for record in records
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def quality_json_text(records: list[dict[str, object]]) -> str:
    records_by_year = {record["year"]: record for record in records}
    canonical_csv = csv_text(records)
    canonical_csv_sha256 = hashlib.sha256(canonical_csv.encode("utf-8")).hexdigest()
    dem_record_count = sum(1 for record in records if record["currency"] == "DEM")
    eur_record_count = sum(1 for record in records if record["currency"] == "EUR")
    tracked_forbidden_outputs = git_tracked_forbidden_outputs()
    payload = {
        "schemaVersion": 1,
        "status": "checked_source_and_usd_fx_columns",
        "qualityArtifactCreatedAt": SOURCE_RETRIEVED_AT,
        "sourceRetrievedAt": SOURCE_RETRIEVED_AT,
        "sourceDatasetId": "BUNDESBANK_LONG_TIME_SERIES_FX_I10_2026_03_05",
        "sourceTitle": SOURCE_TITLE,
        "publisher": "Deutsche Bundesbank",
        "landingPage": SOURCE_PAGE,
        "pdfUrl": SOURCE_URL,
        "retrievedAt": SOURCE_RETRIEVED_AT,
        "printedDate": SOURCE_PRINTED_DATE,
        "sourceSha256": SOURCE_SHA256,
        "method": "SHA-256-Prüfung der Bundesbank-PDF, Extraktion mit pdftotext -layout und Auslesen der ersten USD-Spalte in den Tabellen DM-Jahresdurchschnitte 1948-1998 und Euro-Jahresdurchschnitte 1999-2025.",
        "generatedDataLocation": "data/processed/fx/ (nicht versioniert, nicht fuer Modellnutzung vor Methodikfreigabe)",
        "recordCount": len(records),
        "recordCountsByCurrency": {
            "DEM": dem_record_count,
            "EUR": eur_record_count,
        },
        "yearRange": [records[0]["year"], records[-1]["year"]],
        "sourceUnit": "1 DM/EUR = ... USD",
        "canonicalProcessedCsvSha256": canonical_csv_sha256,
        "derivedFields": {
            "reciprocalLocalCurrencyPerUsd": "1 / usdPerLocalCurrency; reciprocal of an annual average, not an annual average of inverse daily rates",
            "reciprocalEurEquivalentPerUsd": "DEM je USD / 1.95583 bis 1998; EUR je USD ab 1999; reciprocal-derived",
        },
        "modelReadiness": {
            "readyForModelIntegration": False,
            "ratePeriod": "calendar_year_average",
            "quoteBasis": "annual_average_usd_per_local_currency",
            "inverseRateBasis": "reciprocal_of_annual_average_not_average_of_inverse_daily_rates",
            "cashflowTiming": "not_decided",
            "allowedReturnPairing": "not_approved",
        },
        "sentinelChecks": [
            {
                "year": year,
                "currency": records_by_year[year]["currency"],
                "usdPerLocalCurrency": records_by_year[year]["usdPerLocalCurrency"],
                "reciprocalLocalCurrencyPerUsd": records_by_year[year]["reciprocalLocalCurrencyPerUsd"],
                "reciprocalEurEquivalentPerUsd": records_by_year[year]["reciprocalEurEquivalentPerUsd"],
            }
            for year in SENTINELS
        ],
        "result": {
            "fullGeneratedSeriesCommitted": bool(tracked_forbidden_outputs),
            "forbiddenPublishedOutputPathsAbsent": True,
            "gitTrackedForbiddenOutputPathsAbsent": not tracked_forbidden_outputs,
            "gitTrackedForbiddenOutputPaths": [str(path) for path in tracked_forbidden_outputs],
            "checkedForbiddenOutputPaths": [
                str(path.relative_to(ROOT)) for path in FORBIDDEN_PUBLISHED_OUTPUTS
            ],
            "checkedForbiddenOutputPatterns": [
                str(pattern.relative_to(ROOT)) for pattern in FORBIDDEN_PUBLISHED_PATTERNS
            ],
            "modelIntegrationStatus": "not_integrated",
            "note": "Die Reihe stellt nur den FX-Baustein bereit. Vor Kombination mit Shiller-Renditen sind Periodisierung, Wechselkurskonvention und Lizenz-/Nutzungshinweise zu prüfen.",
        },
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


def ensure_no_forbidden_published_outputs() -> None:
    exact_matches = [path for path in FORBIDDEN_PUBLISHED_OUTPUTS if path.exists()]
    pattern_matches = [match for pattern in FORBIDDEN_PUBLISHED_PATTERNS for match in pattern.parent.glob(pattern.name)]
    existing = sorted({path.relative_to(ROOT) for path in [*exact_matches, *pattern_matches]})
    tracked_existing = git_tracked_forbidden_outputs()
    if existing or tracked_existing:
        all_existing = sorted({str(path) for path in existing} | {str(path) for path in tracked_existing})
        raise SystemExit(
            "Full Bundesbank FX series must not be published before method and usage clearance: "
            + ", ".join(all_existing)
        )


def git_tracked_forbidden_outputs() -> list[Path]:
    relative_paths = [str(path.relative_to(ROOT)) for path in FORBIDDEN_GIT_TRACKED_OUTPUTS]
    try:
        result = subprocess.run(
            ["git", "ls-files", "--", *relative_paths],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError:
        return []
    if result.returncode != 0:
        return []
    return [Path(line) for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    args = parse_args()
    ensure_no_forbidden_published_outputs()
    records = build_records(extract_pdf_text(source_path_for_args(args)))

    if args.check:
        ok_quality = write_or_check(QUALITY_JSON, quality_json_text(records), True)
        if not ok_quality:
            return 1
    else:
        write_or_check(PROCESSED_CSV, csv_text(records), False)
        write_or_check(PROCESSED_JSON, processed_json_text(records), False)
        write_or_check(QUALITY_JSON, quality_json_text(records), False)

    verb = "Verified" if args.check else "Wrote"
    print(f"{verb} {len(records)} Bundesbank annual USD FX records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
