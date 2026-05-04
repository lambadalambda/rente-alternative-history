#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path

try:
    import build_bundesbank_fx as bundesbank_fx
    import build_shiller_returns as shiller_returns
except ModuleNotFoundError:  # pragma: no cover - used when imported as scripts.* in tests
    from . import build_bundesbank_fx as bundesbank_fx
    from . import build_shiller_returns as shiller_returns


ROOT = Path(__file__).resolve().parents[1]

PROCESSED_CSV = ROOT / "data/processed/returns/shiller-us-equity-eur-equivalent-annual.csv"
PROCESSED_JSON = ROOT / "data/processed/returns/shiller-us-equity-eur-equivalent-annual.json"
QUALITY_JSON = ROOT / "data/quality/returns/shiller-us-equity-eur-equivalent-check.json"
QUALITY_ARTIFACT_CREATED_AT = "2026-05-04"
FORBIDDEN_PUBLISHED_OUTPUTS = [
    ROOT / "data/website/us-equity-eur-returns.json",
    ROOT / "data/extracted/returns/shiller-us-equity-eur-equivalent-annual.csv",
    ROOT / "data/extracted/returns/shiller-us-equity-eur-equivalent-annual.json",
]
FORBIDDEN_PUBLISHED_PATTERNS = [
    ROOT / "data/website/*return*",
    ROOT / "data/extracted/returns/*eur*return*.csv",
    ROOT / "data/extracted/returns/*eur*return*.json",
    ROOT / "data/extracted/returns/*local*return*.csv",
    ROOT / "data/extracted/returns/*local*return*.json",
]
FORBIDDEN_GIT_TRACKED_OUTPUTS = [
    PROCESSED_CSV,
    PROCESSED_JSON,
    *FORBIDDEN_PUBLISHED_OUTPUTS,
]

EXPECTED_YEARS = list(range(1948, 2015))
SENTINELS = {
    1960: (0.06272617611580222, -0.03539823008849563, 0.025107550412587942),
    1998: (0.31308129878757684, 0.04306039782323112, 0.3696231018876148),
    1999: (0.15496048111341554, 0.1539627544391513, 0.3327813780540043),
    2008: (-0.35161304360439816, 0.05448809865213655, -0.316283671159556),
    2014: (0.1345837265962817, 0.1973862100045065, 0.35853490832191093),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a local-only EUR-equivalent return check from Shiller nominal returns and Bundesbank FX."
    )
    parser.add_argument(
        "--shiller-xlsx",
        type=Path,
        default=shiller_returns.DEFAULT_SOURCE_XLSX,
        help=f"Path to the Shiller Chapter 26 XLSX. Default: {shiller_returns.DEFAULT_SOURCE_XLSX.relative_to(ROOT)}",
    )
    parser.add_argument(
        "--fx-pdf",
        type=Path,
        default=bundesbank_fx.DEFAULT_SOURCE_PDF,
        help=f"Path to the Bundesbank FX PDF. Default: {bundesbank_fx.DEFAULT_SOURCE_PDF.relative_to(ROOT)}",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Fail instead of downloading missing source files.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the tracked quality artifact without writing outputs. Downloads missing sources to temporary files unless --no-download is set.",
    )
    return parser.parse_args()


def source_xlsx_for_args(args: argparse.Namespace) -> Path:
    source_xlsx = args.shiller_xlsx if args.shiller_xlsx.is_absolute() else ROOT / args.shiller_xlsx
    if args.check and not source_xlsx.exists() and not args.no_download:
        return shiller_returns.download_source_to_temp()
    shiller_returns.ensure_source_xlsx(source_xlsx, allow_download=not args.no_download and not args.check)
    return source_xlsx


def source_pdf_for_args(args: argparse.Namespace) -> Path:
    source_pdf = args.fx_pdf if args.fx_pdf.is_absolute() else ROOT / args.fx_pdf
    if args.check and not source_pdf.exists() and not args.no_download:
        return bundesbank_fx.download_source_to_temp()
    bundesbank_fx.ensure_source_pdf(source_pdf, allow_download=not args.no_download and not args.check)
    return source_pdf


