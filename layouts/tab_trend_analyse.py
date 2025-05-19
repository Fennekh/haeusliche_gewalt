import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.validators.scatter.marker import SymbolValidator
from dash import dash_table

# Importieren der gemeinsamen Daten
from layouts.data import load_data

#Variabeln
color_women= "maroon"
color_men = "royalblue"
color_all = "black"


#------
#Daten laden
opfer = pd.read_csv("/Users/karinhugentobler/PycharmProjects/dashboard_haeusliche_gewalt/data/geschaedigte_tidy.csv")
taeter = pd.read_csv("/Users/karinhugentobler/PycharmProjects/dashboard_haeusliche_gewalt/data/beschuldigte_tidy.csv")
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
#----

# Altersgruppen festlegen
age_order = [
    '<10 Jahre', '10 - 19 Jahre', '20 - 29 Jahre', '30 - 39 Jahre',
    '40 - 49 Jahre', '50 - 59 Jahre', '60 - 69 Jahre', '70 Jahre und +'
]

##

# Daten aus der ursprünglichen Datei
opfer_data = [
    {"year": 2009, "totalMale": 2319, "totalFemale": 7397, "ageGroups": {
        "male": {"<10": 178, "10-19": 276, "20-29": 364, "30-39": 491, "40-49": 555, "50-59": 287, "60-69": 121,
                 "70+": 47},
        "female": {"<10": 205, "10-19": 774, "20-29": 2016, "30-39": 2068, "40-49": 1570, "50-59": 522, "60-69": 178,
                   "70+": 63}}},
    # ... Rest der Daten gekürzt, im vollständigen Code müssen alle Datensätze eingefügt werden
]

taeter_data = [
    {"year": 2009, "totalMale": 7476, "totalFemale": 1772, "ageGroups": {
        "male": {"<10": 0, "10-19": 354, "20-29": 1709, "30-39": 2190, "40-49": 2022, "50-59": 859, "60-69": 254,
                 "70+": 84},
        "female": {"<10": 0, "10-19": 84, "20-29": 424, "30-39": 601, "40-49": 455, "50-59": 137, "60-69": 47,
                   "70+": 22}}},
    # ... Rest der Daten gekürzt, im vollständigen Code müssen alle Datensätze eingefügt werden
]

# Daten in DataFrames umwandeln für bessere Verarbeitung
# Opfer nach Jahr und Geschlecht
opfer_yearly = pd.DataFrame([(item['year'], item['totalMale'], item['totalFemale'])
                             for item in opfer_data],
                            columns=['Jahr', 'Männliche Opfer', 'Weibliche Opfer'])

# Täter nach Jahr und Geschlecht
taeter_yearly = pd.DataFrame([(item['year'], item['totalMale'], item['totalFemale'])
                              for item in taeter_data],
                             columns=['Jahr', 'Männliche Täter', 'Weibliche Täter'])

# Altersgruppen für alle Jahre
opfer_age_all_years = []
taeter_age_all_years = []

for data in opfer_data:
    year = data['year']
    for gender, gender_label in [('male', 'Männlich'), ('female', 'Weiblich')]:
        for age_group, count in data['ageGroups'][gender].items():
            opfer_age_all_years.append((year, gender_label, age_group, count))

for data in taeter_data:
    year = data['year']
    for gender, gender_label in [('male', 'Männlich'), ('female', 'Weiblich')]:
        for age_group, count in data['ageGroups'][gender].items():
            taeter_age_all_years.append((year, gender_label, age_group, count))

opfer_age_df = pd.DataFrame(opfer_age_all_years, columns=['Jahr', 'Geschlecht', 'Altersgruppe', 'Anzahl'])
taeter_age_df = pd.DataFrame(taeter_age_all_years, columns=['Jahr', 'Geschlecht', 'Altersgruppe', 'Anzahl'])

