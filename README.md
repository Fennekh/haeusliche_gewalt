## # Dashboard zu Häuslicher Gewalt in der Schweiz 2009–2024

Ein interaktives Dashboard zur Visualisierung und Analyse der Entwicklung von häuslicher Gewalt von 2009 bis 2024 nach Delikten sowie der Gesamtentwicklung der Betroffenen (Täter:innen und Opfer) und deren Eigenschaften (Geschlecht, Alter, Beziehung zwischen Täter:innen und Opfer). Erstellt mit Python und Dash.

### Ziel des Dashboards

Das Dashboard soll es der Schweizer Bevölkerung, Behörden und Beratungsstellen dabei ermöglichen, die Entwicklung häuslicher Gewalt zu analysieren, zu erkennen, wer die Betroffenen (Täter:innen und Opfer) sind und in welcher Beziehung sie zueinander standen.  
*Ziel:* Bewusstsein und Sichtbarkeit für häusliche Gewalt erhöhen.

### Disclaimer

Die Dunkelziffer bei Häuslicher Gewalt wird sehr hoch geschätzt. 
Bei Tätlichkeiten und Körperverletzungen werden z. B. 28,9 %, bei sexueller Gewalt 10,5 % 
der Fälle angezeigt.

Quelle: https://www.unisg.ch/de/newsdetail/news/hsg-strafrechtlerin-leuchtet-die-dunkelziffer-der-haeusli-chen-gewalt-aus/, Univeristät St.Gallen, 26.10.2023, zuletzt abgerufen: 09.06.2025 

### Datenquelle

Wir nutzen dafür die Daten des Bundesamts für Statistik. Die Polizeistatistik 2009–2024 (Letzte Aktualisierung: 22.04.2025):

- **Strafgesetzbuch (StGB)**: Straftaten häusliche Gewalt und beschuldigte Personen  
  https://www.bfs.admin.ch/bfs/de/home/statistiken/kriminalitaet-strafrecht/polizei/haeusliche-gewalt.assetdetail.34387386.html

- **Strafgesetzbuch (StGB)**: Straftaten häusliche Gewalt und geschädigte Personen  
  https://www.bfs.admin.ch/bfs/de/home/statistiken/kriminalitaet-strafrecht/polizei/haeusliche-gewalt.assetdetail.34387408.html

Folgende Attribute sind jeweils für Täter:innen und Opfer vorhanden und für 30 verschiedene Deliktarten sowie männlich/weiblich differenziert:

| Attribut                      | Beschreibung                                                                 |
|------------------------------|------------------------------------------------------------------------------|
| `Straftaten Total`           | Anzahl Straftaten pro Delikt                                                |
| `Straftaten Mehrfach (2)`    | Anteil der mehrfach verübten Straftaten                                     |
| `Beschuldigte/Geschädigte Total` | Anzahl Personen pro Delikt                                                |
| `Alter`                      | 13 Alterskategorien, reduziert auf 8 (10-Jahres-Schritte), in Anzahl Personen |
| `Beziehungsart`              | Beziehung zwischen den Personen (4 Kategorien: Partnerschaft, ehemalige Partnerschaft, Eltern-Kind-Beziehung, andere Verwandtschaft) |

**Hinweise:**  
(2) In Fällen, in denen die gleiche Person von derselben Täterschaft zu mehreren Zeitpunkten auf die gleiche Art wiederholt geschädigt wird, ohne dass eine separate Anzeige bzw. ein separater Rapport erfolgt, wird der betreffende Straftatbestand mit „mehrfach“ gekennzeichnet. 

### Metadaten im Dashboard

- **Aktualisierungsdatum** der Daten (z. B. „Letzte Aktualisierung: 09. Mai 2025“)
- **Datenquelle** (z. B. „Simulierte Smart-Meter-Daten v2.1“)
- **Hinweis zu Verbrauchseinheiten** (Tooltips bei Diagrammen)
- **Haftungsausschluss** im Fußbereich


### Datenschutz und Datenanonymisierung
Datenschutzmassnahmen des BFS

Das Bundesamt für Statistik wendet strenge Datenschutzrichtlinien an, um die Anonymität der Betroffenen zu gewährleisten:

- Statistische Geheimhaltung: Alle Daten werden vollständig anonymisiert veröffentlicht - keine Rückschlüsse auf Einzelpersonen möglich
- Schwellenwertregelung: Bei Totalwerten zwischen 1-3 Personen werden Detailinformationen (Alter, Beziehungsart) aus Datenschutzgründen nicht ausgewiesen
- Geografische Anonymisierung: Keine kleinräumigen geografischen Zuordnungen unter kantonaler Ebene
- Zeitliche Aggregation: Daten werden nur in Jahreszyklen veröffentlicht, nie tagesaktuell

### Visualisierungen und ihre Begründung

| Visualisierung                          | Warum gewählt?                                                                 |
|----------------------------------------|--------------------------------------------------------------------------------|
| **Tabelle**                             | Überblick über einzelne Delikte hinsichtlich Entwicklung, Geschlechterverhältnis, Beziehungsart und Alter |
| **Balkendiagramm**                      | Jahresverlauf der Straftaten zur Trendanalyse und Erkennung mehrfacher Straftaten |
| **Liniendiagramm (Betroffene)**         | Jahresverlauf der Betroffenenzahlen zur Analyse von Unterkategorien (Täter:innen, Opfer, Alter, Geschlecht) |
| **Balkendiagramme je Täter:innen/Opfer**| Jahresverlauf der prozentualen Anteile Betroffener nach Geschlecht             |
| **Liniendiagramm (Geschlecht)**         | Entwicklung der absoluten Zahlen nach Geschlecht                               |
| **Gruppiertes Balkendiagramm**          | Absolute Zahlen je Beziehungsart im gewählten Jahr, differenziert nach Geschlecht |
| **Liniendiagramm (Alter)**              | Jahresverlauf nach Alterskategorien                                            |
| **Alterspyramide**                      | Detailanalyse der Altersverteilung in einem bestimmten Jahr nach Geschlecht    |


