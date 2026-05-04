# Rendite-Extraktion

Dieses Verzeichnis enthält aus externen Kapitalmarktquellen extrahierte Zwischendaten. Die Dateien werden durch Skripte erzeugt und sollen nicht manuell bearbeitet werden.

## Shiller-US-Aktienmarktproxy

- Herausgeber: Robert J. Shiller / Yale University website
- Quelle: `Annual U.S. Stock Price Data, Chapter 26 update`
- Landingpage: `http://www.econ.yale.edu/~shiller/data.htm`
- Aktuelle Datenseite laut Recherche: `https://shillerdata.com/`
- Datei: `http://www.econ.yale.edu/~shiller/data/chapt26.xlsx`
- Erstes Hash-Prüfdatum: 2026-05-04
- SHA-256: `d255bb1230a9a94c450ee4738d914ec8c6c79ceae58f1cc89559c7f40fa7c9c0`
- Lokale Ausgabe: `data/processed/returns/shiller-sp500-proxy-annual.csv` und `data/processed/returns/shiller-return-series.json`
- Versionierter Qualitätsnachweis: `data/quality/returns/shiller-return-pipeline-check.json`

Regeneration:

```bash
python3 scripts/build_shiller_returns.py
```

Nicht-mutierende Prüfung des versionierten Qualitätsnachweises. Wenn die Rohdatei fehlt, lädt der Prüfmodus die hashgeprüfte Quelle in ein temporäres Verzeichnis, nicht nach `data/raw/`:

```bash
python3 scripts/build_shiller_returns.py --check
```

Strikt offline prüfen, wenn die Rohdatei bereits unter `data/raw/returns/shiller_chapt26.xlsx` liegt:

```bash
python3 scripts/build_shiller_returns.py --check --no-download
```

## Methodische Einordnung

- Die Reihe ist ein Forschungsproxy für den US-Aktienmarkt, keine offizielle S&P-500-Total-Return-Reihe.
- Die vollständige generierte Reihe wird wegen ungeklärter Weiterverbreitungsrechte nicht versioniert und nicht in `data/website/` veröffentlicht.
- Der historische Yale-Dateilink ist nur per HTTP erreichbar; die Pipeline pinnt und prüft deshalb den SHA-256-Hash strikt.
- Die jährlichen Renditen laufen jeweils von Jahr `t` bis `t+1`.
- `nominal_total_return` wird aus Preisindex und Dividende rekonstruiert: `(Preis_{t+1} + Dividende_t) / Preis_t - 1`.
- `real_total_return` deflationiert Preis und Dividende mit dem CPI der Shiller-Arbeitsmappe; soweit die Arbeitsmappe eine gecachte reale Rendite enthält, gleicht das Skript dagegen ab.
- Die aktuelle generierte Reihe deckt Renditejahre `1871-2014` ab. Für das Rentenmodell sind besonders `1960-2014` relevant; spätere Jahre fehlen in dieser Quelle.
- Die Renditejahre `2013` und `2014` sind formelbasiert rekonstruiert, aber nicht gegen eine gecachte Workbook-Rendite validiert, weil Spalte `P` dort leer ist.
- Für eine deutsche Rentenrechnung fehlen noch die freigegebene DM-/Euro-/USD-Wechselkursbehandlung, deutsche Inflation und eine explizite Entscheidung, ob nominale USD-, nominale DM/EUR- oder reale Renditen genutzt werden.

## Lokale EUR-Äquivalent-Hilfsrechnung

`scripts/build_us_equity_eur_returns.py` kombiniert den nominalen Shiller-US-Renditeproxy mit den reziprok abgeleiteten Bundesbank-FX-Hilfswerten aus `scripts/build_bundesbank_fx.py`.

Regeneration:

```bash
python3 scripts/build_us_equity_eur_returns.py
```

Nicht-mutierende Prüfung:

```bash
python3 scripts/build_us_equity_eur_returns.py --check
```

Strikt offline prüfen, wenn die Rohdateien bereits unter `data/raw/returns/shiller_chapt26.xlsx` und `data/raw/bundesbank/i-10-wechselkurse.pdf` liegen:

```bash
python3 scripts/build_us_equity_eur_returns.py --check --no-download
```

Voraussetzungen: `pdftotext` muss verfügbar sein, weil die Bundesbank-FX-Pipeline die PDF per Layout-Text extrahiert. Der normale Prüfmodus kann fehlende Rohquellen temporär herunterladen; `--no-download` verhindert Netzwerkzugriff.

Die vollständige Reihe wird lokal unter `data/processed/returns/shiller-us-equity-eur-equivalent-annual.csv` und `data/processed/returns/shiller-us-equity-eur-equivalent-annual.json` erzeugt. Versioniert ist nur `data/quality/returns/shiller-us-equity-eur-equivalent-check.json`.

Diese Hilfsrechnung ist nicht modellfreigegeben. Die Formel ist `(1 + USD-Nominalrendite) * (FX_Jahresdurchschnitt_t+1 / FX_Jahresdurchschnitt_t) - 1`, wobei `FX` der reziprok abgeleitete EUR-Äquivalentwert je USD ist. Offen sind Periodisierung, Cashflow-Timing, deutsche Inflationsbehandlung und Nutzungshinweise.
