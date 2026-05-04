# Wechselkurs-Extraktion

Dieses Verzeichnis dokumentiert Wechselkurs-Pipelines. Vollständige generierte Reihen liegen bis zur Methodik- und Nutzungsklärung nur lokal unter `data/processed/`.

## Bundesbank USD-Jahresdurchschnittskurse

- Herausgeber: Deutsche Bundesbank
- Quelle: `Long time series on economic development in Germany`, Abschnitt `X. Exchange rates`
- PDF: `https://www.bundesbank.de/resource/blob/844844/3c013bcde6fa7164d956999d8d16a761/mL/i-10-wechselkurse-data.pdf`
- Gedruckter Datenstand in der PDF: `05-03-2026`
- Abrufdatum: 2026-05-04
- SHA-256: `f1ad66a9dc0501358fa31851066ee698b6fb64f056df725e95aeece2b9f24f15`
- Lokale Ausgabe: `data/processed/fx/bundesbank-usd-annual-fx.csv` und `data/processed/fx/bundesbank-usd-annual-fx.json`
- Versionierter Qualitätsnachweis: `data/quality/fx/bundesbank-usd-annual-fx-check.json`

Regeneration:

```bash
python3 scripts/build_bundesbank_fx.py
```

Nicht-mutierende Prüfung des versionierten Qualitätsnachweises. Wenn die Rohdatei fehlt, lädt der Prüfmodus die hashgeprüfte Quelle in ein temporäres Verzeichnis, nicht nach `data/raw/`:

```bash
python3 scripts/build_bundesbank_fx.py --check
```

Strikt offline prüfen, wenn die Rohdatei bereits unter `data/raw/bundesbank/i-10-wechselkurse.pdf` liegt:

```bash
python3 scripts/build_bundesbank_fx.py --check --no-download
```

## Methodische Einordnung

- Die Bundesbank-PDF weist jährliche Durchschnittskurse aus.
- Die Quelleneinheit lautet für die erste Tabelle `1 Deutsche Mark = ... USD` und für die zweite Tabelle `1 euro = ... USD`.
- Das Skript erzeugt daraus `reciprocalLocalCurrencyPerUsd = 1 / usdPerLocalCurrency`. Das ist der Reziprokwert des Jahresdurchschnitts, nicht zwingend der Jahresdurchschnitt täglicher inverser Kurse.
- Für eine durchgehende EUR-äquivalente Hilfsreihe vor 1999 nutzt das Skript den festen Umrechnungskurs `1 EUR = 1,95583 DM`; auch diese Hilfsreihe ist reziprok abgeleitet.
- Die Reihe ist noch nicht mit den Shiller-Renditen verbunden. Vor Modellintegration müssen Periodisierung und Wechselkurskonvention geprüft werden.
