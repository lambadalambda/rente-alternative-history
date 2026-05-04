# Renten-Alternative-History

Eine deutschsprachige, datenjournalistische Website über ein kontrafaktisches Gedankenexperiment: Was wäre rechnerisch passiert, wenn seit der Rentenreform 1957 unter Konrad Adenauer ein Teil der Mittel der gesetzlichen Rentenversicherung nicht vollständig im Umlageverfahren ausgegeben, sondern in einen langfristigen Reservefonds investiert worden wäre?

Die zentrale These wird nicht vorausgesetzt. Das Projekt soll prüfen, ob und unter welchen Annahmen eine teilweise Kapitaldeckung spätere Rentenzahlungen teilweise oder vollständig hätte finanzieren können.

## Ziel

- Eine moderne, statisch hostbare Website auf Deutsch bauen.
- Historische Rentenfinanzen, Kapitalmarktdaten und Modellannahmen transparent referenzieren.
- Interaktive Szenarien ermöglichen: Anlagequote, Startjahr, Index/Portfolio, Kosten, reale/nominale Betrachtung und Übergangsfinanzierung.
- Schöne, zugängliche Infografiken mit journalistischer Einordnung statt generischem Dashboard entwickeln.
- Auch Ergebnisse zeigen, die die Ausgangsthese schwächen oder widerlegen.

## Grundprinzipien

- Historische Fakten, Modellannahmen, Szenarioergebnisse und Interpretation werden sichtbar getrennt.
- Keine Headline-Zahl ohne Quelle, Annahmenkontext und Hinweis auf Unsicherheit.
- Brutto-Fondsvermögen wird nie ohne Übergangskosten und fiskalischen Nettoeffekt als Erfolg dargestellt.
- DAX, S&P 500 und Weltindex-Szenarien werden als Vergleichsrechnungen behandelt, nicht automatisch als historisch realistische Staatsfondsstrategie.
- Die Website ist keine Anlageberatung und keine parteipolitische Kampagne.

## Projektstatus

Dieses Repository befindet sich in der Planungs- und Recherchephase. Der konkrete Static-Site-Stack ist noch nicht gewählt.

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

## Entwicklung

Noch nicht eingerichtet. Sobald ein Stack gewählt ist, werden hier die Befehle für Entwicklung, Build, Test, Daten-Rebuild und GitHub-Pages-Deployment dokumentiert.

## Korrekturen

Für die Veröffentlichung ist ein sichtbarer Korrekturprozess vorgesehen. Fehler in Daten, Modell oder Text sollen versioniert korrigiert und im Änderungslog nachvollziehbar gemacht werden.

## Lizenz

Noch offen. Code, Texte, Grafiken und Daten können unterschiedliche Lizenzbedingungen brauchen, weil externe Datensätze teils nicht frei weiterverbreitet werden dürfen.
