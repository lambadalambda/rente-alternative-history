# Renten-Alternative-History

Eine deutschsprachige, datenjournalistische Website über ein kontrafaktisches Gedankenexperiment: Was wäre rechnerisch passiert, wenn seit der Rentenreform 1957 unter Konrad Adenauer etwas höhere Beiträge und etwas niedrigere Rentenausgaben einen langfristigen Reservefonds aufgebaut hätten?

Die zentrale These wird nicht vorausgesetzt. Das Projekt soll prüfen, ob und unter welchen Annahmen eine teilweise Kapitaldeckung spätere Rentenzahlungen teilweise oder vollständig hätte finanzieren können.

## Ziel

- Eine moderne, statisch hostbare Website auf Deutsch bauen.
- Historische Rentenfinanzen, Kapitalmarktdaten und Modellannahmen transparent referenzieren.
- Interaktive Szenarien ermöglichen: Beitragsaufschlag, Rentenverzicht, Startjahr, Index/Portfolio, Kosten sowie reale/nominale Betrachtung.
- Schöne, zugängliche Infografiken mit journalistischer Einordnung statt generischem Dashboard entwickeln.
- Auch Ergebnisse zeigen, die die Ausgangsthese schwächen oder widerlegen.

## Grundprinzipien

- Historische Fakten, Modellannahmen, Szenarioergebnisse und Interpretation werden sichtbar getrennt.
- Keine Headline-Zahl ohne Quelle, Annahmenkontext und Hinweis auf Unsicherheit.
- Brutto-Fondsvermögen wird nie ohne kumulierten Aufbaupreis und Hinweis auf Modellgrenzen als Erfolg dargestellt.
- DAX, S&P 500 und Weltindex-Szenarien werden als Vergleichsrechnungen behandelt, nicht automatisch als historisch realistische Staatsfondsstrategie.
- Die Website ist keine Anlageberatung und keine parteipolitische Kampagne.

## Projektstatus

Dieses Repository befindet sich in der Prototyp- und Recherchephase. Die erste Website ist bewusst frameworklos gebaut und statisch hostbar; DRV-PDF-Extraktion, Modelltests und erste lokale Rendite-/FX-Hilfspipelines sind automatisiert, aber noch nicht vollständig modellintegriert oder publikationsfreigegeben.

Die offenen Arbeitspakete liegen im repo-lokalen Issue-Tracker:

- `meta/issues.md`
- `meta/issues/`
- `meta/issues_archive.md`

## Geplante Datenbereiche

- Rentenreform 1957, Umlageverfahren, dynamische Rente und spätere Reformbrüche.
- Beitragseinnahmen, Rentenausgaben, Bundeszuschüsse, Beitragssätze, Nachhaltigkeitsrücklage und Rentnerzahlen.
- Wiedervereinigung, DDR-Rentenüberleitung und Änderungen des Bundesgebiets beziehungsweise der institutionellen Abgrenzung.
- Inflation, DM-/Euro-/USD-Wechselkursbehandlung, nominale und reale Größen.
- Kapitalmarktdaten für DAX, S&P 500 und mindestens eine global diversifizierte Alternative.
- Kosten, Steuern, Dividendenbehandlung, Total-Return/Price-Return-Unterscheidung und historisch plausible Investmentpolitik.

## Reproduzierbarkeit

Langfristiges Ziel ist ein nachvollziehbarer Datenfluss:

```text
Rohquellen -> bereinigte Tabellen -> Annahmenregister -> Modelloutputs -> Website-Daten -> Infografiken
```

Jede Datenquelle soll Herausgeber, URL, Abrufdatum, Lizenz-/Nutzungshinweis, Vertrauensniveau und bekannte Einschränkungen enthalten. Wenn Rohdaten nicht frei weiterverbreitet werden dürfen, werden stattdessen die exakten Reproduktionsschritte dokumentiert.

Aktuelle Planungsartefakte:

- `meta/methodik/modellgovernance.md`: Regeln für Claims, Falsifikation, Aufbaupreis, optionale Übergangskosten und Veröffentlichung.
- `assumptions/register.yaml`: versioniertes Register zentraler Annahmen und offener Entscheidungen.
- `data/manifest.yaml`: Grundstruktur des Datenmanifests.
- `meta/research/drv-zeitreihen-inventar.md`: erstes Inventar der DRV-Zeitreihenquelle.
- `data/extracted/drv/README.md`: Reproduktionshinweise für die aktuelle DRV-Cashflow-Extraktion.

## Entwicklung

Die erste Basiswebsite ist bewusst ohne Framework angelegt und kann direkt statisch gehostet werden.

Lokal ansehen:

```bash
python3 -m http.server 4173
```

Danach im Browser öffnen: `http://localhost:4173/`

Einfache Syntaxchecks:

