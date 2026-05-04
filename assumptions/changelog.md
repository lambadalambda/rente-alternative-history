# Annahmen-Changelog

Dieses Log dokumentiert Änderungen an zentralen Modellannahmen aus `assumptions/register.yaml`.

## 2026-05-04

- Initiales Annahmenregister angelegt.
- Die 10-Prozent-Idee wurde als `sensitivity_only` und nicht als bestätigte Baseline markiert.
- Zentrale Entscheidungen zu Cashflow-Basis, Gebietsstand, Rentenausgabenbasis, Übergangsfinanzierung, Indexwahl, Kosten, Steuern und Währung bleiben offen.
- Nutzerentscheidung ergänzt: `FLOW-001` nutzt Beitragseinnahmen als Basis der Anlagequote.
- Nutzerentscheidung ergänzt: `FLOW-002` nutzt Rentenausgaben als Vergleichsgröße.
- Nutzerentscheidung ergänzt: `TRANS-001` modelliert 10 Prozent Fondsbeitrag als 5 Prozent zusätzliche Beiträge plus 5 Prozent Umleitung aus der Umlage. Die Werte sind als relative Anteile an historischen Beitragseinnahmen zu verstehen, nicht als Beitragssatz-Prozentpunkte.
- Nutzerentscheidung ergänzt: `PENSION-001` nutzt `allgemeine RV` als erste institutionelle Baseline; `RV insgesamt` bleibt als späterer Vergleich vorgesehen.

## 2026-05-04, spätere Aktualisierung

- Nutzerentscheidung korrigiert: Die Baseline soll keine Übergangsschuld aufbauen. Stattdessen finanziert ein neutraler Verzichtsdeal den Fonds direkt.
- `TRANS-001` wurde geändert: 5 Prozent höhere Beiträge plus 5 Prozent niedrigere Rentenausgaben ergeben die Fonds-Einzahlung; `payg_gap` ist in der Baseline `0`.
- `INV-001` wurde von einer abstrakten 10-Prozent-Anlagequote auf den konkreten Standarddeal `+5 Prozent Beiträge / -5 Prozent Rentenausgaben` umgestellt.
- `FISC-001` berichtet nun Fondsvermögen neben kumuliertem Aufbaupreis statt neben Übergangsschuld.
