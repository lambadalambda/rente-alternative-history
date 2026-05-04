# Initiale Datenquellen-Recherche

Abrufdatum dieser Recherche: 2026-05-04

Ziel: Quellen identifizieren, die ein kontrafaktisches Modell zur gesetzlichen Rentenversicherung ab 1957 mit hypothetischer Kapitalanlage nachvollziehbar machen. Diese Datei enthält noch keine finalen Datenwerte und ersetzt kein späteres Datenmanifest.

## Kurzfazit

- Die stärkste Primärquelle für Renten-Zeitreihen ist die Deutsche Rentenversicherung, besonders `Rentenversicherung in Zeitreihen` und die direkte historische XLSX-Datei.
- Für aktuelle und aggregierte Tabellen sind BMAS-Seiten zu GRV-Einnahmen/Ausgaben und `Daten zur Rente` nützlich, aber wahrscheinlich eher ergänzend zu DRV-Zeitreihen.
- Für reale Werte ist Destatis mit den Verbraucherpreisindex-Langreihen ab 1948 die belastbare Quelle.
- Für Wechselkurse, Bundesanleiherenditen, DAX-/Kapitalmarkt-Zeitreihen und SDMX-Zugriff ist die Bundesbank zentral.
- Indexrenditen sind der schwierigste Teil: DAX vor 1987, S&P-500-Total-Return-Daten, MSCI/FTSE-Weltindizes und Lizenzrechte müssen sehr vorsichtig behandelt werden.
- Der wichtigste Modellhinweis bleibt: Fondsvermögen allein reicht nicht. Aufbaupreis und bei echten Beitragsumleitungen auch Übergangskosten müssen mitgerechnet werden.

## Empfohlene Kernquellen

