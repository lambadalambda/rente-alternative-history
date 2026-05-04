# Statische Website-Architektur aufsetzen

## Summary

Eine statisch hostbare Website-Struktur aufbauen, die Daten, Modell und Visualisierung sauber trennt.

## Requirements

- Geeigneten Static-Site-Stack waehlen, der auf GitHub Pages hostbar ist.
- Daten als versionierte, nachvollziehbare Artefakte im Repository ablegen.
- Modellcode clientseitig oder build-time ausfuehrbar halten.
- Gute Ladezeiten fuer Desktop und Mobile sichern.
- Entwicklungs-, Build- und Deploy-Befehle dokumentieren.
- Lokale statische Assets bevorzugen und Drittanbieterabhängigkeiten minimieren.
- Build-, Test- und Accessibility-Checks für CI vorbereiten.
- Statische Fallbacks für zentrale Szenarien build-time generieren.

## Acceptance Criteria

- Ein lokaler Entwicklungsserver und ein statischer Produktionsbuild funktionieren.
- Daten, Berechnungslogik und Praesentationskomponenten sind getrennt auffindbar.
- GitHub-Pages-Hosting ist ohne Server-Backend moeglich.
- Der Produktionsbuild funktioniert ohne Tracking, Cookies oder externe Laufzeitdienste.
- Die README dokumentiert die Befehle für Entwicklung, Build, Test und Daten-Rebuild.

## Notes

- JavaScript ist erlaubt; Serverabhängigkeit nach dem Build nicht.
