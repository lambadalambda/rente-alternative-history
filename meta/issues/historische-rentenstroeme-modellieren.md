# Historische Rentenstroeme modellieren

## Summary

Die historischen Finanzstroeme der gesetzlichen Rentenversicherung so modellieren, dass ein hypothetischer Fondsaufbau ab 1957 berechnet werden kann.

## Requirements

- Jahresdaten fuer Beitragseinnahmen, Rentenausgaben und Bundesmittel erfassen.
- Entscheiden, auf welchen Beitrags- und Ausgabenbasen der Fondsaufbau beruht.
- Umlageverfahren und Nachhaltigkeitsruecklage vom hypothetischen Fonds klar trennen.
- Nominale und reale Betrachtung getrennt ausweisen.
- Historische Gebiets- und Systembrueche, insbesondere Wiedervereinigung, transparent behandeln.
- Klären, welche Zweige der gesetzlichen Rentenversicherung enthalten oder ausgeschlossen sind.
- DDR-Rentenüberleitung, Wiedervereinigungseffekte und spätere Reformbrüche als eigene Modellentscheidungen behandeln.
- Ausgeschlossene Cashflows wie Sonderzahlungen, Ausgleichsbeträge oder versicherungsfremde Leistungen dokumentieren.

## Acceptance Criteria

- Ein dokumentiertes Cashflow-Schema beschreibt Einzahlungen, Auszahlungen, Fondsbestand und Renditeannahmen pro Jahr.
- Mindestens eine Baseline ab 1957 ist reproduzierbar berechenbar.
- Strittige methodische Entscheidungen sind fuer Leserinnen und Leser verstaendlich begruendet.
- Westdeutsche, gesamtdeutsche und heutige Bezugsgrößen werden nicht unkommentiert vermischt.
- Das Cashflow-Schema verweist auf Aufbaupreis und gegebenenfalls separate Übergangskosten.

## Notes

- Der Claim, dass ein 5/5-Verzichtsdeal heute Rentenzahlungen aus Renditen decken koennte, muss als pruefbare Hypothese behandelt werden, nicht als Vorabfakt.
- Arbeitsstand 2026-05-04: DRV-Finanzdaten im PDF `Rentenversicherung in Zeitreihen 2025` sind grob inventarisiert; `allgemeine RV` ist als erste Baseline gesetzt, `RV insgesamt` bleibt Vergleich.
- Eine erste Prototyp-Baseline wurde erstellt; sie nutzt noch manuell rekonstruierte DRV-Stützjahre und lineare Interpolation.
- Nutzerentscheidung 2026-05-04: Der Fondsaufbau basiert auf zusätzlichen Beiträgen und niedrigeren Rentenausgaben; Vergleichsgröße sind Rentenausgaben.