| Bereich | Quelle | Herausgeber | URL | Datenbereich / Zeitraum | Lizenz / Nutzung | Vertrauensniveau | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GRV-Zeitreihen | Rentenversicherung in Zeitreihen | Deutsche Rentenversicherung | https://www.deutsche-rentenversicherung.de/SharedDocs/Downloads/DE/Statistiken-und-Berichte/statistikpublikationen/rv_in_zeitreihen.html | Langfristige Reihen zur gesetzlichen Alterssicherung; laut Fundstelle Datenstand Mitte Oktober 2025 | Nutzungshinweis prüfen | Hoch, amtliche Statistik | Tabellen, Abgrenzungen und Brüche müssen je Variable geprüft werden |
| GRV-Zeitreihen | Historische Zeitreihe XLSX | Deutsche Rentenversicherung / Statistikportal | https://statistik-rente.de/drv/extern/zeitreihen/rv_in_zeitreihen/documents/ZR_Historie.xlsx | Nach späterer Prüfung: 1891-1956, nicht Hauptquelle für das Modell ab 1957 | Nutzungshinweis prüfen | Hoch, amtliche Statistik | Für historischen Kontext nützlich; Hauptmodell nutzt zunächst die PDF-Publikation |
| GRV-Finanzen | Einnahmen und Ausgaben der GRV | BMAS | https://www.bmas.de/SharedDocs/Downloads/DE/Soziale-Sicherung/einnahmen-und-ausgaben-der-gesetzlichen-rentenversicherung-grv.html | Einnahmen/Ausgaben der gesetzlichen Rentenversicherung | Nutzungshinweis prüfen; BMAS Open-Data-Kontext prüfen | Hoch, ministerielle Quelle | Datenbereich und maschinenlesbare Formate noch extrahieren |
| Rentenbericht | Rentenversicherungsbericht / Alterssicherungsbericht | BMAS | https://www.bmas.de/DE/Soziales/Rente-und-Altersvorsorge/rentenversicherungsbericht-art.html | Historische, aktuelle und projizierte GRV-Entwicklung | Nutzungshinweis prüfen | Hoch, Regierungsbericht | Projektionen nicht mit historischen Daten vermischen |
| Rentenbestand | Rentenbestandsstatistik | BMAS | https://www.bmas.de/DE/Service/Statistiken-Open-Data/Rentenbestandsstatistik/rentenbestandsstatistik.html | Rentenbestand, laut Recherche mindestens jüngere Jahre | Open-Data-Kontext prüfen | Hoch | Für lange Reihen vermutlich nicht ausreichend |
| Beitragssätze | Beitragssätze ab 1957 | Bundesamt für Soziale Sicherung | https://www.bundesamtsozialesicherung.de/fileadmin/redaktion/Rentenversicherung/Beitraege/Beitragssaetze_ab_1957.pdf | Beitragssätze der gesetzlichen Rentenversicherung ab 1957 | Nutzungshinweis prüfen | Hoch, Bundesbehörde | PDF muss in strukturierte Tabelle überführt werden |
| Historischer Kontext | Bundestag: Rentenreform 1957 | Deutscher Bundestag | https://www.bundestag.de/dokumente/textarchiv/1957-01-21-rentenreform-488538 | Kontext zur Reform, dynamische Rente, parlamentarischer Beschluss | Bundestag-Nutzungshinweise prüfen | Hoch für Kontext, keine Modelldaten | Nicht als Zahlenquelle für Modellcashflows verwenden |
| Historischer Kontext | BGBl. I 1957 S. 45 | Bundesgesetzblatt / Dejure-Spiegel | https://dejure.org/BGBl/1957/BGBl._I_S._45 | Arbeiterrentenversicherungs-Neuregelungsgesetz vom 23.02.1957 | Amtliche Fundstelle möglichst über BGBl. prüfen | Hoch für Rechtskontext | Dejure ist bequem, amtliche Quelle bevorzugen |
| Inflation | Verbraucherpreisindex lange Reihen ab 1948 | Destatis | https://www.destatis.de/DE/Themen/Wirtschaft/Preise/Verbraucherpreisindex/Publikationen/Downloads-Verbraucherpreise/statistischer-bericht-verbraucherpreisindex-lange-reihen-5611103.html | Monats- und Jahreswerte, lange Reihen ab 1948 | Destatis Open Data / Datenlizenz Deutschland 2.0 prüfen | Sehr hoch, amtliche Statistik | Basiswechsel und Gebietsstände dokumentieren |
| Inflation API | GENESIS-Online API | Destatis | https://www.destatis.de/EN/Service/OpenData/api-webservice.html | Automatisierter Zugriff auf amtliche Tabellen | Datenlizenz Deutschland - Namensnennung 2.0 laut Destatis-Kontext | Sehr hoch | Tabellen-IDs und API-Parameter noch festlegen |
| Open Data | Destatis Open Data | Destatis | https://www.destatis.de/EN/Service/OpenData/_node.html | Lizenz- und API-Hinweise | Open Data / Datenlizenz Deutschland | Sehr hoch | Lizenztext je konkretem Datensatz prüfen |
| Wechselkurse | Bundesbank Wechselkurse | Deutsche Bundesbank | https://www.bundesbank.de/de/statistiken/wechselkurse | Wechselkurse, Referenzkurse, historische Reihen | Nutzungshinweis prüfen | Hoch | DEM/EUR/USD-Methodik und fixe Euro-Umrechnung dokumentieren |
| Bundesbank API | Zeitreihen-Datenbanken / SDMX | Deutsche Bundesbank | https://www.bundesbank.de/de/statistiken/zeitreihen-datenbanken | CSV- und SDMX-Downloads | Nutzungshinweis prüfen | Hoch | Bundesbank weist auf neue Statistik-Infrastruktur hin; Zugriffspfade stabilisieren |
| Kapitalmarkt Deutschland | Renditen und Indizes deutscher Wertpapiere | Deutsche Bundesbank | https://www.bundesbank.de/de/statistiken/geld-und-kapitalmaerkte/wertpapieremissionen/nr-05-renditen-und-indizes-deutscher-wertpapiere-650634 | Deutsche Kapitalmarktindizes, Renditen, DAX/CDAX-Kontext | Nutzungshinweis prüfen | Hoch | Seriencodes und Startdaten noch identifizieren |
| Bundesanleihen | Umlaufsrenditen | Deutsche Bundesbank | https://www.bundesbank.de/de/statistiken/geld-und-kapitalmaerkte/zinssaetze-und-renditen/umlaufsrenditen/umlaufsrenditen-772416 | Renditen börsennotierter Bundeswertpapiere | Nutzungshinweis prüfen | Hoch | Für Schulden-/Diskontierungsannahmen geeignet, aber Laufzeitwahl definieren |
| DAX offiziell | DAX Factsheet | STOXX / Deutsche Börse Gruppe | https://www.dax-indices.com/document/Resources/Guides/Factsheet_DAX%20EUR_NR.pdf | DAX-Methodik und aktuelle Indexdaten; offizielles Basisdatum 30.12.1987 | Indexanbieter-Lizenz prüfen | Hoch für offizielle Methodik | DAX vor 1987 ist rückgerechnet oder Proxy, nicht einfach historische ETF-Anlage |
| Deutsche Aktienrenditen | Returns on German Stocks 1954 to 2013 | Wissenschaftliche Quelle / HU Berlin | https://edoc.hu-berlin.de/bitstreams/b8f049e3-37d0-48f4-b891-98d1c1217f7a/download | Deutsche Aktienrenditen inkl. Total-Return-Rekonstruktion 1954-2013 laut Recherche | Publikations-/Datenlizenz prüfen | Mittel bis hoch für Backtesting | Methodik, Delistings und Replizierbarkeit genau prüfen |
| S&P 500 offiziell | S&P 500 Index | S&P Dow Jones Indices | https://www.spglobal.com/spdji/en/indices/equity/sp-500/ | Offizielle Indexinformationen, Price und Total Return je nach Zugang | Lizenzpflichtig / Nutzungsbedingungen prüfen | Hoch | Rohdatenveröffentlichung wahrscheinlich eingeschränkt |
| S&P 500 wissenschaftlich | CRSP Historical Indexes Guide | CRSP | https://www.crsp.org/wp-content/uploads/guides/CRSP_Historical_Indexes_Guide.pdf | Historische US-Indexserien, inkl. Delisting-Returns laut Recherche | Lizenzpflichtig | Sehr hoch | Institutioneller Datenzugang nötig |
| S&P 500 Proxy | Robert Shiller Online Data | Robert J. Shiller / Yale | http://www.econ.yale.edu/~shiller/data.htm | Monatliche US-Aktienmarktpreise, Dividenden, Earnings, CPI ab 1871 | Nutzungshinweis prüfen | Hoch als Forschungsproxy | Kein offizieller S&P-500-Total-Return-Index; Rekonstruktion nötig |
| S&P 500 freie Vergleichsdaten | S&P 500 TR bei Yahoo Finance / Slickcharts / Investing.com | Kommerzielle Finanzportale | https://finance.yahoo.com/quote/%5ESP500TR/history/ | Total-Return- oder Jahresrenditen je Portal | Nutzungsbedingungen meist restriktiv | Mittel als Plausibilitätscheck | Nicht als frei redistribuierbare Primärdaten einplanen |
| Weltindex | MSCI Indexes | MSCI | https://www.msci.com/indexes | MSCI World und andere Indizes; Backhistory oft ab 1969 | Lizenzpflichtig | Hoch | Historie startet nicht 1957; Lizenz und Backfill markieren |
| Weltindex Alternative | FTSE All-World Index | LSEG / FTSE Russell | https://www.lseg.com/en/ftse-russell/indices/ftseall-world | Globale Aktienindizes und Methodik | Lizenzpflichtig | Hoch | Lizenz und historische Verfügbarkeit prüfen |
| Weltindex Methodik | FTSE Global Equity Index Series Guide | LSEG / FTSE Russell | https://www.lseg.com/content/dam/ftse-russell/en_us/documents/ground-rules/ftse-global-equity-index-series-guide-to-calc.pdf | Total-Return- und Indexberechnungsmethodik | Nutzungshinweis prüfen | Hoch für Methodik | Nicht automatisch Datenlizenz |
| Internationale Einordnung | Pensions at a Glance | OECD | https://www.oecd.org/en/publications/pensions-at-a-glance-2025_e40274c1-en/full-report/public-expenditure-on-pensions_ddc9a2dd.html | Internationale Rentenausgabenvergleiche | OECD-Nutzungshinweise prüfen | Mittel bis hoch für Kontext | Startet für viele Reihen nicht 1957; nicht primär für GRV-Cashflows |
| Demografie | Population projections | Eurostat | https://ec.europa.eu/eurostat/web/population-demography/population-projections | Demografische Projektionen | Eurostat-Nutzungshinweise prüfen | Hoch für Kontext und Zukunftsszenarien | Projektionen sind Annahmen, keine historischen Cashflows |

