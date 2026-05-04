# Kapitalmarkt-Backtesting aufbauen

## Summary

Ein belastbares Backtesting fuer hypothetische Fondsanlagen mit verschiedenen Indizes und Kostenannahmen aufbauen.

## Requirements

- DAX, S&P 500 und mindestens eine global diversifizierte Alternative vergleichbar machen.
- Performance-Index vs. Kursindex sauber unterscheiden, besonders beim DAX.
- Fuer S&P 500 die DM-/Euro-/USD-Wechselkursbehandlung und Dividenden-/Total-Return-Fragen dokumentieren.
- Laufende Kosten, Rebalancing und moegliche Transaktions-/Verwaltungskosten als Parameter fuehren.
- Renditen mit jaehrlichen Cashflows aus dem Rentenmodell verbinden.
- Survivorship Bias, Indexmethodik und historische Rekonstruktion offenlegen.
- Steuerannahmen wie Quellensteuer, Kapitalertragsteuer oder hypothetische Steuerfreiheit eines Staatsfonds dokumentieren.
- Wechselkursregime, Quelleneinheiten und Umrechnungstage beziehungsweise Jahresdurchschnitte festlegen.

## Acceptance Criteria

- Fuer jeden Index ist klar, ob Total Return, Price Return, nominal oder real gerechnet wird.
- Backtest-Ergebnisse sind mit mindestens zwei unabhaengigen Plausibilitaetsquellen abgleichbar.
- Das Modell kann mehrere Aufbaupfade wie +1/-1, +5/-5 und einseitige Beitrags- oder Rentenszenarien berechnen.
- Die Darstellung warnt sichtbar, wenn ein Szenario eine rückblickende Vergleichsrechnung statt einer historisch plausiblen Anlagepolitik ist.
- Jahre mit negativen Renditen und Drawdown-Stress werden nicht geglättet oder ausgeblendet.

## Notes

- Historische Indexdaten vor ETF-Verfuegbarkeit duerfen genutzt werden, muessen aber als hypothetische Indexabbildung gekennzeichnet werden.

## Progress

- 2026-05-04: Erste reproduzierbare Kapitalmarkt-Pipeline hinzugefügt: `scripts/build_shiller_returns.py` erzeugt lokal einen Robert-Shiller-Forschungsproxy für jährliche US-Aktienmarktrenditen 1871-2014. Wegen ungeklärter Weiterverbreitungsrechte wird nur der Qualitätsnachweis `data/quality/returns/shiller-return-pipeline-check.json` versioniert. Noch nicht in das interaktive Modell integriert; keine offizielle S&P-500-Total-Return-Reihe; Lizenzklärung, Wechselkurse und Plausibilitätsquelle fehlen noch.
- 2026-05-04: Erste Bundesbank-FX-Pipeline hinzugefügt: `scripts/build_bundesbank_fx.py` extrahiert USD-Jahresdurchschnittskurse für DM 1948-1998 und Euro 1999-2025 aus der Bundesbank-Long-Time-Series-PDF. Versioniert ist `data/quality/fx/bundesbank-usd-annual-fx-check.json`; die vollständige Reihe bleibt lokal unter `data/processed/fx/`. Noch offen: Periodisierung mit Shiller-Jahresrenditen und Nutzungshinweise.
- 2026-05-04: Lokale Hilfsrechnung `scripts/build_us_equity_eur_returns.py` ergänzt. Sie kombiniert Shiller-USD-Nominalrenditen mit den Bundesbank-FX-Hilfswerten zu einer EUR-äquivalenten nominalen Proxy-Reihe 1948-2014. Versioniert ist nur `data/quality/returns/shiller-us-equity-eur-equivalent-check.json`; die Hilfsrechnung ist ausdrücklich nicht modellfreigegeben.
