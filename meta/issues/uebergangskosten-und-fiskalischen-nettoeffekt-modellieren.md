# Aufbaupreis und optionale Uebergangskosten modellieren

## Summary

Den Aufbaupreis der Baseline modellieren und optionale Finanzierungslücken für spätere Beitragsumleitungs-Szenarien vorbereiten.

## Requirements

- Baseline-Szenarien definieren, wie viel Fondsaufbau aus höheren Beiträgen und niedrigeren Rentenausgaben stammt.
- Fondsvermögen immer auch dem kumulierten Aufbaupreis gegenüberstellen.
- Für spätere echte Beitragsumleitungs-Szenarien festlegen, wie der fehlende Umlage-Cashflow finanziert würde.
- Bei optionaler Schuldenfinanzierung Zinsannahmen und Nettovermögen aus Fonds abzüglich Schulden berechnen.
- Deutlich machen, dass ein reiner Brutto-Fondsbestand ohne Aufbaupreis kein vollständiger Wohlfahrtsvergleich ist.

## Acceptance Criteria

- Für jedes Hauptszenario gibt es Fondsbestand, kumulierten Aufbaupreis und Kapitalertrag über Aufbaupreis.
- Die Website kann den Unterschied zwischen Brutto-Fondsvermögen, Aufbaupreis und Kapitalertrag erklären.
- Das Modell verhindert implizite "free money"-Annahmen.

## Notes

- Dieses Thema ist zentral, weil ein Fonds ohne expliziten Aufbaupreis als kostenloser Vermögensaufbau missverstanden werden kann.
- Arbeitsstand 2026-05-04: Die Baseline baut keine Übergangsschuld auf. Der Fonds wird aus 5 Prozent höheren Beiträgen und 5 Prozent niedrigeren Rentenausgaben finanziert.
- `TRANS-001` dokumentiert diesen Verzichtsdeal; spätere echte Beitragsumleitungen brauchen weiterhin eine gesonderte Übergangsfinanzierung.