def build_records(
    shiller_records: list[dict[str, object]], fx_records: list[dict[str, object]]
) -> list[dict[str, object]]:
    fx_by_year = {int(record["year"]): record for record in fx_records}
    records: list[dict[str, object]] = []

    for shiller_record in shiller_records:
        year = int(shiller_record["year"])
        start_fx = fx_by_year.get(year)
        end_fx = fx_by_year.get(year + 1)
        if not start_fx or not end_fx:
            continue

        usd_nominal_return = float(shiller_record["nominalTotalReturn"])
        average_fx_year_t = float(start_fx["reciprocalEurEquivalentPerUsd"])
        average_fx_year_t_plus_1 = float(end_fx["reciprocalEurEquivalentPerUsd"])
        reciprocal_fx_change = average_fx_year_t_plus_1 / average_fx_year_t - 1
        eur_equivalent_nominal_return = (1 + usd_nominal_return) * (1 + reciprocal_fx_change) - 1

        records.append(
            {
                "year": year,
                "period": f"{year}-{year + 1}",
                "usdNominalTotalReturn": usd_nominal_return,
                "reciprocalFxChange": reciprocal_fx_change,
                "eurEquivalentNominalReturn": eur_equivalent_nominal_return,
                "averageFxYearTReciprocalEurEquivalentPerUsd": average_fx_year_t,
                "averageFxYearTPlus1ReciprocalEurEquivalentPerUsd": average_fx_year_t_plus_1,
                "startFxCurrency": start_fx["currency"],
                "endFxCurrency": end_fx["currency"],
                "dataStatus": "reconstructed_research_proxy_not_model_ready",
            }
        )

    years = [int(record["year"]) for record in records]
    if years != EXPECTED_YEARS:
        raise SystemExit(f"Unexpected combined return years: {years[:3]} ... {years[-3:]} ({len(years)} rows)")

    records_by_year = {int(record["year"]): record for record in records}
    for year, expected in SENTINELS.items():
        record = records_by_year[year]
        actual = (
            float(record["usdNominalTotalReturn"]),
            float(record["reciprocalFxChange"]),
            float(record["eurEquivalentNominalReturn"]),
        )
        if any(abs(actual[index] - expected[index]) > 1e-12 for index in range(3)):
            raise SystemExit(f"Unexpected combined return sentinel for {year}: {actual}")

    return records


def format_decimal(value: object) -> str:
    return f"{float(value):.15g}"


def csv_text(records: list[dict[str, object]]) -> str:
    buffer = io.StringIO()
    fieldnames = [
        "year",
        "period",
        "usd_nominal_total_return",
        "reciprocal_fx_change",
        "eur_equivalent_nominal_return",
        "average_fx_year_t_reciprocal_eur_equivalent_per_usd",
        "average_fx_year_t_plus_1_reciprocal_eur_equivalent_per_usd",
        "start_fx_currency",
        "end_fx_currency",
        "data_status",
        "source_note",
    ]
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for record in records:
        writer.writerow(
            {
                "year": record["year"],
                "period": record["period"],
                "usd_nominal_total_return": format_decimal(record["usdNominalTotalReturn"]),
                "reciprocal_fx_change": format_decimal(record["reciprocalFxChange"]),
                "eur_equivalent_nominal_return": format_decimal(record["eurEquivalentNominalReturn"]),
                "average_fx_year_t_reciprocal_eur_equivalent_per_usd": format_decimal(record["averageFxYearTReciprocalEurEquivalentPerUsd"]),
                "average_fx_year_t_plus_1_reciprocal_eur_equivalent_per_usd": format_decimal(record["averageFxYearTPlus1ReciprocalEurEquivalentPerUsd"]),
                "start_fx_currency": record["startFxCurrency"],
                "end_fx_currency": record["endFxCurrency"],
                "data_status": record["dataStatus"],
                "source_note": "Lokale Hilfsrechnung aus Shiller-US-Renditeproxy und reziprok abgeleiteten Bundesbank-FX-Jahresdurchschnittswerten; nicht modellfreigegeben.",
            }
        )
    return buffer.getvalue()