# Altersgruppensortierung festlegen
age_order = ['<10', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70+']
opfer_age_df['Altersgruppe'] = pd.Categorical(opfer_age_df['Altersgruppe'], categories=age_order, ordered=True)
taeter_age_df['Altersgruppe'] = pd.Categorical(taeter_age_df['Altersgruppe'], categories=age_order, ordered=True)

# Layout für den dritten Tab (Trend-Analyse)
layout = html.Div([
    # Globaler Zeitregler (Slider)
    html.Div([
        html.H4("Zeitraum auswählen:", style={'marginBottom': 10}),
        dcc.RangeSlider(
            id='jahr-slider-tab3',  # Eindeutige ID
            min=2009,
            max=2024,
            value=[2009, 2024],
            marks={year: str(year) for year in range(2009, 2025)},
            step=1
        )
    ], style={'width': '80%', 'margin': 'auto', 'marginBottom': 30, 'marginTop': 20}),

    # Information zum aktuell ausgewählten Zeitraum
    html.Div(id='zeitraum-info-tab3', style={'textAlign': 'center', 'marginBottom': 20}),

    # Trend-Analyse
    html.Div([
        html.H3("Entwicklung der Altersgruppen über die Jahre",
                style={'textAlign': 'center', 'marginTop': 30}),
        html.Div([
            dcc.RadioItems(
                id='trend-selector',
                options=[
                    {'label': 'Opfer', 'value': 'opfer'},
                    {'label': 'Täter', 'value': 'taeter'}
                ],
                value='opfer',
                labelStyle={'marginRight': 20},
                style={'display': 'inline-block', 'marginRight': 30}
            ),
            dcc.Dropdown(
                id='gender-selector-trend',
                options=[
                    {'label': 'Männlich', 'value': 'Männlich'},
                    {'label': 'Weiblich', 'value': 'Weiblich'}
                ],
                value='Weiblich',
                style={'width': '200px', 'display': 'inline-block'}
            )
        ], style={'textAlign': 'center', 'marginBottom': 20}),
        dcc.Graph(id='altersgruppen-trend')
    ]),

    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009-2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])

# Hier registrieren wir die Callbacks für diesen Tab
def register_callbacks(app):
    # Callback für Trend-Analyse
    @app.callback(
        Output('altersgruppen-trend', 'figure'),
        [Input('trend-selector', 'value'),
         Input('gender-selector-trend', 'value'),
         Input('jahr-slider-tab3', 'value')]
    )
    def update_altersgruppen_trend(perspektive, geschlecht, jahr_bereich):
        jahr_start, jahr_ende = jahr_bereich

        # Daten filtern
        if perspektive == 'opfer':
            df = opfer_age_df[(opfer_age_df['Geschlecht'] == geschlecht) &
                              (opfer_age_df['Jahr'] >= jahr_start) &
                              (opfer_age_df['Jahr'] <= jahr_ende)]
            title = f"Entwicklung der Altersgruppen bei {geschlecht.lower()}n Opfern ({jahr_start}-{jahr_ende})"
            if geschlecht == 'Männlich':
                color_scale = px.colors.sequential.Blues
            else:
                color_scale = px.colors.sequential.Blues_r
        else:
            df = taeter_age_df[(taeter_age_df['Geschlecht'] == geschlecht) &
                               (taeter_age_df['Jahr'] >= jahr_start) &
                               (taeter_age_df['Jahr'] <= jahr_ende)]
            title = f"Entwicklung der Altersgruppen bei {geschlecht.lower()}n Tätern ({jahr_start}-{jahr_ende})"
            if geschlecht == 'Männlich':
                color_scale = px.colors.sequential.Reds
            else:
                color_scale = px.colors.sequential.Reds_r

        # Pivot-Tabelle erstellen
        pivot_df = df.pivot(index='Jahr', columns='Altersgruppe', values='Anzahl')

        # Visualisierung erstellen
        fig = px.line(pivot_df, markers=True, line_shape='linear', color_discrete_sequence=color_scale)

        # Layout anpassen
        fig.update_layout(
            title=title,
            xaxis_title="Jahr",
            yaxis_title="Anzahl Personen",
            legend_title="Altersgruppe",
            template="plotly_white",
            hovermode="x unified"
        )

        return fig

    # Callback für die Anzeige des ausgewählten Zeitraums
    @app.callback(
        Output('zeitraum-info-tab3', 'children'),
        [Input('jahr-slider-tab3', 'value')]
    )
    def update_zeitraum_info_tab3(jahr_bereich):
        jahr_start, jahr_ende = jahr_bereich
        if jahr_start == jahr_ende:
            return f"Ausgewähltes Jahr: {jahr_start}"
        else:
            return f"Ausgewählter Zeitraum: {jahr_start} - {jahr_ende}"
