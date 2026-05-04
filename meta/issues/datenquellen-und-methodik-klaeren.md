# Datenquellen und Methodik klaeren

## Summary

Klaeren, welche offiziellen und nachvollziehbaren Daten fuer die Alternativgeschichte der deutschen gesetzlichen Rentenversicherung genutzt werden.

## Requirements

- Startpunkt der Analyse auf die Rentenreform 1957 unter Konrad Adenauer legen.
- Primaerquellen fuer Rentenausgaben, Beitragseinnahmen, Beitragssaetze, Bundeszuschuesse, Rentnerzahlen und relevante Reformbrueche identifizieren.
- Kapitalmarktdaten fuer DAX, S&P 500 und mindestens eine breitere Weltindex-Alternative identifizieren.
- Inflations-, Wechselkurs- und Steuerannahmen explizit dokumentieren.
- Quellen bevorzugen, die langfristig stabil, zitierbar und lizenzrechtlich nutzbar sind.
- Für Datenpunkte ein Vertrauensniveau kennzeichnen: amtliche Zahl, rekonstruierte Zahl, Schätzung oder Modellannahme.
- Eine Konfliktregel festlegen, falls mehrere seriöse Quellen unterschiedliche Werte nennen.
- Abrufdatum, Archivlink oder lokale Snapshot-Strategie für webbasierte Quellen dokumentieren.

## Acceptance Criteria

- Eine Quellenliste mit URL, Herausgeber, Datenbereich, Aktualitaet, Lizenz-/Nutzungshinweis und Vertrauensniveau liegt vor.
- Jede benoetigte Modellvariable ist einer Quelle oder einer dokumentierten Annahme zugeordnet.
- Datenluecken und Brueche in Zeitreihen sind sichtbar markiert.
- Konflikte zwischen Quellen sind dokumentiert und begründet entschieden.
- Nicht weiterverbreitbare Daten sind mit exakten Reproduktionsschritten statt kopierten Rohdaten beschrieben.

## Notes

- Wichtige Kandidaten: Deutsche Rentenversicherung, Bundesministerium fuer Arbeit und Soziales, Statistisches Bundesamt, Bundesbank, OECD, FRED, Stooq, Yahoo Finance, MSCI/S&P/DAX-Indexanbieter.
- Arbeitsstand 2026-05-04: Erstes Datenmanifest in `data/manifest.yaml`, Recherche in `meta/research/initiale-datenquellen-recherche.md`, DRV-Inventar in `meta/research/drv-zeitreihen-inventar.md`.
- Issue bleibt offen, weil die Quellenliste noch nicht vollständig extrahiert, lizenzgeprüft und mit finalen Tabellen-/Serien-IDs versehen ist.
