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

Dieses Repository befindet sich in der Prototyp- und Recherchephase. Die erste Website ist bewusst frameworklos gebaut und statisch hostbar; Datenextraktion, Modelltests und historische Renditeserien folgen noch.

Die offenen Arbeitspakete liegen im repo-lokalen Issue-Tracker:

- `meta/issues.md`
- `meta/issues/`
- `meta/issues_archive.md`

## Geplante Datenbereiche

- Rentenreform 1957, Umlageverfahren, dynamische Rente und spätere Reformbrüche.
- Beitragseinnahmen, Rentenausgaben, Bundeszuschüsse, Beitragssätze, Nachhaltigkeitsrücklage und Rentnerzahlen.
- Wiedervereinigung, DDR-Rentenüberleitung und Änderungen des Bundesgebiets beziehungsweise der institutionellen Abgrenzung.
- Inflation, DEM/EUR/USD-Wechselkurse, nominale und reale Größen.
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
python3 -m json.tool data/website/prototype-allgemeine-rv.json >/dev/null
ruby -e 'require "yaml"; YAML.load_file("assumptions/register.yaml"); YAML.load_file("data/manifest.yaml")'
```

Ein Produktionsbuild ist für diese reine Static-Version nicht nötig; GitHub Pages kann den Repository-Root ausliefern. Später kann ein Build-Schritt ergänzt werden, sobald Datenextraktion, Modelltests und Accessibility-Checks automatisiert sind.

## Korrekturen

Für die Veröffentlichung ist ein sichtbarer Korrekturprozess vorgesehen. Fehler in Daten, Modell oder Text sollen versioniert korrigiert und im Änderungslog nachvollziehbar gemacht werden.

## Lizenz

Noch offen. Code, Texte, Grafiken und Daten können unterschiedliche Lizenzbedingungen brauchen, weil externe Datensätze teils nicht frei weiterverbreitet werden dürfen.
