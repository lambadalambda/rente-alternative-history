# Modellgovernance

Stand: 2026-05-04

Status: Arbeitsentwurf vor der ersten Modellrechnung. Dieses Dokument definiert, welche Aussagen das Projekt prüfen darf. Es enthält keine Ergebnisse.

## Primärfrage

Wir prüfen, ob und unter welchen Annahmen eine seit der Rentenreform 1957 aufgebaute, teilweise kapitalgedeckte Reserve spätere Rentenausgaben teilweise oder vollständig hätte finanzieren können.

Die 10-Prozent-Idee ist ein Szenarioparameter. Sie ist kein vorab bestätigtes Ergebnis.

## Nebenfragen

- Welche historischen Zahlungsströme der gesetzlichen Rentenversicherung eignen sich als Basis für eine hypothetische Anlagequote?
- Wie groß wäre der jährliche Finanzierungsbedarf im Umlageverfahren, wenn ein Teil der Beiträge nicht sofort zur Rentenzahlung verfügbar wäre?
- Wie unterscheiden sich Brutto-Fondsvermögen und fiskalische Nettoposition nach Übergangskosten?
- Wie sensibel sind Ergebnisse gegenüber Indexwahl, Startjahr, Kosten, Steuern, Wechselkursen, Inflation und Entnahmeregel?
- Welche Szenarien sind bloße Vergleichsrechnungen mit rückblickenden Indexdaten und welche kommen einer historisch plausibleren öffentlichen Investmentpolitik näher?

## Aussagekategorien

Jede spätere Headline-Zahl muss einer dieser Kategorien zugeordnet werden:

| Kategorie | Bedeutung | Zulässige Formulierung |
| --- | --- | --- |
| Historischer Fakt | Direkt aus einer Quelle belegte historische Angabe | "Die DRV weist für Jahr X Beitragseinnahmen von Y aus." |
| Rekonstruktion | Aus Quellen abgeleiteter Wert mit Transformationsschritt | "Nach Umrechnung in Euro und Preisbasis X ergibt sich Y." |
| Modellannahme | Nicht beobachtete Setzung für das kontrafaktische Szenario | "Das Szenario setzt eine Anlagequote von 10 Prozent der Beiträge an." |
| Modelloutput | Ergebnis einer definierten Rechnung | "Unter Annahmen A, B und C berechnet das Modell Y." |
| Interpretation | Einordnung des Outputs | "Das spricht dafür, dass der Befund stark von der Übergangsfinanzierung abhängt." |

## Nicht-Claims

Diese Aussagen sind ohne weitere Einschränkung verboten:

- "10 Prozent investiert hätten alle Renten bezahlt."
- "Deutschland hätte heute X Billionen Euro."
- "Das Umlagesystem war historisch eindeutig die falsche Entscheidung."
- "Ein S&P-500-, DAX- oder Weltindex-Szenario war seit 1957 politisch und institutionell automatisch realistisch."
- "Die Rentenprobleme wären gelöst gewesen."

Zulässig sind vorsichtige, belegbare Formulierungen:

- "Unter Annahme X ergibt das Modell Y."
- "Dieses Szenario berücksichtigt Übergangskosten noch nicht und ist deshalb nur eine Bruttorechnung."
- "Der Befund hängt sichtbar von Indexwahl, Kosten, Steuern und der Definition der investierten Beiträge ab."

## Definition von Deckung

"Rentenzahlungen aus Fondserträgen decken" ist mehrdeutig. Die Website darf erst dann von Deckung sprechen, wenn die verwendete Definition sichtbar benannt ist.

| Metrik | Definition | Einschränkung |
| --- | --- | --- |
| Brutto-Fondsvermögen | Fondsbestand am Jahresende ohne Abzug von Übergangskosten | Kein Wohlfahrts- oder Fiskalvergleich |
| Jahresrendite brutto | Wertänderung des Fonds in einem Jahr vor Kosten/Steuern | Kann in Krisenjahren negativ sein |
| Jahresrendite netto | Wertänderung nach Kosten, Steuern und Währungseffekten | Braucht explizite Annahmen |
| Nachhaltige Entnahme | Regelbasierte Entnahme, die den Fonds nicht sofort aufzehrt | Keine Garantie für einzelne Krisenpfade |
| Fiskalische Nettoposition | Fondsvermögen minus kumulierte Übergangsfinanzierung und Zinsen | Zentrale Metrik für öffentliche Finanzen |
| Deckungsquote | Zulässige Fondsfinanzierung geteilt durch gewählte Rentenausgaben | Nur interpretierbar mit klarer Ausgabenbasis |

