# Plausibilitaetschecks und Sensitivitaetsanalyse durchfuehren

## Summary

Das Modell gegen Rechenfehler, Scheingenauigkeit und einseitige Annahmen absichern.

## Requirements

- Ergebnisse mit offiziellen Aggregaten und unabhaengigen Kapitalmarktquellen abgleichen.
- Sensitivitaeten fuer Anlagequote, Startjahr, Kosten, reale Rendite, Wechselkurs und Krisenjahre berechnen.
- Risiko- und Pfadabhaengigkeit sichtbar machen, nicht nur Endwerte.
- Mindestens ein konservatives, ein mittleres und ein optimistisches Szenario definieren.
- Kritische Gegenargumente wie politische Umsetzbarkeit, Uebergangskosten und Marktrisiko behandeln.
- Negative oder ernüchternde Szenarien bewusst einbeziehen, wenn sie plausibel sind.
- Sequenzrisiko, Liquiditätsstress und Entnahmejahre mit negativen Renditen prüfen.
- Modelltests für handgerechnete Beispieljahre und bekannte Aggregatwerte anlegen.

## Acceptance Criteria

- Baseline-Ergebnisse bestehen Plausibilitaetschecks gegen Referenzsummen.
- Die Website zeigt, wie stark zentrale Aussagen von Annahmen abhaengen.
- Bekannte Modellgrenzen sind im Text und/oder Methodenbereich sichtbar.
- Headline-Ergebnisse bestehen Regressionstests, damit spätere Daten- oder Codeänderungen auffallen.
- Falls die zentrale Hypothese nur unter aggressiven Annahmen trägt, wird das sichtbar als Ergebnis ausgewiesen.

## Notes

- Besonders wichtig ist die Frage, ob Fondsrenditen ohne Substanzverzehr wirklich laufende Rentenausgaben decken koennten.
- Arbeitsstand 2026-05-04: Der UI-Prototyp zeigt bereits Brutto-Fondsbestand, Übergangsschuld, fiskalische Nettoposition und Rendite/Rentenausgaben. Die Werte sind noch nicht als Plausibilitätsbefund nutzbar, weil Renditen konstant und DRV-Daten nur prototypisch transkribiert sind.
