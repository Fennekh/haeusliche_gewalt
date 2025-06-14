#### Dashboard zu Häusliche Gewalt in der Schweiz 2009–2024

Ein interaktives Dashboard zur Visualisierung und Analyse der Entwicklung von Häusliche Gewalt von 2009 bis 2024 nach Delikten sowie der Gesamtentwicklung der Betroffenen (Täter:innen und Opfer) und deren Eigenschaften (Geschlecht, Alter, Beziehung zwischen Täter:innen und Opfer). Erstellt mit Python und Dash.
.
#### Ziel des Dashboards

Das Dashboard soll es der Schweizer Bevölkerung, Behörden und Beratungsstellen dabei ermöglichen, die Entwicklung Häusliche Gewalt zu analysieren, zu erkennen, wer die Betroffenen (Täter:innen und Opfer) sind und in welcher Beziehung sie zueinander stehen.  
**Ziel:** Bewusstsein und Sichtbarkeit für Häusliche Gewalt erhöhen.

.
#### Datenquelle

Wir nutzen dafür die Daten des Bundesamts für Statistik. Die Polizeistatistik 2009–2024 (Datenstand: 14.02.2025):

- **Strafgesetzbuch (StGB)**: Straftaten Häusliche Gewalt und beschuldigte Personen  
  https://www.bfs.admin.ch/bfs/de/home/statistiken/kriminalitaet-strafrecht/polizei/haeusliche-gewalt.assetdetail.34387386.html

- **Strafgesetzbuch (StGB)**: Straftaten Häusliche Gewalt und geschädigte Personen  
  https://www.bfs.admin.ch/bfs/de/home/statistiken/kriminalitaet-strafrecht/polizei/haeusliche-gewalt.assetdetail.34387408.html

Folgende Attribute werden für die Jahre von 2009 bis 2024, für Täter:innen und Opfer und für 30 verschiedene Deliktarten sowie männlich/weiblich differenziert:

