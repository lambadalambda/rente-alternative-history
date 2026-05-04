# Interaktives Szenario-Modell entwickeln

## Summary

Ein interaktives Modell bereitstellen, mit dem Nutzerinnen und Nutzer Anlagequoten, Indexwahl und zentrale Annahmen veraendern koennen.

## Requirements

- Regler fuer Anlagequote, Startjahr, Kostenquote und Renditevariante anbieten.
- Auswahl zwischen DAX, S&P 500 und einer globalen Index-Alternative ermoeglichen.
- Kerngroessen anzeigen: Fondsbestand, Jahresrendite, Rentenausgaben, Deckungsquote und Entnahmebedarf.
- Unsicherheit und Grenzen des Modells sichtbar machen.
- Interaktion muss clientseitig in einer statischen Website funktionieren.
- Regler und Auswahlfelder mit tastaturbedienbaren, zugänglichen Alternativen umsetzen.
- Parameter in teilbaren URLs oder Presets speichern, ohne die Caveats aus dem Kontext zu reißen.
- Eine No-JS-Baseline mit statischen Kerntabellen oder Grafiken anbieten.

## Acceptance Criteria

- Aenderungen an Parametern aktualisieren Grafiken ohne Server.
- Die Baseline-Szenarien sind per URL oder Preset reproduzierbar.
- Jede angezeigte Zahl ist auf eine Datenquelle oder Annahme zurueckfuehrbar.
- Angezeigte Werte vermeiden Scheingenauigkeit durch sinnvolle Rundung, Einheiten, Basisjahr und Annahmenlabel.
- Geteilte Szenarien zeigen sichtbar, welche Parameter und Einschränkungen gelten.

## Notes

- Die Website soll nicht als Anlageberatung wirken, sondern als historisches und fiskalisches Gedankenexperiment.
- Arbeitsstand 2026-05-04: Erste interaktive Modellwerkstatt mit Reglern für Fondsbeitrag, zusätzliche Beiträge, Rendite, Kosten und Übergangszins angelegt. Die Renditen sind ausdrücklich illustrative Konstanten, keine historischen Indexdaten.
- Issue bleibt offen, bis echte historische Renditeserien, Presets per URL und vollständige Quellenrückführung angebunden sind.
