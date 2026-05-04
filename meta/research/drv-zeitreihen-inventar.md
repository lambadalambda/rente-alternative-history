# DRV-Zeitreihen-Inventar

Stand: 2026-05-04

Status: Erstinventar mit erster PDF-Text-Extraktion für die allg.-RV-Cashflows. Noch keine finale Modellgrundlage.

## Geprüfte Quellen

| Quelle | Status | Ergebnis |
| --- | --- | --- |
| `Rentenversicherung in Zeitreihen 2025` PDF | per `scripts/build_drv_cashflows.py` herunterladbar, hashgeprüft und für die Tabellen 244-245 per `pdftotext -layout` extrahiert | zentrale Quelle für Finanzdaten, Versicherte, Bemessungswerte, Demografie und Volkswirtschaft |
| `ZR_Historie.xlsx` | temporär heruntergeladen und Workbook-Struktur geprüft | nicht die Hauptquelle ab 1957; enthält ein Tabellenblatt für 1891-1956 |
| Korrekturseiten | gefunden, aber noch nicht heruntergeladen | vor finaler Extraktion zwingend abgleichen |

PDF-Metadaten der geprüften Datei:

- Landingpage: https://www.deutsche-rentenversicherung.de/SharedDocs/Downloads/DE/Statistiken-und-Berichte/statistikpublikationen/rv_in_zeitreihen.html
- PDF: https://www.deutsche-rentenversicherung.de/SharedDocs/Downloads/DE/Statistiken-und-Berichte/statistikpublikationen/rv_in_zeitreihen.pdf?__blob=publicationFile&v=9
- Stand laut Landingpage: 13.10.2025
- Auflage laut Landingpage: 31
- Umfang: 338 PDF-Seiten
- Datei ist laut DRV nicht barrierefrei
- SHA-256 der temporär geprüften Datei: `f41ad3a1c398ac56ad5ac75898ba5c664aa1ef7e6ad98859cb2a622b6293ee07`

## Wichtige Entdeckung zur XLSX-Datei

Die per Suche gefundene Datei `ZR_Historie.xlsx` ist keine maschinenlesbare Haupttabelle für 1957 ff. Das Workbook enthält nach Prüfung ein Tabellenblatt `HistorZR_RV__1891_1956_pub` mit dem Titel:

> Gesetzliche Rentenversicherung: "Historische Zeitreihen" zum Rentenbestand und zu den Einnahmen und Ausgaben

Der Untertitel nennt `Reichsgebiet 1891 bis 1938 und Bundesgebiet 1949 bis 1956`. Für das Kernmodell ab 1957 ist daher zunächst das PDF `Rentenversicherung in Zeitreihen 2025` oder eine noch zu findende maschinenlesbare DRV-Tabelle maßgeblich.

## Relevante Finanzdaten-Tabellen im PDF

