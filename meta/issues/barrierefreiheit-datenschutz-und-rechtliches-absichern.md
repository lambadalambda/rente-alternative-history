# Barrierefreiheit, Datenschutz und Rechtliches absichern

## Summary

Die Website so planen, dass sie für ein deutsches Publikum rechtlich sauber, datensparsam und barrierearm nutzbar ist.

## Requirements

- Impressum, Datenschutzerklärung und sichtbaren Haftungsausschluss "keine Anlageberatung" einplanen.
- Standardmäßig ohne Tracking, Cookies, externe Fonts, CDNs oder eingebettete Drittinhalte arbeiten; Abweichungen begründen.
- WCAG 2.1 AA beziehungsweise BITV-nahe Anforderungen für Kontrast, Tastaturbedienung, Fokus, Screenreader und semantische Struktur anstreben.
- Für interaktive Regler ARIA-Beschriftungen, Tastaturbedienung und verständliche Ergebnisankündigungen vorsehen.
- Für komplexe Charts Textzusammenfassungen, Datentabellen und reduzierte Bewegungsalternativen bereitstellen.

## Acceptance Criteria

- Jede interaktive Kerngrafik ist per Tastatur bedienbar und hat eine zugängliche Text-/Tabellenalternative.
- `prefers-reduced-motion` wird respektiert und keine Information hängt nur an Animation oder Farbe.
- Rechtliche Pflichtseiten und Disclaimer sind als eigene Seiten oder klar erreichbare Abschnitte eingeplant.

## Notes

- GitHub Pages reduziert Serverrisiken, ersetzt aber nicht Impressum, Datenschutzprüfung und Lizenzprüfung.
