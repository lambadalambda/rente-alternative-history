# DRV-Cashflow-Extraktion

Dieses Verzeichnis enthält aus der DRV-PDF-Publikation extrahierte Zwischendaten. Die Dateien werden durch `scripts/build_drv_cashflows.py` erzeugt und sollen nicht manuell bearbeitet werden.

## Quelle

- Herausgeber: Deutsche Rentenversicherung
- Quelle: `Rentenversicherung in Zeitreihen 2025`
- PDF: `https://www.deutsche-rentenversicherung.de/SharedDocs/Downloads/DE/Statistiken-und-Berichte/statistikpublikationen/rv_in_zeitreihen.pdf?__blob=publicationFile&v=9`
- Abrufdatum: 2026-05-04
- SHA-256: `f41ad3a1c398ac56ad5ac75898ba5c664aa1ef7e6ad98859cb2a622b6293ee07`

## Regeneration

```bash
python3 scripts/build_drv_cashflows.py
```

Der Roh-PDF-Download landet unter `data/raw/drv/` und wird nicht versioniert. Das Skript prüft den SHA-256-Hash und extrahiert die PDF-Seiten 246-247 mit `pdftotext -layout`. In der DRV-Publikation entsprechen diese PDF-Seiten den Inhaltsseiten 244-245:

- `Einnahmen allg. RV`, Variable `Beiträge`
- `Ausgaben allg. RV`, Variable `Rentenausgaben`

Voraussetzung: `pdftotext` aus Poppler oder Xpdf muss lokal verfügbar sein. Die Layout-Ausgabe kann je Version variieren; das Skript prüft deshalb die erwartete Jahresliste und mehrere Sentinel-Werte.

Nicht-mutierende Prüfung vorhandener Artefakte:

```bash
python3 scripts/build_drv_cashflows.py --check --no-download
```

## Aktuelle Grenzen

- Die DRV-Korrekturseiten sind noch nicht automatisiert abgeglichen.
- Für `allgemeine RV` enthält die Tabelle keine durchgehenden Jahreswerte ab 1957. Die aktuelle Website-Datenrechnung beginnt 1960; Lücken zwischen vorhandenen Stützjahren werden linear interpoliert.
- Die Baseline nutzt `Alte Bundesländer` bis 1990 und `Insgesamt` ab 1991. Neue Bundesländer werden nicht separat modelliert.
- Eine erste manuelle Stichprobenkontrolle liegt unter `data/quality/drv/allgemeine-rv-cashflow-spotchecks.json`; sie ersetzt noch keinen vollständigen Tabellen- und Korrekturseitenabgleich.