| Attribut                         | Beschreibung                                                                                                                                                                                                                                                                                                              |
|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Straftaten Total`               | Anzahl Straftaten pro Delikt                                                                                                                                                                                                                                                                                              |
| `Straftaten Mehrfach`            | Anteil der mehrfach verübten Straftaten. In Fällen, in denen die gleiche Person von derselben Täterschaft zu mehreren Zeitpunkten auf die gleiche Art wiederholt geschädigt wird, ohne dass eine separate Anzeige bzw. ein separater Rapport erfolgt, wird der betreffende Straftatbestand mit „mehrfach“ gekennzeichnet. |
| `Beschuldigte/Geschädigte Total` | Anzahl Personen pro Delikt (zur besseren Verständlichkeit umbenannt in Täter:innen und Opfer)                                                                                                                                                                                                                                                                     |
| `Alter`                          | 13 Alterskategorien, reduziert auf 8 Kategorien (10-Jahres-Schritte), in Anzahl Personen                                                                                                                                                                                                                                  |
| `Beziehungsart`                  | Beziehung zwischen den Personen (4 Kategorien: Partnerschaft, ehemalige Partnerschaft, Eltern-Kind-Beziehung, andere Verwandtschaft)                                                                                                                                                                                     |
.
#### Disclaimer

Die Dunkelziffer bei Häusliche Gewalt wird sehr hoch geschätzt.  
Bei Tätlichkeiten und Körperverletzungen werden z. B. 28,9 %, bei sexueller Gewalt 10,5 % der Fälle angezeigt.

Quelle: https://www.unisg.ch/de/newsdetail/news/hsg-strafrechtlerin-leuchtet-die-dunkelziffer-der-haeusli-chen-gewalt-aus/, Universität St. Gallen, 26.10.2023, zuletzt abgerufen: 09.06.2025
.
#### Metadaten im Dashboard

  - **Aktualisierungsdatum** der Daten im Fussbereich (z. B. „Letzte Aktualisierung: 22. April 2025")
  - **Datenquelle** im Fussbereich und Impressum („Bundesamt für Statistik – Polizeistatistik 2009–2024")
  - **Hinweise zu Dateninterpretation und Begrifflichkeiten** (z. B. Tooltip bei Hover über Info-Icon neben der Seitenüberschrift, oder Hinweise zu Delikt-Umbenennungen (Tab 1)) 
  - **Hinweise auf fehlende Werte Datenschutz** (z. B. Hinweis unter Tabelle)
  - **Haftungsausschluss** im Fussbereich
.
#### Datenschutz und Datenanonymisierung – Datenschutzmassnahmen des BFS

Das Bundesamt für Statistik wendet strenge Datenschutzrichtlinien an, um die Anonymität der Betroffenen zu gewährleisten:

- Statistische Geheimhaltung: Alle Daten werden vollständig anonymisiert veröffentlicht – keine Rückschlüsse auf Einzelpersonen möglich  
- Schwellenwertregelung: Bei Totalwerten zwischen 1–3 Personen werden Detailinformationen (Alter, Beziehungsart) aus Datenschutzgründen nicht ausgewiesen  
- Geografische Anonymisierung: Keine kleinräumigen geografischen Zuordnungen unter kantonaler Ebene  
- Zeitliche Aggregation: Daten werden nur in Jahreszyklen veröffentlicht, nie tagesaktuell  

Quelle: BFS Methodische Grundlagen, https://www.bfs.admin.ch/bfs/de/home/statistiken/kriminalitaet-strafrecht/polizei.html, Bundesamt für Statistik, zuletzt abgerufen: 14.06.2025
.
#### Visualisierungen und ihre Begründung

| Visualisierung                           | Warum gewählt?                                                                                                                                            |
|------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Tabelle**                               | Zeigt, welche Delikte zu Häusliche Gewalt gezählt werden, und ermöglicht Überblick über einzelne Delikte hinsichtlich Entwicklung, Geschlechterverhältnis, Beziehungsart und Alter |
| **Balkendiagramm**                        | Ermöglicht Analyse der Entwicklung der Straftaten und Erkennung des Anteils mehrfacher Straftaten                                                         |
| **Liniendiagramm (Betroffene)**           | Ermöglicht Analyse der Entwicklung der Betroffenenzahlen und Vergleich der Gesamtanzahl Täter:innen, Opfer                                               |
| **Balkendiagramme je Täter:innen/Opfer**  | Ermöglicht Analyse der Entwicklung der prozentualen Anteile Betroffener nach Geschlecht sowie den Vergleich Täter:innen und Opfer                        |
| **Liniendiagramm (Geschlecht)**           | Ermöglicht Analyse der Entwicklung der absoluten Anzahl von Betroffenen nach Geschlecht sowie den Vergleich Täter:innen und Opfer                        |
| **Gruppiertes Balkendiagramm**            | Ermöglicht eine geschlechterspezifische Analyse der Häufigkeit von Beziehungskonstellationen im gewählten Jahr sowie deren Unterschiede zwischen Täter:innen und Opfern |
| **Liniendiagramm (Alter)**                | Ermöglicht Analyse der Entwicklung der Anzahl Betroffener pro Alterskategorie nach Täter:innen und Opfer und gewähltem Geschlecht                        |
| **Alterspyramide**                        | Detailanalyse der Altersverteilung in einem bestimmten Jahr nach Geschlecht                                                                              |
.
#### Page Layout

Ein stratifiziertes Layout:

- *Oben:* Webseitentitel zur Darstellung des Oberthemas  
- *Ebene 2:* Navigation zur Seitenübersicht  
- *Ebene 3:* Abschnittstitel in Frageform und Untertitel für ergänzende Informationen  
- *Ebene 4:* Filter und Anzeigeeinstellungen  
- *Ebene 5:* Interaktive Diagramme, Tabelle, erläuternder Text  
- *Unten:* Hinweise, Quellen, Haftungsausschluss  
.
#### Seitenorganisation (Structure)

- *Seite 1:* Übersicht (Delikte im tabellarischen Überblick)  
- *Seite 2:* Zeitliche Entwicklung (Jahresverlauf)  
- *Seite 3:* Geschlechterverhältnis  
- *Seite 4:* Beziehungsart (Täter-Opfer-Beziehung)  
- *Seite 5:* Entwicklung Altersverteilung  
- *Seite 6:* Impressum (zusätzliche Informationen zum Projekt, Metadaten, rechtliches)  
.
#### Interaktionen

- **Sortier-Button:** Auf-/absteigende Sortierung der Tabellenwerte nach Anzahl Straftaten  
- **Toggle: Straftaten vs. Betroffene:** Wechsel von Ansicht Anzahl Straftaten zu Anzahl Betroffener  
- **Toggle: Prozentual vs. Absolut:** Wechsel zwischen absoluten und prozentualen Werten  
- **Dropdown-Filter:** Für Geschlecht und Jahr  
- **Radio-Button:** Täter:innen-/Opfer-Ansicht  
- **Linkage (Fokus):** Detailansicht der Altersverteilung für ein gewähltes Jahr  
- **Hover-Tooltips:** Für Anzeige genauer Werte und ergänzende Erklärungen  
- **Zoom & Pan:** In Diagrammen  
- **Tabs zur Navigation:** Zwischen Seiten  
.
#### Farbauswahl

- *Datenkodierung:* Geschlecht: Frauen (Rot), Männer (Blau), Gesamt (Schwarz)  
- *Semantische Farben:* Helligkeitsabstufungen für einfache/mehrfache Straftaten  
- *Barrierefreiheit:* Hoher Kontrast, farbenblindenfreundliche Darstellung (keine Rot-Grün-Kodierung)
.
#### Strukturmuster

- **Overview first, zoom and filter, then details-on-demand**  
  Nutzer:innen erhalten zuerst einen Überblick (z. B. Gesamtzahl der Straftaten), können anschließend durch Filter und Tabs fokussieren und bei Bedarf Details (z. B. Altersstruktur in einem Jahr oder per Hover) einsehen.

- **Einheitliche Seitenhierarchie**  
  Jede Seite folgt einer konsistenten Struktur:  
  Titel in Frageform → erläuternder Untertitel → Filter- und Auswahloptionen → interaktive Visualisierungen → ergänzende Hinweise

- **Barrierearme Farbgestaltung**  
  Die verwendete Farbpalette (Rot = Frauen, Blau = Männer, Schwarz = Gesamt) gewährleistet hohe Kontraste. Farben sind klar voneinander unterscheidbar und farbenblindenfreundlich.

- **Konsistente Achsenbeschriftung**  
  Über alle Diagramme hinweg gilt:  
  Y-Achse = Personenanzahl, X-Achse = Zeitverlauf oder thematische Kategorie (Ausnahme: Alterspyramide)  
  Dadurch wird die Vergleichbarkeit zwischen den Visualisierungen verbessert.

- **Konsistenz bei Diagrammen**  
  Achsentitel und Farben sind konsistent. Skalierungen bleiben pro Seite auch bei Filterungen unverändert. So bleibt die visuelle Vergleichbarkeit erhalten.
.
#### Limitationen

**Datenbedingte Einschränkungen**

- Hohe Dunkelziffer – nur angezeigte Fälle enthalten  
- Datenschutz – Werte 1–3 nicht sichtbar  
- Beziehungsart – nicht nach Geschlecht differenziert  

**Was nicht geklappt hat**

- Responsiveness für kleinere Geräte nur eingeschränkt (besonders Tabelle)  
- Tabellen haben keine Hover-Details und keine Filterung der Werte nach Jahr  
- Deliktspezifische Filterung auf Tab 2 bis 5 nicht umgesetzt  
- Keine automatischen Updates bei neuen BFS-Daten  
- Vermeiden von nicht überlappender Beschriftung bei Filterung von Liniendiagramm Alterskategorien

**Technische Limitationen**

- Lange Ladezeit beim Laden/Sortieren der Tabelle  
- Möglichkeit von PNG-Darstellung nicht zuverlässig in Dash DataTable darstellbar, daher Verwendung von HTML-Tabelle  

**Verbesserungsideen**

- Integration der BFS-API für automatische Datenupdates  
- Ergänzung von Interaktion mit Tabelle (z. B. Filterung nach Jahr, Hoverinfos über Miniaturen)  
- Deliktspezifische Filterung für Tab 2 bis 5  
- Export-Funktion für Tabelle  
- Vergleichstool für Kantone (sofern Daten verfügbar)  
- Vergleichstool gleiche Straftaten Häusliche Gewalt vs. nicht Häusliche Gewalt  
- Responsive Design  
- Code objektorientiert umsetzen und schöner lesbar schreiben  
- Bessere Lösung für Beschriftung bei Liniendiagramm Alterskategorien  
.
#### Feedback-Umsetzung von Tag 7

**Metadata**

- Quelle & Beschreibung ergänzt  
- Datenschutzhinweise ergänzt  

**Visual Representation**

- *Tab Beziehungen*  
  - Titel & Hoverinfo mit erklärendem Text ergänzt (Diskrepanzen erklärt)  
  - Wechsel von gestapeltem zu gruppiertem Balkendiagramm  
  - Vertikale Ausrichtung des Balkendiagramms beibehalten aufgrund besserer Vergleichbarkeit zwischen Täter:innen- und Opfer-Grafik  
  - Umstellung auf absolute Zahlen, da prozentuale Darstellung irreführend war  
  - Anordnung Balkenfarben (Frauen = links/Rot, Männer = rechts/Blau)

- *Alterspyramide:* Umgedreht (üblichere Darstellung)

**Page Layout**

- Tabelle auf Seite 1 verschoben  
- Layout „Zeitliche Entwicklung“ an Layout „Entwicklung Altersverteilung“ angeglichen  
- Eine ursprünglich geplante Gegenüberstellung auf dem Alters-Tab zweier Alterspyramiden (Täter:innen links, Opfer rechts) für mehr Konsistenz im Layout wurde zugunsten der Linkage-Funktion und dem Fokus auf die zeitliche Entwicklung verworfen  
- Ergänzung Linkage-Funktion für Alters-Detailansicht  

**Vereinheitlichung Layout/Grafiken**

- Achsen konsistent (Y = Personenanzahl, X = Zeit/Kategorien)  
- Vertikale Balken für das Geschlechterverhältnis beibehalten, da der zeitliche Verlauf mit horizontalen Balken schwer lesbar war und der Switch zwischen absoluten und prozentualen Werten nicht funktionierte  
- Farbzuordnung konsequent: Rot = Frauen, Blau = Männer

**Farben**

- Farbpalette reduziert auf Rot, Blau, Schwarz, Grau  
- Verzicht auf Farbabstufung im Alter-Liniendiagramm, da diese bei 8 Alterskategorien nicht unterscheidbar waren (Lösung: Linienbeschriftung direkt bei der jeweiligen Linie und Herauslesen der Kategorie durch Hovern ermöglicht)

**Text**

- Reduktion auf Seite 2 für bessere Übersicht  
- Vollständiges Readme als Dashboard mit Infos zum Projekt  
- Anpassung der Titel für besseres Verständnis  
- Ergänzung von Untertiteln  

**Interaktionen**

- Linkage im Alters-Tab ergänzt  
- Sortierfunktion für Tabelle integriert  
- Filter optimiert und entfernt wo nicht relevant.
