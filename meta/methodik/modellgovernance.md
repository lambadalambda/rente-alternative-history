# Modellgovernance

Stand: 2026-05-04

Status: Arbeitsentwurf mit Prototyprechnung. Dieses Dokument definiert, welche Aussagen das Projekt prüfen darf. Es enthält noch keine veröffentlichungsreifen Ergebnisse.

## Primärfrage

Wir prüfen, ob und unter welchen Annahmen eine seit der Rentenreform 1957 aufgebaute, teilweise kapitalgedeckte Reserve spätere Rentenausgaben teilweise oder vollständig hätte finanzieren können.

Der 5/5-Verzichtsdeal ist ein Szenarioparameter. Er ist kein vorab bestätigtes Ergebnis.

## Nebenfragen

- Welche historischen Zahlungsströme der gesetzlichen Rentenversicherung eignen sich als Basis für einen hypothetischen Fondsaufbau?
- Was kauft ein kleiner jährlicher Verzicht, wenn 5 Prozent höhere Beiträge und 5 Prozent niedrigere Rentenausgaben langfristig investiert werden?
- Wie unterscheiden sich Brutto-Fondsvermögen, kumulierter Aufbaupreis und Kapitalertrag über diesen Aufbaupreis hinaus?
- Wie sensibel sind Ergebnisse gegenüber Indexwahl, Startjahr, Kosten, Steuern, Wechselkursen, Inflation und Entnahmeregel?
- Welche Szenarien sind bloße Vergleichsrechnungen mit rückblickenden Indexdaten und welche kommen einer historisch plausibleren öffentlichen Investmentpolitik näher?

## Aussagekategorien

Jede spätere Headline-Zahl muss einer dieser Kategorien zugeordnet werden:

| Kategorie | Bedeutung | Zulässige Formulierung |
| --- | --- | --- |
| Historischer Fakt | Direkt aus einer Quelle belegte historische Angabe | "Die DRV weist für Jahr X Beitragseinnahmen von Y aus." |
| Rekonstruktion | Aus Quellen abgeleiteter Wert mit Transformationsschritt | "Nach Umrechnung in Euro und Preisbasis X ergibt sich Y." |
| Modellannahme | Nicht beobachtete Setzung für das kontrafaktische Szenario | "Das Szenario setzt 5 Prozent höhere Beiträge und 5 Prozent niedrigere Rentenausgaben an." |
| Modelloutput | Ergebnis einer definierten Rechnung | "Unter Annahmen A, B und C berechnet das Modell Y." |
| Interpretation | Einordnung des Outputs | "Das spricht dafür, dass der Befund stark vom Aufbaupreis abhängt." |

## Nicht-Claims

Diese Aussagen sind ohne weitere Einschränkung verboten:

- "10 Prozent investiert hätten alle Renten bezahlt."
- "Deutschland hätte heute X Billionen Euro."
- "Das Umlagesystem war historisch eindeutig die falsche Entscheidung."
- "Ein S&P-500-, DAX- oder Weltindex-Szenario war seit 1957 politisch und institutionell automatisch realistisch."
- "Die Rentenprobleme wären gelöst gewesen."

Zulässig sind vorsichtige, belegbare Formulierungen:

- "Unter Annahme X ergibt das Modell Y."
- "Dieses Szenario finanziert den Fonds über höhere Beiträge und niedrigere Rentenausgaben."
- "Der Befund hängt sichtbar von Indexwahl, Kosten, Steuern und der Definition der investierten Cashflows ab."

## Definition von Deckung

"Rentenzahlungen aus Fondserträgen decken" ist mehrdeutig. Die Website darf erst dann von Deckung sprechen, wenn die verwendete Definition sichtbar benannt ist.

| Metrik | Definition | Einschränkung |
| --- | --- | --- |
| Brutto-Fondsvermögen | Fondsbestand am Jahresende | Kein Wohlfahrts- oder Fiskalvergleich ohne Aufbaupreis |
| Aufbaupreis | Kumulierte zusätzliche Beiträge plus kumulierte eingesparte Rentenausgaben | Zeigt den jährlichen Verzicht ohne Opportunitätsverzinsung |
| Kapitalertrag über Aufbaupreis | Fondsbestand minus kumulierter Aufbaupreis | Keine vollständige Wohlfahrtsrechnung, aber verständlicher Vergleichswert |
| Jahresrendite brutto | Wertänderung des Fonds in einem Jahr vor Kosten/Steuern | Kann in Krisenjahren negativ sein |
| Jahresrendite netto | Wertänderung nach Kosten, Steuern und Währungseffekten | Braucht explizite Annahmen |
| Nachhaltige Entnahme | Regelbasierte Entnahme, die den Fonds nicht sofort aufzehrt | Keine Garantie für einzelne Krisenpfade |
| Deckungsquote | Zulässige Fondsfinanzierung geteilt durch gewählte Rentenausgaben | Nur interpretierbar mit klarer Ausgabenbasis |

Ein Szenario darf nicht als "vollständig gedeckt" gelten, wenn es nur Brutto-Fondsvermögen zeigt, aber den jährlichen Aufbaupreis aus höheren Beiträgen und niedrigeren Renten ausblendet.

## Mindestmodell vor öffentlicher Aussage

Vor jeder öffentlichen Ergebniszahl braucht das Modell mindestens diese Bausteine:

