import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.validators.scatter.marker import SymbolValidator
from dash import dash_table
import matplotlib.pyplot as plt
import io
import plotly.io as pio

plotly_font = dict(
    family="Arimo, sans-serif",
    size=14,
    color="black"
)
pio.templates["arimo"] = go.layout.Template(layout=dict(font=plotly_font))
pio.templates.default = "arimo"


#------ Variabeln überall gleich

#Variabeln
color_women = "#811616"
color_men = "#0a0a35"
color_all = "black"


#----

text = """
## Daten: Statistik zu Häuslicher Gewalt in der Schweiz 2009–2024

Ein interaktives Dashboard zur Visualisierung und Analyse der Entwicklung von häuslicher Gewalt von 2009 bis 2024 nach Delikten sowie der Gesamtentwicklung der Betroffenen (Täter:innen und Opfer) und deren Eigenschaften (Geschlecht, Alter, Beziehung zwischen Täter:innen und Opfer). Erstellt mit **Python** und **Dash**.

### Ziel des Dashboards

Das Dashboard soll es der Schweizer Bevölkerung erleichtern, die Entwicklung häuslicher Gewalt zu analysieren, zu erkennen, wer die Betroffenen (Täter:innen und Opfer) sind und in welcher Beziehung sie zueinander standen. Dadurch sollen das Bewusstsein und die Sichtbarkeit für häusliche Gewalt erhöht werden.

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

Wir wählten ein **stratifiziertes Layout**:

- **1. Schicht**: Webseitentitel zur Darstellung des Oberthemas
- **2. Schicht**: Navigation zur Seitenübersicht
- **3. Schicht**: Abschnittstitel in Form einer Frage
- **4. Schicht**: Filter und Anzeigeeinstellungen der Inhalte
- **5. Schicht**: Interaktive Diagramme, Tabelle und erläuternder Text
- **6. Schicht**: Hinweise und Quellenangaben

### Seitenorganisation (Structure)

- **Seite 1: Übersicht einzelne Delikte**
- **Seite 2: Zeitliche Entwicklung**
- **Seite 3: Entwicklung Geschlechterverhältnis**
- **Seite 4: Beziehungsart**
- **Seite 5: Entwicklung Altersverteilung**
- **Seite 6: Impressum**

### Interaktionen

- **Sortier-Button** für auf- oder absteigende Sortierung nach Anzahl Straftaten
- **Toggle Straftaten/Betroffene Personen** für Umschaltung der Gesamtzahlen
- **Toggle Prozentual/Absolut** für Darstellung der Geschlechterverteilung
- **Dropdown Jahr** zur Jahresauswahl
- **Dropdown Geschlecht** zur Filterung
- **Radio-Button** zum Wechsel zwischen Täter:innen- und Opfer-Ansicht
- **Linkage (Fokus)** zur Detailansicht eines Jahres
- **Zoom & Pan** in Diagrammen
- **Tabs zur Navigation** zwischen Seiten

### Farbwahl

- **Datenkodierung**: Frau (Rot), Mann (Blau), Total (Schwarz); Helligkeitsabstufungen für einfache/mehrfache Straftaten
- **Barrierefreiheit**: Farben mit hohem Kontrast

### Strukturmuster

- **Detail-on-Demand**: Genaue Zahlen erscheinen beim Mouseover
- **Screenfit mit Overflow**: Inhalte passen auf die Seite; bei mobilen Geräten Scrollen aktiviert
- **Hierarchie**: KPIs oben, dann Kontext, dann Details

### Limitationen

- **Es wird von einer hohen Dunkelziffer ausgegangen. Die Zahlen sind daher mit Vorsicht zu genießen.**
- **Keine genauen Daten zur Beziehungsart nach Geschlecht (z. B. Eltern-Kind-Beziehung: Frau-Mann oder Frau-Frau nicht differenzierbar)**
- **Auf Deliktebene entfallen gewisse Informationen aus Datenschutzgründen (bei Totalwerten 1–3)**

### Was nicht geklappt hat

- **Tabelle ist nicht responsiv und zeigt keine genauen Daten beim Hover an**
- **Filterung nach Delikt nicht möglich**

### Technische Limitationen

- Kartenintegration mit Mapbox erforderte Token und Layout-Tuning
- Responsives Design nur eingeschränkt zuverlässig
- Komplexe Callbacks bei vielen Filtern
- Lange Ladezeiten bei großen Datenmengen

### Verbesserungsideen

- **Automatische Aktualisierung der Daten**
- **Filtermöglichkeiten für Delikte**

### Feedback-Umsetzung von Tag 7
*(Inhalt bei Bedarf ergänzen)*

**Metadata**
- Quelle und Beschreibung ergänzt

**Visual Representation**
- Beziehungsgrafik:
  - Titel und Hoverinfo ergänzt, um Diskrepanzen zwischen Täter:innen und Opferzahlen zu erklären
  - Wechsel von Stacked zu gruppiertem Barchart zur besseren Vergleichbarkeit
  - Umstellung auf absolute Zahlen zur Vermeidung von Verwirrung
  - Vertikale Balkendiagramme zur besseren Vergleichbarkeit
  - Farbcode: Rot links, Blau rechts

- Alterspyramide umgedreht

**Page Layout**
- Tabelle auf Seite 1 verschoben
- Layout „Zeitliche Entwicklung“ an „Entwicklung Alter“ angepasst
- Gegenüberstellung zweier Alterspyramiden verworfen zugunsten klarerer zeitlicher Entwicklung
- Alterstab enthält nun auch Linkage

**Vereinheitlichung Layout/Grafiken**
- Y-Achse: Personenanzahl; X-Achse: Zeit/Kategorien (Ausnahme Pyramide)
- Vertikale Balken für Geschlechterverhältnis beibehalten für bessere Vergleichbarkeit
- Farbzuordnung konsequent: Rot links, Blau rechts

**Colors**
- Reduktion auf klare Farben (Rot, Blau, Schwarz)
- Direkte Beschriftung der Linien bei Altersgrafik mit Hovereffekt

**Text**
- Text auf Seite 2 reduziert; Impressum erstellt

**Interaktionen**
- Linkage im Alterstab ergänzt
- Tabelle mit Sortierfunktion erweitert
- Filter je nach Relevanz erhalten
"""

layout = html.Div([dbc.Container([html.H2("Impressum", style={'textAlign': 'left', 'marginLeft': 0, 'paddingBottom': 48, 'marginTop': 48,  'fontWeight': 600 }),
    dcc.Markdown(text, style={"whiteSpace": "pre-wrap"})
], style={'margin': 40}, fluid=True)])


def register_callbacks(app):
    @app.callback(
        Output('impressum', 'figure'),
        Input('impressum', 'id')
    )
    def update_impressum(_):
        fig = go.Figure()
        return fig



