# Uebergangskosten und fiskalischen Nettoeffekt modellieren

## Summary

Die Finanzierungslücke modellieren, die entsteht, wenn ein Teil der Rentenbeiträge nicht sofort ausgegeben, sondern investiert wird.

## Requirements

- Szenarien definieren, wie der fehlende Umlage-Cashflow finanziert wird: höhere Beiträge, geringere Leistungen, höhere Steuern/Bundeszuschüsse oder Schulden.
- Fondsvermögen immer auch dem kumulierten Finanzierungsbedarf gegenüberstellen.
- Bei Schuldenfinanzierung Zinsannahmen und Nettovermögen aus Fonds abzüglich Schulden berechnen.
- Politische und makroökonomische Grenzen einer jahrzehntelangen Übergangsfinanzierung beschreiben.
- Deutlich machen, dass ein reiner Brutto-Fondsbestand ohne Übergangskosten kein vollständiger Wohlfahrtsvergleich ist.

## Acceptance Criteria

- Für jedes Hauptszenario gibt es Fondsbestand, kumulierte Übergangsfinanzierung und fiskalische Nettoposition.
- Die Website kann den Unterschied zwischen Brutto-Fondsvermögen und Nettoeffekt erklären.
- Das Modell verhindert implizite "free money"-Annahmen.

## Notes

- Dieses Thema ist zentral, weil das reale Umlagesystem historische Renten weiterzahlen musste.
- Arbeitsstand 2026-05-04: `meta/methodik/modellgovernance.md` legt fest, dass jede Umleitung von Beiträgen entgangene Umlageeinnahmen, Ersatzfinanzierung, Zinskosten und fiskalische Nettoposition ausweisen muss.
- Konkrete Übergangsfinanzierung ist noch offen und steht als `TRANS-001` in `assumptions/register.yaml`.
- Nutzerentscheidung 2026-05-04: Bei historischen Beitragseinnahmen von 100 werden im Szenario 105 gezahlt, 95 gehen in die Umlage und 10 in den Fonds. Diese Annahme ist als relativer Beitragsanteil dokumentiert, nicht als Beitragssatz-Prozentpunkte.