## Modellvariablen und bevorzugte Quellen

| Modellvariable | Bevorzugte Quelle | Ersatz / Plausibilitätscheck | Status |
| --- | --- | --- | --- |
| Beitragseinnahmen GRV | DRV `Rentenversicherung in Zeitreihen` / `ZR_Historie.xlsx` | BMAS Einnahmen/Ausgaben GRV | Primärquelle gefunden, Tabellen noch extrahieren |
| Rentenausgaben GRV | DRV `Rentenversicherung in Zeitreihen` / `ZR_Historie.xlsx` | BMAS Einnahmen/Ausgaben GRV | Primärquelle gefunden, Brutto/Netto klären |
| Bundeszuschüsse | DRV / BMAS GRV-Finanztabellen | Haushaltsdaten des Bundes | Quelle gefunden, Abgrenzung klären |
| Beitragssätze | Bundesamt für Soziale Sicherung, DRV | Sozialpolitik aktuell als Sekundärdarstellung | Gut auffindbar |
| Rentnerzahlen / Rentenbestand | DRV Zeitreihen, BMAS Rentenbestandsstatistik | DRV `RV in Zahlen` | Gut auffindbar, lange Reihe prüfen |
| Nachhaltigkeitsrücklage | DRV Geschäftsberichte / Zeitreihen | Rentenversicherungsbericht | Aktuelle Quelle gefunden, historische Reihe prüfen |
| Inflation / Realwerte | Destatis CPI lange Reihen ab 1948 | GENESIS API | Sehr gut auffindbar |
| DEM/USD und EUR/USD | Bundesbank Wechselkurse / SDMX | DBnomics BUBA als Mirror | Quelle gefunden, Seriencodes fehlen |
| Schuldenzins / Diskontierung | Bundesbank Umlaufsrenditen / Termstruktur | Bundesbank Kapitalmarktkennzahlen | Quelle gefunden, Laufzeitannahme fehlt |
| DAX Total Return | Offizielle DAX-Methodik plus Bundesbank/deutsche Aktienrendite-Backseries | HU Berlin Backseries, CDAX/Commerzbank-Proxys | Kritisch wegen Basisdatum und Lizenz |
| S&P 500 Total Return | S&P/CRSP bei Lizenzzugang | Shiller-Daten als Forschungsproxy, Yahoo/Slickcharts nur Plausibilität | Kritisch wegen Lizenz und offizieller TR-Serie |
| Weltindex | MSCI World / FTSE All-World bei Lizenzzugang | wissenschaftliche Weltaktienrenditen, Proxy-Portfolio | Kritisch wegen Startdatum 1969 und Lizenz |
| Kosten / Steuern | Explizite Modellannahmen plus Steuerquellen | KPMG nur als moderne Referenz | Historische Reihen noch offen |