Ein Szenario darf nicht als "vollständig gedeckt" gelten, wenn es nur Brutto-Fondsvermögen zeigt, aber die entgangenen Umlageeinnahmen und deren Finanzierung ausblendet.

## Mindestmodell vor öffentlicher Aussage

Vor jeder öffentlichen Ergebniszahl braucht das Modell mindestens diese Bausteine:

- Historische Jahresreihe für Beitragseinnahmen oder eine andere begründete Cashflow-Basis.
- Historische Jahresreihe für Rentenausgaben mit klarer Brutto-/Netto-Abgrenzung.
- Anlagequote und Investmentpolitik mit dokumentiertem Status als Annahme oder Vergleichsrechnung.
- Übergangsfinanzierung für den Teil der Beiträge, der dem Umlagesystem entzogen wird.
- Kosten-, Steuer-, Inflations- und Währungsannahmen oder eine sichtbare Markierung, dass sie noch fehlen.
- Sensitivitäten für mindestens konservatives, mittleres, optimistisches und adverses Szenario.

## Übergangskostenregel

Jede Umleitung von Beiträgen in einen Fonds erzeugt im Umlagesystem einen Finanzierungsbedarf. Das Modell muss deshalb je Jahr zeigen:

- entgangene Umlageeinnahmen,
- Ersatzfinanzierung durch Beiträge, Steuern, Bundeszuschuss, Leistungskürzung oder Schulden,
- Zinskosten bei Schuldenfinanzierung,
- Brutto-Fondsvermögen,
- fiskalische Nettoposition.

Eine Rechnung ohne Übergangskosten ist erlaubt, muss aber sichtbar als unvollständige Brutto-Sparrechnung gekennzeichnet werden.

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

- Die 10-Prozent-Hypothese trägt nur ohne Übergangskosten.
- Die 10-Prozent-Hypothese trägt nur bei optimistischer Indexwahl, aber nicht bei plausibleren Kosten-, Steuer- oder Portfoliovarianten.
- Die fiskalische Nettoposition bleibt negativ, obwohl das Brutto-Fondsvermögen groß wirkt.
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

- Handgerechnete Beispieljahre für Beitragumleitung und Fondsakkumulation.
- Regressionstests für Headline-Zahlen.
- Tests für nominale und reale Umrechnung.
- Tests für DEM/EUR/USD-Umrechnung.
- Tests für Kosten- und Steuerabzug.
- Tests für Übergangsfinanzierung und fiskalische Nettoposition.
- Datenprovenienzprüfung gegen `data/manifest.yaml`.

## Offene Entscheidungen vor der ersten Rechnung

- Gilt die Anlagequote auf Beitragseinnahmen, Gesamteinnahmen oder nur bestimmte Beitragsarten? Arbeitsannahme 2026-05-04: Beitragseinnahmen.
- Soll die Baseline `RV insgesamt` oder `allgemeine RV` verwenden? Arbeitsannahme 2026-05-04: `allgemeine RV` als erste Baseline, `RV insgesamt` als späterer Vergleich.
- Welche Rentenausgaben sind die Vergleichsgröße: Rentenausgaben ohne KVdR/PVdR-Zuschüsse, Renten plus KVdR/PVdR oder Gesamtausgaben? Arbeitsannahme 2026-05-04: Rentenausgaben.
- Wie wird der Bruch `Alte Bundesländer bis 1991` und `Insgesamt ab 1992` behandelt?
- Welche Übergangsfinanzierung ist die konservative Baseline? Arbeitsannahme 2026-05-04: Bei historischen Beitragseinnahmen von 100 werden 105 Beiträge gezahlt, 95 gehen in die Umlage und 10 in den Fonds.
- Welche Investmentpolitik ist historisch plausibler als reine DAX/S&P-500-Rückblicke?