### Page Layout

Ein stratifiziertes Layout:

- *Oben:* Webseitentitel zur Darstellung des Oberthemas  
- *Ebene 2:* Navigation zur Seitenübersicht  
- *Ebene 3:* Abschnittstitel in Frageform  
- *Ebene 4:* Filter und Anzeigeeinstellungen  
- *Ebene 5:* Interaktive Diagramme, Tabelle, erläuternder Text  
- *Unten:* Hinweise, Quellen, Haftungsausschluss


### Seitenorganisation (Structure)

- *Seite 1:* Übersicht (Delikte im tabellarischen Überblick)  
- *Seite 2:* Zeitliche Entwicklung (Jahresverlauf)  
- *Seite 3:* Geschlechterverhältnis  
- *Seite 4:* Beziehungsart (Täter-Opfer-Beziehung)  
- *Seite 5:* Altersverteilung  
- *Seite 6:* Impressum (Metadaten, Rechtliches)


### Interaktionen

- Sortier-Button für auf-/absteigende Sortierung nach Anzahl Straftaten  
- Toggle: Straftaten vs. Betroffene  
- Toggle: Prozentual vs. Absolut  
- Dropdown: Jahrsauswahl  
- Dropdown: Geschlecht  
- Radio-Button: Täter:innen-/Opfer-Ansicht  
- Linkage (Fokus) zur Detailansicht eines Jahres  
- Hover Tooltips mit Werten und Erklärungen  
- Zoom & Pan in Diagrammen  
- Tabs zur Seitennavigation  


### Farbauswahl

- *Datenkodierung:* Frauen (Rot), Männer (Blau), Gesamt (Schwarz)  
- *Semantische Farben:* Helligkeitsabstufungen für einfache/mehrfache Straftaten  
- *Barrierefreiheit:* Hoher Kontrast, keine ausschliessliche Farbcodierung


### Strukturmuster

- *Detail-on-Demand:* Genaue Zahlen und Erklärungen beim Mouseover  
- *Fokus + Kontext:* Hauptvisualisierung mit Filtern  
- *Hierarchische Navigation:* Vom Überblick zu Details  
- *Konsistente Achsenbeschriftung:* Y-Achse = Personenanzahl, X-Achse = Zeit/Kategorien  
- *Responsive Layout:* Anpassung an Bildschirmgrößen


### Limitationen

### Datenbedingte Einschränkungen

- Hohe Dunkelziffer – nur angezeigte Fälle enthalten  
- Datenschutz – Werte 1–3 nicht sichtbar  
- Beziehungsart – nicht nach Geschlecht differenziert  
- Mehrfachstraftaten – erschwerte Zuordnung


### Was nicht geklappt hat

- Tabellen nicht mobiloptimiert, keine Hover-Details  
- Delikt-spezifische Filterung nicht umgesetzt  
- Keine automatischen Updates bei neuen BFS-Daten


### Technische Limitationen (Dash/Python)

- Komplexe Callback-Struktur bei vielen Filtern  
- Performance-Einbrüche bei vollständiger Datenanzeige  
- Responsiveness nur eingeschränkt auf mobilen Geräten  
- Dash DataTable mit begrenzten Styling-Optionen

## Verbesserungsideen

- Integration der BFS-API für automatische Datenupdates  
- Deliktspezifische Filterung zur Fokussierung  
- Export-Funktion für Diagramme und Tabellen  
- Vergleichstool für Kantone (sofern Daten verfügbar)  
- Migration zu Dash Bootstrap Components  
- Kontextuelle Hilfen für rechtliche/statistische Begriffe


### Feedback-Umsetzung von Tag 7
*(Inhalt bei Bedarf ergänzen)*

**Metadata**
- Quelle & Beschreibung ergänzt  
- Datenschutzhinweise explizit gemacht

**Visual Representation**
- *Beziehungsgrafik:*
  - Titel & Hoverinfo ergänzt (Diskrepanzen erklärt)
  - Wechsel von Stacked zu gruppiertem Balkendiagramm
  - Umstellung auf absolute Zahlen
  - Vertikale Balken (Frauen = links/Rot, Männer = rechts/Blau)
- *Alterspyramide:* Umgedreht für intuitive Darstellung

**Page Layout**
- Tabelle auf Seite 1 verschoben  
- Layout „Zeitliche Entwicklung“ angepasst  
- Gegenüberstellung zweier Pyramiden verworfen  
- Linkage-Funktion für Alters-Detailansicht

**Vereinheitlichung Layout/Grafiken**
- Achsen konsistent (Y = Personenanzahl, X = Zeit/Kategorien)  
- Vertikale Balken für Geschlechterverhältnis  
- Farbzuordnung konsequent: Rot = Frauen, Blau = Männer

**Farben**
- Farbpalette reduziert auf Rot, Blau, Schwarz  
- Linienbeschriftung direkt auf der Altersgrafik mit Hovereffekt

**Text**
- Reduktion auf Seite 2 für bessere Übersicht  
- Vollständiges Impressum mit rechtlichen Hinweisen

**Interaktionen**
- Linkage im Alterstab ergänzt  
- Sortierfunktion für Tabelle integriert  
- Filter optimiert und auf Seitenrelevanz reduziert