## Offene Risiken

- DAX ist als offizieller Index ab 1987 definiert; ältere Werte müssen als Rückrechnung oder Proxy gekennzeichnet werden.
- MSCI World und viele globale Reihen starten erst ab 1969 oder sind zurückgerechnet; sie decken 1957 nicht ohne Zusatzannahme ab.
- S&P-500-Total-Return-Daten sind qualitativ gut verfügbar, aber offizielle Daten und CRSP sind lizenzpflichtig.
- Shiller-Daten sind ein plausibler Forschungsproxy für US-Aktienrenditen, aber nicht identisch mit einer offiziell investierbaren S&P-500-Total-Return-Reihe.
- Eine echte Umleitung historischer Beitragseinnahmen in einen Fonds erzeugt im Umlagesystem eine Finanzierungslücke; diese muss als Übergangskosten-, Steuer- oder Schuldenpfad modelliert werden. Die aktuelle 5/5-Baseline vermeidet diese Lücke, weil sie zusätzliche Beiträge und niedrigere Rentenausgaben nutzt.
- Westdeutsche Daten 1957-1990 dürfen nicht ohne Annahme mit gesamtdeutschen Verpflichtungen nach 1990 vermischt werden.
- Steuer-, Kosten- und Quellensteuerannahmen können den Endwert stark verändern.
- Bei einem sehr großen öffentlichen Fonds ist die Price-Taker-Annahme unrealistisch; die Website muss das offenlegen.

## Nächste Recherche- und Extraktionsschritte

- DRV-XLSX `ZR_Historie.xlsx` herunterladen, Tabellenblätter inventarisieren und relevante Spalten für Einnahmen, Ausgaben, Bundesmittel, Beitragssätze, Rentenbestand und Rücklagen identifizieren.
- BMAS-GRV-Einnahmen/Ausgaben-Seite extrahieren und prüfen, ob CSV/XLSX statt PDF verfügbar ist.
- Destatis GENESIS-Tabellen-IDs für Verbraucherpreisindex-Jahresdurchschnitte und lange Reihen festlegen.
- Bundesbank-SDMX-Seriencodes für USD/DEM, USD/EUR, DAX/CDAX und Umlaufsrenditen identifizieren.
- Prüfen, ob offizielle Indexdaten in der Website überhaupt redistribuiert werden dürfen oder nur abgeleitete, lizenzkonforme Ergebnisse gezeigt werden können.
- Für DAX vor 1987 eine saubere Proxy-Entscheidung treffen und im Annahmenregister dokumentieren.
- Für S&P 500 entscheiden, ob CRSP/S&P-Lizenzdaten genutzt werden oder ein transparenter Shiller-Proxy reicht.
- Für Weltindex-Szenarien entscheiden, ob die Reihe erst 1969 startet oder 1957-1969 mit einem plausiblen Proxy überbrückt wird.