def processed_json_text(records: list[dict[str, object]]) -> str:
    payload = {
        "schemaVersion": 1,
        "status": "generated_not_model_ready",
        "language": "de",
        "title": "Verarbeitete Daten: US-Aktienmarktproxy in EUR-Äquivalent",
        "warning": "Diese Datei ist eine lokale Hilfsrechnung unter data/processed/. Sie ist nicht modellfreigegeben, weil Wechselkursperiodisierung, inverse Jahresdurchschnittskurse und Nutzungsrechte noch offen sind.",
        "generatedBy": "scripts/build_us_equity_eur_returns.py",
        "sourceDatasetIds": [
            "SHILLER_CHAPTER26_ANNUAL_XLSX",
            "BUNDESBANK_LONG_TIME_SERIES_FX_I10_2026_03_05",
        ],
        "method": {
            "formula": "(1 + usdNominalTotalReturn) * (averageFxYearTPlus1ReciprocalEurEquivalentPerUsd / averageFxYearTReciprocalEurEquivalentPerUsd) - 1",
            "fxBasis": "reciprocal-derived Bundesbank annual-average USD per DM/EUR helper",
            "modelReady": False,
        },
        "records": records,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def quality_json_text(records: list[dict[str, object]]) -> str:
    canonical_csv = csv_text(records)
    canonical_csv_sha256 = hashlib.sha256(canonical_csv.encode("utf-8")).hexdigest()
    records_by_year = {record["year"]: record for record in records}
    tracked_forbidden_outputs = git_tracked_forbidden_outputs()
    payload = {
        "schemaVersion": 1,
        "status": "checked_combined_return_formula_not_model_ready",
        "qualityArtifactCreatedAt": QUALITY_ARTIFACT_CREATED_AT,
        "sourceDatasetIds": [
            "SHILLER_CHAPTER26_ANNUAL_XLSX",
            "BUNDESBANK_LONG_TIME_SERIES_FX_I10_2026_03_05",
        ],
        "upstreamSources": {
            "shillerXlsxSha256": shiller_returns.SOURCE_SHA256,
            "bundesbankFxPdfSha256": bundesbank_fx.SOURCE_SHA256,
            "shillerQualityArtifactSha256": file_sha256_if_exists(shiller_returns.QUALITY_JSON),
            "bundesbankFxQualityArtifactSha256": file_sha256_if_exists(bundesbank_fx.QUALITY_JSON),
        },
        "generatedBy": "scripts/build_us_equity_eur_returns.py",
        "generatedDataLocation": "data/processed/returns/ (nicht versioniert, nicht modellfreigegeben)",
        "recordCount": len(records),
        "yearRange": [records[0]["year"], records[-1]["year"]],
        "canonicalProcessedCsvSha256": canonical_csv_sha256,
        "formula": "(1 + usdNominalTotalReturn) * (averageFxYearTPlus1ReciprocalEurEquivalentPerUsd / averageFxYearTReciprocalEurEquivalentPerUsd) - 1",
        "modelReadiness": {
            "readyForModelIntegration": False,
            "reason": "FX uses reciprocal-derived annual-average helpers; cashflow timing, return period alignment, German inflation and source usage rights are unresolved.",
            "returnPeriod": "Shiller year t to t+1",
            "fxRatePeriod": "Bundesbank calendar-year average",
            "inverseRateBasis": "reciprocal_of_annual_average_not_average_of_inverse_daily_rates",
            "allowedWebsiteUse": False,
        },
        "sentinelChecks": [
            {
                "year": year,
                "usdNominalTotalReturn": records_by_year[year]["usdNominalTotalReturn"],
                "reciprocalFxChange": records_by_year[year]["reciprocalFxChange"],
                "eurEquivalentNominalReturn": records_by_year[year]["eurEquivalentNominalReturn"],
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
            "note": "Dieser Check beweist nur, dass die Hilfsrechnung reproduzierbar ist; er gibt keine Modellannahme frei.",
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def file_sha256_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
            "Combined Shiller/FX return series must not be published before methodology and usage clearance: "
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
    shiller_records = shiller_returns.build_records(
        shiller_returns.parse_workbook(source_xlsx_for_args(args))
    )
    fx_records = bundesbank_fx.build_records(
        bundesbank_fx.extract_pdf_text(source_pdf_for_args(args))
    )
    records = build_records(shiller_records, fx_records)

    if args.check:
        ok_quality = write_or_check(QUALITY_JSON, quality_json_text(records), True)
        if not ok_quality:
            return 1
    else:
        write_or_check(PROCESSED_CSV, csv_text(records), False)
        write_or_check(PROCESSED_JSON, processed_json_text(records), False)
        write_or_check(QUALITY_JSON, quality_json_text(records), False)

    verb = "Verified" if args.check else "Wrote"
    print(f"{verb} {len(records)} EUR-equivalent US equity proxy return records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
