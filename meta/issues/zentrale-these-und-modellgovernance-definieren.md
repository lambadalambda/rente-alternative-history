# Zentrale These und Modellgovernance definieren

## Summary

Die Kernfrage des Projekts als falsifizierbare Modellhypothese festlegen, bevor Daten, Design oder Interaktion die Aussage verzerren.

## Requirements

- Definieren, welche Hauptclaims die Website machen darf und welche ausdrücklich nicht.
- Festlegen, was "Rentenzahlungen aus Fondserträgen decken" bedeutet: Bruttoausgaben, Nettoausgaben, laufende Erträge, nachhaltige Entnahme oder Substanzverzehr.
- Harte Trennung zwischen historischem Fakt, Modellannahme, Szenarioergebnis und Interpretation verlangen.
- Falsifikationskriterien festlegen: Die Website muss auch veröffentlichen, wenn der 5/5-Verzichtsdeal unter plausiblen Annahmen nicht trägt.
- Ein versioniertes Annahmenregister für zentrale Entscheidungen wie Aufbaupfad, Cashflow-Basis, Kosten, Steuern und Wechselkurse anlegen.

## Acceptance Criteria

- Ein Methodenentwurf benennt die Primärfrage, Nebenfragen, Nicht-Claims und Abbruch-/Falsifikationsbedingungen.
- Jede spätere Headline-Zahl lässt sich einer definierten Claim-Kategorie zuordnen.
- Änderungen an Modellannahmen brauchen eine dokumentierte Begründung im Annahmenregister.

## Notes

- Ausgangsformulierung: "Wir prüfen, ob und unter welchen Annahmen eine seit 1957 aufgebaute Reserve spätere Rentenausgaben teilweise oder vollständig hätte finanzieren können."
- Arbeitsstand 2026-05-04: Methodenentwurf in `meta/methodik/modellgovernance.md`, Annahmenregister in `assumptions/register.yaml`, Änderungslog in `assumptions/changelog.md`.
- Issue bleibt offen, bis die offenen Baseline-Entscheidungen im Annahmenregister fachlich geprüft und entweder freigegeben oder explizit als Sensitivität markiert sind.