| Inhaltsseite | Tabelle | Potenzielle Modellvariablen | Erste Einschätzung |
| --- | --- | --- | --- |
| 238 | Einnahmen RV | Gesamteinnahmen, Beiträge, Bundeszuschuss, zusätzliche Bundeszuschüsse, Vermögenserträge, Erstattungen, sonstige Einnahmen, Einnahmeüberschuss | Wichtig für `RV insgesamt`; enthält Ost/West/gesamtdeutsche Segmente und Fußnoten |
| 239 | Ausgaben RV | Gesamtausgaben, Rentenausgaben, Leistungen zur Teilhabe, Kindererziehung, Beitragserstattungen, Verwaltung, KVdR, PVdR, sonstige Ausgaben | Wichtig für Ausgabenbasis; Rentenausgaben sind nicht gleich Gesamtausgaben |
| 240 | Anteil der KVdR- und PVdR-Ausgaben an den Rentenausgaben der RV | Rentenausgaben, KVdR/PVdR, Renten plus KVdR/PVdR | Wichtig für Brutto-/Netto-Nähe der Rentenzahlungsdefinition |
| 241 | Rentenausgaben nach Rentenartengruppen RV insgesamt | Rentenausgaben, Erwerbsminderung, Altersrenten, Hinterbliebenenrenten | Wichtig, falls die Website Altersrenten separat erklären will |
| 242 | Rentenausgaben nach Rentenartengruppen RV insgesamt - Anteile | Anteile der Rentenarten | Eher erklärend als Cashflow-Basis |
| 243 | Ausgewählte Bundesmittel an die gesetzliche Rentenversicherung | Bundeszuschüsse, zusätzliche Bundeszuschüsse, Beiträge für Kindererziehungszeiten, Erstattungen, Bundeszuschuss an KnV | Wichtig für fiskalische Nettoposition und Bundeshaushaltsnähe |
| 244 | Einnahmen allg. RV | Einnahmen allgemeine RV, Beiträge, Bundeszuschuss, Ausgleichszahlungen zwischen allg. RV und KnV | Wahrscheinlich sauberere Baseline als `RV insgesamt`, aber KnV-Behandlung klären |
| 245 | Ausgaben allg. RV | Ausgaben allgemeine RV, Rentenausgaben, KVdR/PVdR, Ausgleichszahlungen | Wichtig für Baseline `allgemeine RV` |
| 246 | Anteil der KVdR- und PVdR-Ausgaben an den Rentenausgaben allg. RV | Rentenausgaben plus Gesundheits-/Pflegezuschüsse | Wichtig für Deckungsdefinition |
| 247 | Rentenausgaben nach Rentenartengruppen allg. RV | Rentenausgaben nach Arten | Erklärung und Altersrenten-Sensitivität |
| 248 | Rentenausgaben nach Rentenartengruppen allg. RV - Anteile | Anteile | Eher erklärend |
| 249 | Nachhaltigkeitsrücklage und Bar- und Anlagevermögen allg. RV | Rücklage, Monatsausgaben, Bar- und Anlagevermögen | Wichtig zur Abgrenzung realer Rücklage vs. hypothetischer Fonds |
| 250 | Einnahmen KnV | Knappschaftliche Rentenversicherung: Einnahmen, Bundeszuschuss, Ausgleichszahlungen | Wichtig, falls `RV insgesamt` modelliert wird |
| 251 | Ausgaben KnV | KnV-Ausgaben und Rentenausgaben | Wichtig für Konsolidierung |
| 252 | Ausgaben für Leistungen der Kindererziehung | Kindererziehungsleistungen nach Versicherungszweigen | Wichtig für versicherungsfremde Leistungen und Bundesmittel-Kontext |
| 253 | Ausgewählte Einnahmen der gesetzlichen Rentenversicherung | noch nicht detailliert extrahiert | Prüfen |
| 254 | Vereinfachter Rentnerquotient allg. RV | Rentnerquotient | Nützlich für Kontext, nicht primäre Cashflow-Basis |

## Priorisierte Modellvariablen aus DRV

| Variable | Bevorzugte Tabelle | Offene Abgrenzung |
| --- | --- | --- |
| Beitragseinnahmen | Einnahmen allg. RV oder Einnahmen RV | allgemeine RV vs. RV insgesamt; interne Ausgleichszahlungen; Pflichtbeiträge vs. Beiträge insgesamt |
| Rentenausgaben | Ausgaben allg. RV oder Ausgaben RV | Rentenausgaben ohne KVdR/PVdR vs. Renten plus KVdR/PVdR vs. Gesamtausgaben |
| Bundeszuschüsse | Ausgewählte Bundesmittel; Einnahmen allg. RV/RV | allgemeiner Bundeszuschuss, zusätzlicher Bundeszuschuss, Bundesmittel insgesamt |
| Vermögenserträge realer RV | Einnahmen RV/allg. RV | nicht mit hypothetischen Fondsrenditen vermischen |
| Nachhaltigkeitsrücklage | Nachhaltigkeitsrücklage und Bar-/Anlagevermögen | echte Umlage-Rücklage vs. hypothetischer Kapitalfonds |
| Ausgleich allg. RV/KnV | Einnahmen/Ausgaben allg. RV und KnV | Konsolidierung verhindert Doppelzählung |
| KVdR/PVdR | Ausgaben- und Anteil-Tabellen | entscheiden, ob als Rentenzahlung oder separate Sozialausgabe gewertet |

