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
import base64

# Importieren der gemeinsamen Daten
from layouts.data import load_data

#Variabeln
color_women= "maroon"
color_men = "royalblue"
color_all = "black"


#------
#Daten laden
opfer = pd.read_csv("data/geschaedigte_tidy.csv")
taeter = pd.read_csv("data/beschuldigte_tidy.csv")

#Datenvorbereitung für Tabelle

# Nur Beziehungsart = Alle und Geschlecht = Total verwenden
taeter_filtered = taeter[(taeter["Beziehungsart"] == "Alle") & (taeter["Geschlecht"] == "Total")]

# Gruppieren nach Delikt und Jahr
taeter_grouped = taeter_filtered.groupby(['Delikt', 'Jahr'])['Anzahl_beschuldigter_Personen_Total'].sum().reset_index()

# Pivot-Tabelle: Delikt als Zeile, Jahre als Spalten
trend_pivot = taeter_grouped.pivot(index='Delikt', columns='Jahr', values='Anzahl_beschuldigter_Personen_Total')

# Fehlende Werte auffüllen (z. B. Delikte, die in 2009 oder 2024 nicht gemeldet wurden)
trend_pivot = trend_pivot.fillna(0)

# Mini-Trendliste + aktuelle Zahlen + Veränderung
trend_pivot['Anzahl'] = trend_pivot[2024]
trend_pivot['Trend'] = trend_pivot.apply(lambda row: row.loc[2009:2024].tolist(), axis=1)
trend_pivot['Veränderung (%)'] = ((trend_pivot[2024] - trend_pivot[2009]) / trend_pivot[2009].replace(0, 1)) * 100

# Sortieren nach Anzahl (2024)
trend_pivot_sorted = trend_pivot.sort_values(by='Anzahl', ascending=False).reset_index()

#Datenvorbereitung Grafiken
#Filtern nach Delikte gesamt
taeter = taeter[taeter["Delikt"] == "Total Häusliche Gewalt"]
opfer = opfer[opfer["Delikt"] == "Total Häusliche Gewalt"]

#Filtern nach Beziehungsart alle
taeter = taeter[taeter["Beziehungsart"] == "Alle"]
opfer = opfer[opfer["Beziehungsart"] == "Alle"]

#Filtern nach geschlecht
taeter_maenlich = taeter[taeter["Geschlecht"] == "männlich"]
taeter_weiblich = taeter[taeter["Geschlecht"] == "weiblich"]
taeter_total = taeter[taeter["Geschlecht"] == "Total"]

opfer_maenlich = opfer[opfer["Geschlecht"] == "männlich"]
opfer_weiblich = opfer[opfer["Geschlecht"] == "weiblich"]
opfer_total = opfer[opfer["Geschlecht"] == "Total"]

# --- Vorbereitung der Mini-Geschlechterbalken ---
opfer_agg = opfer[(opfer["Geschlecht"].isin(["männlich", "weiblich"])) & (opfer["Beziehungsart"] == "Alle")]
opfer_latest = opfer_agg[opfer_agg["Jahr"] == 2024]
geschlecht_pivot = opfer_latest.pivot_table(index="Delikt", columns="Geschlecht", values="Anzahl_geschaedigter_Personen_Total", aggfunc="sum").fillna(0)

geschlecht_balken = {}
for delikt, row in geschlecht_pivot.iterrows():
    fig, ax = plt.subplots(figsize=(2, 0.3))
    total = row["männlich"] + row["weiblich"]
    if total == 0:
        ratio_m = ratio_w = 0.5
    else:
        ratio_m = row["männlich"] / total
        ratio_w = row["weiblich"] / total

    ax.barh([0], [ratio_m], color=color_men)
    ax.barh([0], [ratio_w], left=[ratio_m], color=color_women)
    ax.set_xlim(0, 1)
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    geschlecht_balken[delikt] = f"data:image/png;base64,{img_b64}"


#------
# Funktion zur Erstellung von Mini-Trendgrafiken als base64
table_data = []
for _, row in trend_pivot_sorted.iterrows():
    fig, ax = plt.subplots(figsize=(2, 0.5))
    ax.plot(row['Trend'], linewidth=1.5)
    ax.set_axis_off()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    trend_img = f"data:image/png;base64,{img_base64}"

    table_data.append({
        'Delikt': row['Delikt'],
        'Anzahl': int(row['Anzahl']),
        'Trend_src': trend_img,
        'Veränderung': f"{row['Veränderung (%)']:.1f} %",
        'Geschlechterverhältnis_src': geschlecht_balken.get(row['Delikt'], "")
    })


#----

# Layout für den ersten Tab (Zeitliche Entwicklung)
layout = html.Div([
    # Zeitraum-Information
    html.Div(id='zeitraum-info-tab1', style={'textAlign': 'center', 'marginBottom': 20}),





    # Tabelle + weitere Visualisierungen
    dbc.Row([
        dbc.Col([
            html.H4("Übersicht Delikte", style={'marginTop': 30, 'marginLeft': 20}),
            html.Table([
                html.Thead(
                    html.Tr([
                        html.Th("Delikt"),
                        html.Th("Anzahl 2024"),
                        html.Th("Trend 2009–2024"),
                        html.Th("Veränderung (%)"),
                        html.Th("Geschlechterverhältnis (Opfer)"),
                        html.Th("Geschlechterverhältnis (Täter)"),
                        html.Th("Häufigstes Alter (Opfer)"),
                        html.Th("Häufigstes Alter (Täter)"),
                    ])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(row['Delikt']),
                        html.Td(row['Anzahl']),
                        html.Td(html.Img(src=row['Trend_src'], style={'height': '30px'})),
                        html.Td(row['Veränderung']),
                        html.Td(html.Img(src=row['Geschlechterverhältnis_src'], style={'height': '20px'})),
                        html.Td(html.Img(src=row['Geschlechterverhältnis_src'], style={'height': '20px'})),
                        html.Td("20-30 Jahre"),
                        html.Td("40-50 Jahre"),


                    ]) for row in table_data
                ])
            ], style={'width': '95%', 'borderCollapse': 'collapse',  'margin': 20})

    ]),

    # Fußnote
    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009–2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])
])


# Hier registrieren wir die Callbacks für diesen Tab
def register_callbacks(app):



    # Callback für die Anzeige des ausgewählten Zeitraums
    @app.callback(
        Output('zeitraum-info-tab2', 'children'),
        [Input('jahr-slider-tab2', 'value')]
    )
    def update_zeitraum_info_tab2(jahr_bereich):
        jahr_start, jahr_ende = jahr_bereich
        if jahr_start == jahr_ende:
            return f"Ausgewähltes Jahr: {jahr_start}"
        else:
            return f"Ausgewählter Zeitraum: {jahr_start} - {jahr_ende}"
