# DRV-Cashflow-Extraktion

Dieses Verzeichnis enthält aus der DRV-PDF-Publikation extrahierte Zwischendaten. Die Dateien werden durch `scripts/build_drv_cashflows.py` erzeugt und sollen nicht manuell bearbeitet werden.

## Quelle

- Herausgeber: Deutsche Rentenversicherung
- Quelle: `Rentenversicherung in Zeitreihen 2025`
- PDF: `https://www.deutsche-rentenversicherung.de/SharedDocs/Downloads/DE/Statistiken-und-Berichte/statistikpublikationen/rv_in_zeitreihen.pdf?__blob=publicationFile&v=9`
- Abrufdatum: 2026-05-04
- SHA-256: `f41ad3a1c398ac56ad5ac75898ba5c664aa1ef7e6ad98859cb2a622b6293ee07`

Bekannte Korrekturseiten:

- PDF: `https://www.deutsche-rentenversicherung.de/SharedDocs/Downloads/DE/Statistiken-und-Berichte/statistikpublikationen/rv_in_zeitreihen_korrekturseiten.pdf?__blob=publicationFile&v=3`
- Abrufdatum: 2026-05-04
- SHA-256: `694241a0db255784d52f87e323b4d181b66799c7f7df4ba81eee18f936562552`
- Ergebnis des aktuellen Checks: korrigierte Inhaltsseiten `172`, `173` und `263`; keine Korrektur der modellierten Inhaltsseiten `244` und `245`.

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

Korrekturseiten prüfen und das Qualitätsartefakt aktualisieren:

```bash
python3 scripts/validate_drv_corrections.py
```

Nicht-mutierende Prüfung des Korrekturseitenchecks:

```bash
python3 scripts/validate_drv_corrections.py --check --no-download
```

## Aktuelle Grenzen

- Die DRV-Korrekturseiten v=3 sind für die aktuell modellierten Inhaltsseiten 244-245 automatisiert abgeglichen. Bei neuer Korrekturseitenversion muss Hash, Seitenliste und Auswirkung neu geprüft werden.
- Für `allgemeine RV` enthält die Tabelle keine durchgehenden Jahreswerte ab 1957. Die aktuelle Website-Datenrechnung beginnt 1960; Lücken zwischen vorhandenen Stützjahren werden linear interpoliert.
- Die Baseline nutzt `Alte Bundesländer` bis 1990 und `Insgesamt` ab 1991. Neue Bundesländer werden nicht separat modelliert.
- Eine erste manuelle Stichprobenkontrolle liegt unter `data/quality/drv/allgemeine-rv-cashflow-spotchecks.json`; sie ersetzt noch keinen vollständigen Tabellenabgleich.
- Der Korrekturseitencheck liegt unter `data/quality/drv/rv-in-zeitreihen-korrekturseiten-check.json`; korrigierte Seiten 172, 173 und 263 müssen berücksichtigt werden, falls spätere Modellvariablen diese Tabellen nutzen.