```bash
node --check assets/app.js
node --check assets/model.js
node --check scripts/test_model.js
node scripts/test_model.js
python3 -m py_compile scripts/build_bundesbank_fx.py scripts/build_drv_cashflows.py scripts/build_shiller_returns.py scripts/build_us_equity_eur_returns.py scripts/validate_aum_comparisons.py scripts/validate_drv_corrections.py scripts/validate_drv_spotchecks.py
python3 scripts/build_bundesbank_fx.py --check
python3 scripts/build_shiller_returns.py --check
python3 scripts/build_us_equity_eur_returns.py --check
python3 scripts/validate_drv_spotchecks.py
python3 scripts/validate_drv_corrections.py --check --no-download
python3 scripts/validate_aum_comparisons.py
python3 -m json.tool data/website/allgemeine-rv-cashflows.json >/dev/null
python3 -m json.tool data/website/aum-comparisons.json >/dev/null
python3 -m json.tool data/quality/drv/rv-in-zeitreihen-korrekturseiten-check.json >/dev/null
python3 -m json.tool data/quality/fx/bundesbank-usd-annual-fx-check.json >/dev/null
python3 -m json.tool data/quality/returns/shiller-return-pipeline-check.json >/dev/null
python3 -m json.tool data/quality/returns/shiller-us-equity-eur-equivalent-check.json >/dev/null
ruby -e 'require "yaml"; YAML.load_file("assumptions/register.yaml"); YAML.load_file("data/manifest.yaml")'
```

DRV-Cashflow-Daten neu erzeugen:

```bash
python3 scripts/build_drv_cashflows.py
```

Voraussetzung: `pdftotext` aus Poppler oder Xpdf muss lokal verfügbar sein. Das Skript lädt die DRV-PDF nach `data/raw/drv/`, prüft den SHA-256-Hash, extrahiert die Tabellen `Einnahmen allg. RV` und `Ausgaben allg. RV` mit `pdftotext -layout` und schreibt die Zwischentabelle sowie die Website-Daten neu. Der Prüfmodus `--check` lädt bewusst keine Rohdaten nach; falls `data/raw/drv/rv_in_zeitreihen_2025.pdf` fehlt, zuerst den Rebuild ausführen.

Vorhandene Pipeline-Artefakte prüfen, wenn der Roh-PDF-Download bereits vorhanden ist:

```bash
python3 scripts/build_drv_cashflows.py --check --no-download
python3 scripts/validate_drv_corrections.py --check --no-download
```

Manuelle DRV-Stichproben gegen die Originaltabellen liegen in `data/quality/drv/allgemeine-rv-cashflow-spotchecks.json` und werden mit `python3 scripts/validate_drv_spotchecks.py` gegen die extrahierte CSV und die Website-JSON geprüft. Der automatische Korrekturseitencheck liegt unter `data/quality/drv/rv-in-zeitreihen-korrekturseiten-check.json`; er prüft, dass die bekannten Korrekturseiten v=3 die aktuell modellierten Inhaltsseiten `244` und `245` nicht betreffen.

Die erste Kapitalmarkt-Pipeline erzeugt einen Robert-Shiller-Forschungsproxy für jährliche US-Aktienmarktrenditen:

```bash
python3 scripts/build_shiller_returns.py
python3 scripts/build_shiller_returns.py --check
```

Die vollständige generierte Reihe liegt nur lokal unter `data/processed/returns/` und wird wegen ungeklärter Weiterverbreitungsrechte nicht versioniert. Versioniert ist der Qualitätsnachweis `data/quality/returns/shiller-return-pipeline-check.json`. Die Reihe ist noch nicht an Wechselkurse, deutsche Inflation oder das interaktive Modell angebunden.

Die erste Wechselkurs-Pipeline erzeugt Bundesbank-Jahresdurchschnittskurse für USD gegen DM/EUR:

```bash
python3 scripts/build_bundesbank_fx.py
python3 scripts/build_bundesbank_fx.py --check
```

Die vollständige generierte FX-Reihe liegt nur lokal unter `data/processed/fx/`. Versioniert ist der Qualitätsnachweis `data/quality/fx/bundesbank-usd-annual-fx-check.json`.

Eine lokale Hilfsrechnung kombiniert den Shiller-US-Renditeproxy mit der Bundesbank-FX-Reihe:

```bash
python3 scripts/build_us_equity_eur_returns.py
python3 scripts/build_us_equity_eur_returns.py --check
```

Sie liegt nur unter `data/processed/returns/`; versioniert ist `data/quality/returns/shiller-us-equity-eur-equivalent-check.json`. Diese Hilfsrechnung ist ausdrücklich nicht modellfreigegeben.

Ein Produktionsbuild ist für diese reine Static-Version nicht nötig; GitHub Pages kann den Repository-Root ausliefern. Später kann ein Build-Schritt ergänzt werden, sobald Datenextraktion, Modelltests und Accessibility-Checks automatisiert sind.

## Korrekturen

Für die Veröffentlichung ist ein sichtbarer Korrekturprozess vorgesehen. Fehler in Daten, Modell oder Text sollen versioniert korrigiert und im Änderungslog nachvollziehbar gemacht werden.

## Lizenz

Noch offen. Code, Texte, Grafiken und Daten können unterschiedliche Lizenzbedingungen brauchen, weil externe Datensätze teils nicht frei weiterverbreitet werden dürfen.
