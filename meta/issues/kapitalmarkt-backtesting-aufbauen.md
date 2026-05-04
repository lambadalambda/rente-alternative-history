# Kapitalmarkt-Backtesting aufbauen

## Summary

Ein belastbares Backtesting fuer hypothetische Fondsanlagen mit verschiedenen Indizes und Kostenannahmen aufbauen.

## Requirements

- DAX, S&P 500 und mindestens eine global diversifizierte Alternative vergleichbar machen.
- Performance-Index vs. Kursindex sauber unterscheiden, besonders beim DAX.
- Fuer S&P 500 Wechselkurse EUR/DEM/USD und Dividenden-/Total-Return-Fragen dokumentieren.
- Laufende Kosten, Rebalancing und moegliche Transaktions-/Verwaltungskosten als Parameter fuehren.
- Renditen mit jaehrlichen Cashflows aus dem Rentenmodell verbinden.
- Survivorship Bias, Indexmethodik und historische Rekonstruktion offenlegen.
- Steuerannahmen wie Quellensteuer, Kapitalertragsteuer oder hypothetische Steuerfreiheit eines Staatsfonds dokumentieren.
- Wechselkursregime DEM/EUR/USD und Umrechnungstage beziehungsweise Jahresdurchschnitte festlegen.

## Acceptance Criteria

- Fuer jeden Index ist klar, ob Total Return, Price Return, nominal oder real gerechnet wird.
- Backtest-Ergebnisse sind mit mindestens zwei unabhaengigen Plausibilitaetsquellen abgleichbar.
- Das Modell kann mehrere Aufbaupfade wie +1/-1, +5/-5 und einseitige Beitrags- oder Rentenszenarien berechnen.
- Die Darstellung warnt sichtbar, wenn ein Szenario eine rückblickende Vergleichsrechnung statt einer historisch plausiblen Anlagepolitik ist.
- Jahre mit negativen Renditen und Drawdown-Stress werden nicht geglättet oder ausgeblendet.

## Notes

- Historische Indexdaten vor ETF-Verfuegbarkeit duerfen genutzt werden, muessen aber als hypothetische Indexabbildung gekennzeichnet werden.
