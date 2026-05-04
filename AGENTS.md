# AGENTS.md

Dieses Repository dient einer deutschsprachigen, datenjournalistischen, statisch hostbaren Website über ein kontrafaktisches Rentenmodell ab 1957. Arbeite so, dass spätere Leserinnen und Leser Zahlen, Annahmen und Grenzen nachvollziehen können.

## Sprache und Ton

- Sichtbare Website-Texte sind Deutsch.
- Schreibe sachlich, präzise und journalistisch zugänglich.
- Vermeide Formulierungen, die Modelloutputs wie sichere historische Fakten klingen lassen.
- Bevorzuge Formulierungen wie "unter Annahme X ergibt sich Y" statt "Deutschland hätte Y gehabt".
- Die Website ist keine Anlageberatung und keine parteipolitische Kampagne.

## Modellregeln

- Behandle die 10-Prozent-Idee als Hypothese, nicht als bewiesenes Ergebnis.
- Trenne historische Daten, Annahmen, Modelloutputs und Interpretation konsequent.
- Dokumentiere jede Änderung an zentralen Annahmen mit Begründung.
- Zeige Übergangskosten und fiskalische Nettoposition, wenn Beiträge hypothetisch investiert werden.
- Veröffentliche auch negative oder ernüchternde Szenarien, wenn sie aus plausiblen Annahmen folgen.

## Datenregeln

- Keine neue Datenquelle ohne Herausgeber, URL, Abrufdatum, Datenbereich, Lizenz-/Nutzungshinweis und Vertrauensniveau.
- Markiere Datenpunkte als amtliche Zahl, rekonstruierte Zahl, Schätzung oder Modellannahme.
- Halte Rohdaten, transformierte Daten, Annahmen und generierte Website-Daten getrennt.
- Bearbeite generierte Datenartefakte nicht manuell.
- Wenn Daten nicht weiterverbreitet werden dürfen, dokumentiere die Reproduktionsschritte statt die Daten ungeprüft zu kopieren.

## Quellen und Claims

- Keine Headline-Zahl ohne direkte Rückführung auf Quelle und Annahme.
- Jede zentrale Grafik braucht sichtbare Quellen- und Methodennähe.
- Unterscheide DAX/S&P-500/Weltindex-Vergleiche von historisch plausibler Investmentpolitik.
- Benenne Total Return, Price Return, nominale/reale Betrachtung, Basisjahr, Währung, Kosten und Steuern.
- Vermeide Cherry-Picking von Startjahren, Indizes oder optimistischen Endwerten.

## Frontendregeln

- Ziel ist eine statische Website, die auf GitHub Pages gehostet werden kann.
- Clientseitiges JavaScript ist erlaubt, ein Server-Backend nach dem Build nicht.
- Bevorzuge lokale Assets und vermeide Tracking, Cookies, externe Fonts, CDNs und eingebettete Drittinhalte.
- Interaktive Kontrollen müssen per Tastatur bedienbar sein.
- Komplexe Charts brauchen Textzusammenfassungen und Tabellenalternativen.
- Respektiere `prefers-reduced-motion`; keine Information darf nur über Farbe oder Animation vermittelt werden.

## Tests und Verifikation

- Modelllogik braucht Tests für bekannte Jahre, handgerechnete Beispiele und Regressionen bei Headline-Zahlen.
- Datenpipelines sollen reproduzierbar laufen und Prüfsummen oder Versionshinweise nutzen.
- Vor Veröffentlichungen Build, Daten-Rebuild, Modelltests und Accessibility-Checks ausführen, sobald diese eingerichtet sind.
- Wenn ein Check nicht ausgeführt werden kann, dokumentiere den Grund.

## Issue-Workflow

- Der repo-lokale Issue-Tracker liegt unter `meta/issues.md` und `meta/issues/`.
- Neue Arbeitspakete als Detaildatei in `meta/issues/` anlegen und in `meta/issues.md` verlinken.
- Abgeschlossene Issues erst nach erfüllten Acceptance Criteria nach `meta/issues_archive.md` verschieben.
- Bewahre Diskussionen, Anforderungen und Akzeptanzkriterien in den Detaildateien auf, nicht im Index.