- Historische Jahresreihe für Beitragseinnahmen oder eine andere begründete Cashflow-Basis.
- Historische Jahresreihe für Rentenausgaben mit klarer Brutto-/Netto-Abgrenzung.
- Aufbaupfad und Investmentpolitik mit dokumentiertem Status als Annahme oder Vergleichsrechnung.
- Jährlicher Aufbaupreis durch zusätzliche Beiträge und/oder niedrigere Rentenausgaben.
- Kosten-, Steuer-, Inflations- und Währungsannahmen oder eine sichtbare Markierung, dass sie noch fehlen.
- Sensitivitäten für mindestens konservatives, mittleres, optimistisches und adverses Szenario.

## Aufbaupreisregel

Die Baseline leitet keine Beiträge aus der Umlage ab, sondern finanziert den Fonds über einen expliziten Verzichtsdeal. Das Modell muss deshalb je Jahr zeigen:

- zusätzliche Beiträge,
- eingesparte Rentenausgaben,
- Fonds-Einzahlung,
- kumulierten Aufbaupreis,
- Brutto-Fondsvermögen,
- Kapitalertrag über den Aufbaupreis hinaus.

Szenarien, die in Zukunft echte Beitragsumleitungen ohne Rentenkürzung modellieren, müssen weiterhin entgangene Umlageeinnahmen, Ersatzfinanzierung und mögliche Schuldenpfade zeigen. Die aktuelle Baseline braucht das nicht, weil keine historischen Beiträge aus der Umlage abgezogen werden; der Fonds entsteht aus zusätzlichen Beiträgen und niedrigeren Rentenausgaben.

## Index- und Renditeregeln

Jede Renditeserie braucht diese Angaben:

- Indexname und Anbieter oder Rekonstruktionsquelle,
- Total Return oder Price Return,
- Brutto-, Netto- oder Preisindexstatus,
- Währung,
- nominale oder reale Betrachtung mit Preisbasis,
- Kosten, Steuern und Quellensteuerannahmen,
- Start- und Enddatum,
- Rebalancing-Regel,
- Hinweise auf Backfill, Survivorship Bias, Delisting-Behandlung und historische Investierbarkeit.

Moderne Indexbacktests dürfen nicht als automatisch investierbare Politikoption für 1957 dargestellt werden.

## Falsifikationsregeln

Die Website muss die Ausgangsthese sichtbar schwächen oder verwerfen, wenn eine der folgenden Bedingungen eintritt:

- Der Fonds wirkt nur groß, solange der kumulierte Aufbaupreis ausgeblendet wird.
- Die 10-Prozent-Hypothese trägt nur bei optimistischer Indexwahl, aber nicht bei plausibleren Kosten-, Steuer- oder Portfoliovarianten.
- Der Kapitalertrag über Aufbaupreis bleibt klein oder negativ, obwohl das Brutto-Fondsvermögen groß wirkt.
- Die Datenlage erlaubt keine belastbare Abgrenzung von Beitragseinnahmen, Rentenausgaben oder Gebietsständen.
- Ein zentraler Indexdatensatz darf nicht reproduzierbar oder lizenzkonform genutzt werden.

## Annahmenänderungen

Zentrale Annahmen stehen in `assumptions/register.yaml`. Änderungen brauchen:

- Annahmen-ID,
- Datum,
- Begründung,
- erwartete Richtung des Effekts,
- Alternativen,
- Verweis auf Issue oder Review.

Änderungen werden zusätzlich in `assumptions/changelog.md` dokumentiert. Alte Szenarioergebnisse dürfen nicht stillschweigend durch neue Annahmen überschrieben werden.

## Verifikationsplan

Vor Veröffentlichung von Modelloutputs sind mindestens diese Checks nötig:

- Handgerechnete Beispieljahre für Beitragsaufschlag, Rentenverzicht und Fondsakkumulation.
- Regressionstests für Headline-Zahlen.
- Tests für nominale und reale Umrechnung.
- Tests für DEM/EUR/USD-Umrechnung.
- Tests für Kosten- und Steuerabzug.
- Tests für Beitragsaufschlag, Rentenverzicht, Fonds-Einzahlung und kumulierten Aufbaupreis.
- Datenprovenienzprüfung gegen `data/manifest.yaml`.

## Offene Entscheidungen vor belastbaren Ergebnissen

- Wie wird der Aufbaupfad definiert? Arbeitsannahme 2026-05-04: 5 Prozent höhere Beiträge auf Beitragseinnahmen plus 5 Prozent niedrigere Rentenausgaben.
- Soll die Baseline `RV insgesamt` oder `allgemeine RV` verwenden? Arbeitsannahme 2026-05-04: `allgemeine RV` als erste Baseline, `RV insgesamt` als späterer Vergleich.
- Welche Rentenausgaben sind die Vergleichsgröße: Rentenausgaben ohne KVdR/PVdR-Zuschüsse, Renten plus KVdR/PVdR oder Gesamtausgaben? Arbeitsannahme 2026-05-04: Rentenausgaben.
- Wie werden Gebietsbrüche behandelt? Arbeitsstand 2026-05-04: Die aktuelle allg.-RV-Cashflow-Pipeline nutzt `Alte Bundesländer` bis 1990 und `Insgesamt` ab 1991; andere Tabellen können abweichen.
- Welche Übergangsfinanzierung ist die konservative Baseline? Arbeitsannahme 2026-05-04: Keine Übergangsschuld in der Baseline; der Fonds wird aus zusätzlicher Beitragslast und Rentenverzicht finanziert.
- Welche Investmentpolitik ist historisch plausibler als reine DAX/S&P-500-Rückblicke?
