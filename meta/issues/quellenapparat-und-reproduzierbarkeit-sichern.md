# Quellenapparat und Reproduzierbarkeit sichern

## Summary

Sicherstellen, dass alle Daten, Annahmen und Berechnungen der Website nachvollziehbar und zitierbar bleiben.

## Requirements

- Quellen direkt im Datensatz und in der Website referenzieren.
- Rohdaten, transformierte Daten und manuelle Annahmen getrennt dokumentieren.
- Berechnungsschritte reproduzierbar machen.
- Unsichere Datenpunkte und Schaetzungen explizit markieren.
- Lizenz- und Nutzungsfragen fuer Daten und Grafiken dokumentieren.
- Rohdaten, Zwischenstände und finale Website-Daten mit Prüfsummen oder Versionshinweisen versehen.
- Einen Ein-Befehl-Rebuild aus verfügbaren Quellen und dokumentierten Annahmen anstreben.
- Generierte Datenartefakte klar markieren und nicht manuell nachbearbeiten.

## Acceptance Criteria

- Jede Grafik hat einen sichtbaren Quellenhinweis.
- Ein Datenmanifest beschreibt Herkunft, Abrufdatum, Verarbeitung und Lizenzstatus.
- Reproduktionsschritte sind in der README dokumentiert.
- Ein Annahmen- und Datenmanifest enthält Checksummen, Abrufdaten, Transformationsschritte und bekannte Einschränkungen.
- Wenn der Rebuild wegen nicht frei verfügbarer Quellen nicht vollständig automatisierbar ist, sind die manuellen Schritte exakt beschrieben.

## Notes

- Wenn Daten nicht frei weiterverbreitet werden duerfen, nur abgeleitete oder manuell nachbaubare Tabellen aufnehmen und die Beschraenkung nennen.
- Arbeitsstand 2026-05-04: Prototypdatensatz `data/website/prototype-allgemeine-rv.json` ist im Manifest dokumentiert und als rekonstruierte, nicht finale Zahl markiert. Eine reproduzierbare Extraktionspipeline fehlt noch.
