#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

from build_drv_cashflows import (
    CORRECTIONS_CHECKED_PAGES,
    CORRECTIONS_LANDING_PAGE,
    CORRECTIONS_RETRIEVED_AT,
    CORRECTIONS_SHA256,
    CORRECTIONS_URL,
    ROOT,
    sha256,
)


DEFAULT_CORRECTIONS_PDF = ROOT / "data/raw/drv/rv_in_zeitreihen_korrekturseiten_2025.pdf"
QUALITY_JSON = ROOT / "data/quality/drv/rv-in-zeitreihen-korrekturseiten-check.json"
MODELED_TABLES = [
    {
        "contentPage": 244,
        "pdfPage": 246,
        "table": "Einnahmen allg. RV",
        "variable": "Beiträge",
    },
    {
        "contentPage": 245,
        "pdfPage": 247,
        "table": "Ausgaben allg. RV",
        "variable": "Rentenausgaben",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate whether DRV Zeitreihen correction pages affect the allg. RV cashflow tables."
    )
    parser.add_argument(
        "--corrections-pdf",
        type=Path,
        default=DEFAULT_CORRECTIONS_PDF,
        help=f"Path to the DRV correction PDF. Default: {DEFAULT_CORRECTIONS_PDF.relative_to(ROOT)}",
    )
    parser.add_argument(
        "--no-download",
        action="store_true",
        help="Fail instead of downloading the correction PDF when it is missing.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the quality-control JSON is up to date without writing it. Also avoids PDF download by default.",
    )
    return parser.parse_args()


def ensure_corrections_pdf(path: Path, allow_download: bool) -> None:
    if not path.exists():
        if not allow_download:
            raise SystemExit(f"Missing correction PDF: {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = path.with_suffix(path.suffix + ".download")
        with urllib.request.urlopen(CORRECTIONS_URL, timeout=120) as response, temporary_path.open("wb") as target:
            shutil.copyfileobj(response, target)

        downloaded_hash = sha256(temporary_path)
        if downloaded_hash != CORRECTIONS_SHA256:
            temporary_path.unlink(missing_ok=True)
            raise SystemExit(
                f"Unexpected SHA-256 for downloaded correction PDF: {downloaded_hash}. "
                f"Expected {CORRECTIONS_SHA256}."
            )
        temporary_path.replace(path)

    actual_hash = sha256(path)
    if actual_hash != CORRECTIONS_SHA256:
        raise SystemExit(f"Unexpected SHA-256 for {path}: {actual_hash}. Expected {CORRECTIONS_SHA256}.")


def extract_pdf_pages(path: Path) -> list[str]:
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
    return [page for page in result.stdout.split("\f") if page.strip()]


def content_page_number(page_text: str) -> int:
    candidates: list[int] = []
    for line in page_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.endswith("Rentenversicherung in Zeitreihen 2025"):
            first_token = stripped.split()[0]
            if first_token.isdigit():
                candidates.append(int(first_token))
        if stripped.startswith("Rentenversicherung in Zeitreihen 2025"):
            last_token = stripped.split()[-1]
            if last_token.isdigit():
                candidates.append(int(last_token))

    unique_candidates = list(dict.fromkeys(candidates))
    if len(unique_candidates) != 1:
        raise SystemExit(f"Could not determine unique corrected content page from correction PDF page: {candidates}")
    return unique_candidates[0]


def page_topic(page_text: str) -> str:
    if "Rentenbestand nach Wohnort (Bundesland)" in page_text:
        return "Rentenbestand nach Wohnort (Bundesland), Renten wegen Alters - Männer"
    if "Baden-" in page_text and "Mecklenburg-" in page_text:
        return "Rentenbestand nach Wohnort (Bundesland), Renten wegen Alters - Männer, Fortsetzung"
    if "Bemessungswerte der RV" in page_text:
        return "Bemessungswerte der RV, jährliche Höchstwerte an Entgeltpunkten"
    return "nicht automatisch klassifiziert"


def build_payload(pages: list[str]) -> dict[str, object]:
    corrected_pages = [content_page_number(page) for page in pages]
    if corrected_pages != CORRECTIONS_CHECKED_PAGES:
        raise SystemExit(f"Unexpected corrected pages: {corrected_pages}. Expected {CORRECTIONS_CHECKED_PAGES}.")

    model_content_pages = [table["contentPage"] for table in MODELED_TABLES]
    affected_pages = sorted(set(corrected_pages) & set(model_content_pages))
    text = "\n".join(pages)
    table_title_matches = [table["table"] for table in MODELED_TABLES if table["table"] in text]
    if affected_pages or table_title_matches:
        raise SystemExit(
            "Correction pages may affect modeled cashflow tables: "
            f"affected_pages={affected_pages}, table_title_matches={table_title_matches}"
        )

    return {
        "schemaVersion": 1,
        "status": "checked_no_model_table_corrections",
        "checkedAt": CORRECTIONS_RETRIEVED_AT,
        "sourceDatasetId": "DRV_RV_ZEITREIHEN_2025_CORRECTIONS",
        "sourceTitle": "Deutsche Rentenversicherung, Rentenversicherung in Zeitreihen - Korrekturseiten",
        "landingPage": CORRECTIONS_LANDING_PAGE,
        "pdfUrl": CORRECTIONS_URL,
        "retrievedAt": CORRECTIONS_RETRIEVED_AT,
        "sourceSha256": CORRECTIONS_SHA256,
        "method": "SHA-256-Prüfung der Korrekturseiten-PDF, Extraktion mit pdftotext -layout, Ermittlung der korrigierten Inhaltsseiten aus den Seitenfüßen und Abgleich gegen die modellierten Inhaltsseiten 244-245.",
        "modeledTables": MODELED_TABLES,
        "correctedContentPages": [
            {
                "correctionPdfPage": index + 1,
                "contentPage": page_number,
                "topic": page_topic(page_text),
            }
            for index, (page_number, page_text) in enumerate(zip(corrected_pages, pages))
        ],
        "result": {
            "modelSourcePagesAffected": False,
            "affectedModeledContentPages": [],
            "modeledTableTitleMatchesInCorrectionText": [],
            "note": "Die bekannten Korrekturseiten v=3 betreffen Inhaltsseiten 172, 173 und 263; die aktuelle allg.-RV-Cashflow-Pipeline nutzt Inhaltsseiten 244 und 245.",
        },
    }


def write_or_check(path: Path, content: str, check: bool) -> bool:
    if check:
        if not path.exists():
            print(f"Missing quality-control file: {path.relative_to(ROOT)}", file=sys.stderr)
            return False
        existing = path.read_text(encoding="utf-8")
        if existing != content:
            print(f"Quality-control file is stale: {path.relative_to(ROOT)}", file=sys.stderr)
            return False
        return True

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    args = parse_args()
    corrections_pdf = args.corrections_pdf if args.corrections_pdf.is_absolute() else ROOT / args.corrections_pdf
    ensure_corrections_pdf(corrections_pdf, allow_download=not args.no_download and not args.check)
    payload = build_payload(extract_pdf_pages(corrections_pdf))
    content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    ok = write_or_check(QUALITY_JSON, content, args.check)
    if args.check and not ok:
        return 1

    verb = "Verified" if args.check else "Wrote"
    corrected_pages = ", ".join(str(page) for page in payload["result"]["affectedModeledContentPages"])
    if not corrected_pages:
        corrected_pages = "none"
    print(f"{verb} DRV correction-page check; affected modeled pages: {corrected_pages}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