## Strukturbrüche und Fußnoten, die vor der Modellierung markiert werden müssen

- Viele Tabellen verwenden `Alte Bundesländer` bis 1991 und `Insgesamt` ab 1992.
- Manche Tabellen weisen alte und neue Bundesländer separat aus, aber nicht durchgängig für alle Jahre.
- Mehrere Finanzdatentabellen nennen: `Ab 2004 nur noch Ausweisung für Deutschland insgesamt`.
- Die Quelle verweist bei historischen Beträgen auf `Zur Euro-Umrechnung vgl. Glossar`; die Umrechnung muss geprüft werden.
- Rentenausgaben nach Rentenartengruppen sind ohne Beitragszuschuss zur Krankenversicherung beziehungsweise bis 31.03.2004 zur Pflegeversicherung der Rentner ausgewiesen.
- Von 1999 bis 2010 gibt es Fußnoten zu § 291c SGB VI und einigungsbedingten Leistungen.
- Ab 1992 werden Renten wegen verminderter Erwerbsfähigkeit an Berechtigte ab Regelaltersgrenze als Altersrenten ausgewiesen.
- Eine Rücklage wird laut Fußnote erst ab 1972 als Rücklage/Nachhaltigkeitsrücklage ausgewiesen; frühere Bar- und Anlagevermögen sind anders zu behandeln.
- `x`, `-`, leere Felder und Fußnotenzeichen dürfen bei Extraktion nicht stillschweigend als Null interpretiert werden.

## Vorläufige Baseline-Entscheidung

Für die erste reproduzierbare Cashflow-Rechnung wird `allgemeine RV` verwendet, weil sie im PDF eigene Einnahmen-, Ausgaben- und Rücklagentabellen hat und die normale gesetzliche Rentenversicherung für den Großteil der Beschäftigten besser isoliert. Parallel muss `RV insgesamt` inventarisiert bleiben, weil Website-Leserinnen und -Leser vermutlich die gesamte gesetzliche Rentenversicherung erwarten.

Diese Arbeitsannahme steht in `assumptions/register.yaml` unter `PENSION-001`.

## Extraktionsplan

- Korrekturseiten herunterladen und gegen Finanzdatentabellen prüfen.
- Prüfen, ob es eine offizielle maschinenlesbare Fassung der 2025er Tabellen gibt.
- Wenn nur PDF verfügbar ist, Tabellenextraktion mit dokumentiertem Verfahren und manueller Stichprobenkontrolle vorbereiten. Für `Einnahmen allg. RV` und `Ausgaben allg. RV` existiert ein erster Skriptpfad.
- Jede extrahierte Tabelle mit Inhaltsseite, Tabellenkopf, Fußnoten, Einheit und Gebietsstand speichern.
- Rohdaten, Zwischenstände und finale Modellinputs getrennt halten.
- Keine generierten Tabellen manuell nachbearbeiten.
- Aktuelle Pipeline: `python3 scripts/build_drv_cashflows.py` erzeugt `data/extracted/drv/allgemeine-rv-cashflows.csv` und `data/website/allgemeine-rv-cashflows.json`.

## Offene Fragen

- Wie groß ist der Unterschied zwischen der gesetzten Baseline `allgemeine RV` und einem späteren Vergleich `RV insgesamt`?
- Welche Beitrags- und Ausgabenunterpositionen gehören zur Fondsaufbau-Basis?
- Welche Ausgabenbasis entspricht dem Claim `Rentenzahlungen`: Rentenausgaben, Renten plus KVdR/PVdR oder Gesamtausgaben?
- Wie wird der Sprung 1991/1992 in der Fondsakkumulation und in den Rentenverpflichtungen gezeigt?
- Reicht die PDF-Extraktion für Reproduzierbarkeit, oder muss eine maschinenlesbare DRV-Quelle gefunden werden?
