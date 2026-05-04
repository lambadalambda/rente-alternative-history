#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]

SOURCE_URL = "http://www.econ.yale.edu/~shiller/data/chapt26.xlsx"
SOURCE_PAGE = "http://www.econ.yale.edu/~shiller/data.htm"
CURRENT_SOURCE_PAGE = "https://shillerdata.com/"
SOURCE_SHA256 = "d255bb1230a9a94c450ee4738d914ec8c6c79ceae58f1cc89559c7f40fa7c9c0"
SOURCE_HASH_VERIFIED_AT = "2026-05-04"

DEFAULT_SOURCE_XLSX = ROOT / "data/raw/returns/shiller_chapt26.xlsx"
PROCESSED_CSV = ROOT / "data/processed/returns/shiller-sp500-proxy-annual.csv"
PROCESSED_JSON = ROOT / "data/processed/returns/shiller-return-series.json"
QUALITY_JSON = ROOT / "data/quality/returns/shiller-return-pipeline-check.json"
FORBIDDEN_PUBLISHED_OUTPUTS = [
    ROOT / "data/website/return-series.json",
    ROOT / "data/extracted/returns/shiller-sp500-proxy-annual.csv",
    ROOT / "data/extracted/returns/shiller-return-series.json",
]
FORBIDDEN_PUBLISHED_PATTERNS = [
    ROOT / "data/website/*return*",
    ROOT / "data/extracted/returns/*shiller*.csv",
    ROOT / "data/extracted/returns/*shiller*.json",
]
FORBIDDEN_GIT_TRACKED_OUTPUTS = [
    PROCESSED_CSV,
    PROCESSED_JSON,
    *FORBIDDEN_PUBLISHED_OUTPUTS,
]

EXPECTED_YEARS = list(range(1871, 2015))
SENTINELS = {
    1957: (-0.055469953775038605, -0.08849547986682049),
    1960: (0.06272617611580222, 0.04489520000647662),
    2008: (-0.35161304360439816, -0.3514994224216611),
    2014: (0.1345837265962817, 0.135598364578279),
}

NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "office_rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
TEMPORARY_DIRECTORIES: list[tempfile.TemporaryDirectory[str]] = []


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build annual Shiller U.S. equity proxy returns from the Chapter 26 XLSX workbook."
    )
    parser.add_argument(
        "--source-xlsx",
        type=Path,
        default=DEFAULT_SOURCE_XLSX,
        help=f"Path to the Shiller Chapter 26 XLSX. Default: {DEFAULT_SOURCE_XLSX.relative_to(ROOT)}",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Fail instead of downloading the source XLSX when it is missing.",
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


def ensure_source_xlsx(path: Path, allow_download: bool) -> None:
    if not path.exists():
        if not allow_download:
            raise SystemExit(f"Missing source XLSX: {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = path.with_suffix(path.suffix + ".download")
        with urllib.request.urlopen(SOURCE_URL, timeout=120) as response, temporary_path.open("wb") as target:
            shutil.copyfileobj(response, target)

        downloaded_hash = sha256(temporary_path)
        if downloaded_hash != SOURCE_SHA256:
            temporary_path.unlink(missing_ok=True)
            raise SystemExit(
                f"Unexpected SHA-256 for downloaded Shiller workbook: {downloaded_hash}. "
                f"Expected {SOURCE_SHA256}."
            )
        temporary_path.replace(path)

    actual_hash = sha256(path)
    if actual_hash != SOURCE_SHA256:
        raise SystemExit(f"Unexpected SHA-256 for {path}: {actual_hash}. Expected {SOURCE_SHA256}.")


def download_source_to_temp() -> Path:
    temporary_directory = tempfile.TemporaryDirectory(prefix="rente-shiller-")
    temporary_path = Path(temporary_directory.name) / "shiller_chapt26.xlsx"
    with urllib.request.urlopen(SOURCE_URL, timeout=120) as response, temporary_path.open("wb") as target:
        shutil.copyfileobj(response, target)

    downloaded_hash = sha256(temporary_path)
    if downloaded_hash != SOURCE_SHA256:
        temporary_directory.cleanup()
        raise SystemExit(
            f"Unexpected SHA-256 for downloaded Shiller workbook: {downloaded_hash}. "
            f"Expected {SOURCE_SHA256}."
        )

    TEMPORARY_DIRECTORIES.append(temporary_directory)
    return temporary_path


def colname(cell_ref: str) -> str:
    match = re.match(r"([A-Z]+)", cell_ref)
    if not match:
        raise ValueError(f"Missing column in cell reference: {cell_ref}")
    return match.group(1)


def text_content(element: ElementTree.Element) -> str:
    return "".join(text.text or "" for text in element.findall(".//main:t", NS))


def shared_strings(workbook: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in workbook.namelist():
        return []
    root = ElementTree.fromstring(workbook.read("xl/sharedStrings.xml"))
    return [text_content(item) for item in root.findall("main:si", NS)]


def sheet_path(workbook: zipfile.ZipFile, sheet_name: str) -> str:
    workbook_xml = ElementTree.fromstring(workbook.read("xl/workbook.xml"))
    rels_xml = ElementTree.fromstring(workbook.read("xl/_rels/workbook.xml.rels"))
    rel_targets = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels_xml.findall("rel:Relationship", NS)}

    for sheet in workbook_xml.findall("main:sheets/main:sheet", NS):
        if sheet.attrib.get("name") != sheet_name:
            continue
        rel_id = sheet.attrib[f"{{{NS['office_rel']}}}id"]
        target = rel_targets[rel_id]
        return f"xl/{target}" if not target.startswith("xl/") else target

    raise SystemExit(f"Sheet not found in workbook: {sheet_name}")


def cell_value(cell: ElementTree.Element, strings: list[str]) -> str:
    value = cell.find("main:v", NS)
    if value is None:
        inline = cell.find("main:is", NS)
        return text_content(inline) if inline is not None else ""

    raw = value.text or ""
    if cell.attrib.get("t") == "s":
        return strings[int(raw)]
    return raw


def parse_float(value: str | None) -> float | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        parsed = float(value)
    except ValueError:
        return None
    return parsed if math.isfinite(parsed) else None


def validate_headers(cells_by_ref: dict[str, str]) -> None:
    expected = {
        "B3": "P",
        "B4": "S&P",
        "B5": "Composite",
        "B8": "Index",
        "C3": "D",
        "C4": "Dividends",
        "C5": "Accruing",
        "G3": "CPI",
        "G4": "Consumer",
        "G5": "Price",
        "P3": "Return",
        "P4": "on",
        "P5": "S&P",
        "P6": "Composite",
    }
    mismatches = [
        f"{ref}: {cells_by_ref.get(ref)!r} != {value!r}"
        for ref, value in expected.items()
        if cells_by_ref.get(ref) != value
    ]
    if mismatches:
        raise SystemExit("Unexpected Shiller workbook headers: " + "; ".join(mismatches))


def parse_workbook(path: Path) -> dict[int, dict[str, float | None]]:
    with zipfile.ZipFile(path) as workbook:
        strings = shared_strings(workbook)
        root = ElementTree.fromstring(workbook.read(sheet_path(workbook, "Data")))

    rows: dict[int, dict[str, float | None]] = {}
    cells_by_ref: dict[str, str] = {}
    for row in root.findall("main:sheetData/main:row", NS):
        cells = {}
        for cell in row.findall("main:c", NS):
            ref = cell.attrib["r"]
            value = cell_value(cell, strings)
            cells[colname(ref)] = value
            cells_by_ref[ref] = value

        year_text = cells.get("A", "")
        if not re.fullmatch(r"\d{4}", str(year_text)):
            continue
        year = int(year_text)
        rows[year] = {
            "priceIndex": parse_float(cells.get("B")),
            "dividend": parse_float(cells.get("C")),
            "cpi": parse_float(cells.get("G")),
            "cachedRealTotalReturn": parse_float(cells.get("P")),
        }
    validate_headers(cells_by_ref)
    return rows


def build_records(source_rows: dict[int, dict[str, float | None]]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []

    for year in sorted(source_rows):
        current = source_rows[year]
        following = source_rows.get(year + 1)
        if not following:
            continue

        price = current["priceIndex"]
        dividend = current["dividend"]
        cpi = current["cpi"]
        next_price = following["priceIndex"]
        next_cpi = following["cpi"]
        if None in (price, dividend, cpi, next_price, next_cpi):
            continue

        nominal_return = (next_price + dividend) / price - 1
        real_return = ((next_price + dividend) / next_cpi) / (price / cpi) - 1
        cached_real_return = current["cachedRealTotalReturn"]
        validated_against_workbook_cache = cached_real_return is not None

        if cached_real_return is not None and abs(real_return - cached_real_return) > 1e-12:
            raise SystemExit(
                f"Computed real return for {year} differs from workbook cache: "
                f"{real_return} vs {cached_real_return}"
            )

        records.append(
            {
                "year": year,
                "period": f"{year}-{year + 1}",
                "nominalTotalReturn": nominal_return,
                "realTotalReturn": real_return,
                "priceIndex": price,
                "dividend": dividend,
                "cpi": cpi,
                "nextYearPriceIndex": next_price,
                "nextYearCpi": next_cpi,
                "cachedRealTotalReturn": cached_real_return,
                "validatedAgainstWorkbookCache": validated_against_workbook_cache,
                "dataStatus": "reconstructed_research_proxy",
            }
        )

    years = [int(record["year"]) for record in records]
    if years != EXPECTED_YEARS:
        raise SystemExit(f"Unexpected Shiller return years: {years[:3]} ... {years[-3:]} ({len(years)} rows)")

    records_by_year = {int(record["year"]): record for record in records}
    for year, (expected_nominal, expected_real) in SENTINELS.items():
        record = records_by_year[year]
        actual = (float(record["nominalTotalReturn"]), float(record["realTotalReturn"]))
        if abs(actual[0] - expected_nominal) > 1e-12 or abs(actual[1] - expected_real) > 1e-12:
            raise SystemExit(f"Unexpected Shiller sentinel for {year}: {actual}")

    return records


def format_decimal(value: object) -> str:
    if value is None:
        return ""
    return f"{float(value):.15g}"


def csv_text(records: list[dict[str, object]]) -> str:
    buffer = io.StringIO()
    fieldnames = [
        "year",
        "period",
        "nominal_total_return",
        "real_total_return",
        "price_index",
        "dividend",
        "cpi",
        "next_year_price_index",
        "next_year_cpi",
        "cached_real_total_return",
        "validated_against_workbook_cache",
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
                "nominal_total_return": format_decimal(record["nominalTotalReturn"]),
                "real_total_return": format_decimal(record["realTotalReturn"]),
                "price_index": format_decimal(record["priceIndex"]),
                "dividend": format_decimal(record["dividend"]),
                "cpi": format_decimal(record["cpi"]),
                "next_year_price_index": format_decimal(record["nextYearPriceIndex"]),
                "next_year_cpi": format_decimal(record["nextYearCpi"]),
                "cached_real_total_return": format_decimal(record["cachedRealTotalReturn"]),
                "validated_against_workbook_cache": str(record["validatedAgainstWorkbookCache"]).lower(),
                "data_status": record["dataStatus"],
                "source_note": "Robert-Shiller-Forschungsproxy; keine offizielle S&P-500-Total-Return-Reihe; Renditen laufen jeweils von Jahr t bis t+1.",
            }
        )
    return buffer.getvalue()


def processed_json_text(records: list[dict[str, object]]) -> str:
    payload = {
        "schemaVersion": 1,
        "status": "generated_from_shiller_chapter26_xlsx",
        "language": "de",
        "title": "Verarbeitete Daten: jährliche US-Aktienmarkt-Renditen nach Shiller",
        "warning": "Diese Datei ist generiert und liegt absichtlich unter data/processed/, weil die Weiterverbreitungslizenz der Shiller-Daten noch nicht geklärt ist. Nicht manuell bearbeiten und vor Lizenzklärung nicht veröffentlichen.",
        "generatedBy": "scripts/build_shiller_returns.py",
        "source": {
            "datasetId": "SHILLER_CHAPTER26_ANNUAL_XLSX",
            "publisher": "Robert J. Shiller / Yale University website",
            "title": "Annual U.S. Stock Price Data, Chapter 26 update",
            "landingPage": SOURCE_PAGE,
            "currentLandingPage": CURRENT_SOURCE_PAGE,
            "downloadUrl": SOURCE_URL,
            "sourceHashVerifiedAt": SOURCE_HASH_VERIFIED_AT,
            "xlsxSha256": SOURCE_SHA256,
            "extractionTool": "Python stdlib zipfile/xml parser for XLSX worksheet Data",
            "sourceColumns": {
                "A": "year",
                "B": "S&P Composite Stock Price Index",
                "C": "Dividends Accruing to Index",
                "G": "Consumer Price Index",
                "P": "cached real return on S&P Composite where populated",
            },
        },
        "series": {
            "id": "shiller_us_equity_proxy_annual",
            "label": "US-Aktienmarkt nach Shiller, Forschungsproxy",
            "currency": "USD",
            "nominalOrReal": "nominal und real ausgewiesen",
            "returnMeasurement": "Jährliche Total-Return-Rekonstruktion aus Preisindex, Dividende und CPI; periodisiert von Jahr t bis t+1.",
            "dataYears": [records[0]["year"], records[-1]["year"]],
            "modelFitNote": "Für eine deutsche Rentenrechnung fehlen noch DEM/EUR/USD-Wechselkurse und eine Entscheidung, ob nominale USD-, nominale DM/EUR- oder reale Renditen verwendet werden.",
        },
        "records": [
            {
                "year": record["year"],
                "period": record["period"],
                "nominalTotalReturn": record["nominalTotalReturn"],
                "realTotalReturn": record["realTotalReturn"],
                "validatedAgainstWorkbookCache": record["validatedAgainstWorkbookCache"],
                "dataStatus": record["dataStatus"],
            }
            for record in records
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def quality_json_text(records: list[dict[str, object]]) -> str:
    records_by_year = {record["year"]: record for record in records}
    formula_only_years = [record["year"] for record in records if not record["validatedAgainstWorkbookCache"]]
    tracked_forbidden_outputs = git_tracked_forbidden_outputs()
    payload = {
        "schemaVersion": 1,
        "status": "checked_source_and_return_formula",
        "qualityArtifactCreatedAt": SOURCE_HASH_VERIFIED_AT,
        "sourceHashVerifiedAt": SOURCE_HASH_VERIFIED_AT,
        "sourceDatasetId": "SHILLER_CHAPTER26_ANNUAL_XLSX",
        "sourceTitle": "Robert J. Shiller, Annual U.S. Stock Price Data, Chapter 26 update",
        "landingPage": SOURCE_PAGE,
        "currentLandingPage": CURRENT_SOURCE_PAGE,
        "downloadUrl": SOURCE_URL,
        "downloadUrlUsesPlainHttp": True,
        "sourceSha256": SOURCE_SHA256,
        "method": "SHA-256-Prüfung der XLSX-Datei, Headerprüfung der genutzten Spalten, Extraktion der Data-Tabelle mit Python-stdlib und Rekonstruktion jährlicher nominaler sowie realer Total Returns.",
        "generatedDataLocation": "data/processed/returns/ (nicht versioniert, nicht fuer Veroeffentlichung ohne Lizenzklaerung)",
        "recordCount": len(records),
        "returnYearRange": [records[0]["year"], records[-1]["year"]],
        "formula": {
            "nominalTotalReturn": "(priceIndex_{t+1} + dividend_t) / priceIndex_t - 1",
            "realTotalReturn": "((priceIndex_{t+1} + dividend_t) / cpi_{t+1}) / (priceIndex_t / cpi_t) - 1",
        },
        "sentinelChecks": [
            {
                "year": year,
                "nominalTotalReturn": records_by_year[year]["nominalTotalReturn"],
                "realTotalReturn": records_by_year[year]["realTotalReturn"],
                "validatedAgainstWorkbookCache": records_by_year[year]["validatedAgainstWorkbookCache"],
            }
            for year in SENTINELS
        ],
        "formulaOnlyReturnYears": formula_only_years,
        "result": {
            "redistributionStatus": "not_cleared",
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
            "note": "Die vollstaendige Reihe wird nur lokal unter data/processed/ erzeugt. Vor Website-Nutzung sind Lizenz, DM-/Euro-/USD-Wechselkursbehandlung und eine Plausibilitaetsquelle zu klaeren. Der historische Yale-Download nutzt HTTP; die Datei wird deshalb strikt per SHA-256 geprueft.",
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def ensure_no_forbidden_published_outputs() -> None:
    exact_matches = [path for path in FORBIDDEN_PUBLISHED_OUTPUTS if path.exists()]
    pattern_matches = [match for pattern in FORBIDDEN_PUBLISHED_PATTERNS for match in pattern.parent.glob(pattern.name)]
    existing = sorted({path.relative_to(ROOT) for path in [*exact_matches, *pattern_matches]})
    tracked_existing = git_tracked_forbidden_outputs()
    if existing or tracked_existing:
        all_existing = sorted({str(path) for path in existing} | {str(path) for path in tracked_existing})
        raise SystemExit(
            "Full Shiller return series must not be committed or published before license clearance: "
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


def source_path_for_args(args: argparse.Namespace) -> Path:
    source_xlsx = args.source_xlsx if args.source_xlsx.is_absolute() else ROOT / args.source_xlsx
    if args.check and not source_xlsx.exists() and not args.no_download:
        return download_source_to_temp()
    ensure_source_xlsx(source_xlsx, allow_download=not args.no_download and not args.check)
    return source_xlsx


def main() -> int:
    args = parse_args()
    ensure_no_forbidden_published_outputs()
    records = build_records(parse_workbook(source_path_for_args(args)))

    if args.check:
        ok_quality = write_or_check(QUALITY_JSON, quality_json_text(records), True)
        if not ok_quality:
            return 1
    else:
        write_or_check(PROCESSED_CSV, csv_text(records), False)
        write_or_check(PROCESSED_JSON, processed_json_text(records), False)
        write_or_check(QUALITY_JSON, quality_json_text(records), False)

    verb = "Verified" if args.check else "Wrote"
    print(f"{verb} {len(records)} Shiller annual return records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
