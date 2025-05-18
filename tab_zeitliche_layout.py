import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Daten aus der ursprünglichen Datei
opfer_data = [
    {"year": 2009, "totalMale": 2319, "totalFemale": 7397, "ageGroups": {
        "male": {"<10": 178, "10-19": 276, "20-29": 364, "30-39": 491, "40-49": 555, "50-59": 287, "60-69": 121,
                 "70+": 47},
        "female": {"<10": 205, "10-19": 774, "20-29": 2016, "30-39": 2068, "40-49": 1570, "50-59": 522, "60-69": 178,
                   "70+": 63}}},
    # ... Rest der Daten einfügen ...
]

taeter_data = [
    {"year": 2009, "totalMale": 7476, "totalFemale": 1772, "ageGroups": {
        "male": {"<10": 0, "10-19": 354, "20-29": 1709, "30-39": 2190, "40-49": 2022, "50-59": 859, "60-69": 254,
                 "70+": 84},
        "female": {"<10": 0, "10-19": 84, "20-29": 424, "30-39": 601, "40-49": 455, "50-59": 137, "60-69": 47,
                   "70+": 22}}},
    # ... Rest der Daten einfügen ...
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

# Layout für den Tab "Zeitliche Entwicklung"
layout = html.Div([
    html.Div([
        html.H4("Zeitraum auswählen:", style={'marginBottom': 10}),
        dcc.RangeSlider(
            id='jahr-slider-tab1',
            min=2009,
            max=2024,
            value=[2009, 2024],
            marks={year: str(year) for year in range(2009, 2025)},
            step=1
        )
    ], style={'width': '80%', 'margin': 'auto', 'marginBottom': 30, 'marginTop': 20}),

    # Information zum aktuell ausgewählten Zeitraum
    html.Div(id='zeitraum-info-tab1', style={'textAlign': 'center', 'marginBottom': 20}),

    # Zeitliche Entwicklung nach Geschlecht
    html.Div([
        html.H3("Zeitliche Entwicklung von Opfern und Tätern nach Geschlecht",
                style={'textAlign': 'center', 'marginTop': 20}),
        dcc.Graph(id='zeitliche-entwicklung')
    ]),

    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009-2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])

# Hier registrieren wir die Callbacks für diesen Tab
def register_callbacks(app):
    # Callback für zeitliche Entwicklung
    @app.callback(
        Output('zeitliche-entwicklung', 'figure'),
        [Input('zeitliche-entwicklung', 'id'),
         Input('jahr-slider-tab1', 'value')]
    )
    def update_zeitliche_entwicklung(_, jahr_bereich):
        jahr_start, jahr_ende = jahr_bereich

        # Daten nach Zeitraum filtern
        opfer_gefiltert = opfer_yearly[(opfer_yearly['Jahr'] >= jahr_start) & (opfer_yearly['Jahr'] <= jahr_ende)]
        taeter_gefiltert = taeter_yearly[(taeter_yearly['Jahr'] >= jahr_start) & (taeter_yearly['Jahr'] <= jahr_ende)]

        # Daten vorbereiten
        opfer_melted = pd.melt(opfer_gefiltert, id_vars=['Jahr'], value_vars=['Männliche Opfer', 'Weibliche Opfer'],
                               var_name='Gruppe', value_name='Anzahl')
        taeter_melted = pd.melt(taeter_gefiltert, id_vars=['Jahr'], value_vars=['Männliche Täter', 'Weibliche Täter'],
                                var_name='Gruppe', value_name='Anzahl')

        # Daten zusammenführen
        all_data = pd.concat([opfer_melted, taeter_melted])

        # Farben definieren
        colors = {
            'Männliche Opfer': '#2d6bbd',
            'Weibliche Opfer': '#64a7f5',
            'Männliche Täter': '#a83232',
            'Weibliche Täter': '#e05a5a'
        }

        # Visualisierung erstellen
        fig = px.line(all_data, x='Jahr', y='Anzahl', color='Gruppe',
                      color_discrete_map=colors,
                      markers=True, line_shape='linear')

        # Layout anpassen
        fig.update_layout(
            title=f"Entwicklung der Opfer- und Täterzahlen nach Geschlecht ({jahr_start}-{jahr_ende})",
            xaxis_title="Jahr",
            yaxis_title="Anzahl Personen",
            legend_title="Gruppe",
            template="plotly_white",
            hovermode="x unified"
        )

        return fig

    # Callback für die Anzeige des ausgewählten Zeitraums
    @app.callback(
        Output('zeitraum-info-tab1', 'children'),
        [Input('jahr-slider-tab1', 'value')]
    )
    def update_zeitraum_info(jahr_bereich):
        jahr_start, jahr_ende = jahr_bereich
        if jahr_start == jahr_ende:
            return f"Ausgewähltes Jahr: {jahr_start}"
        else:
            return f"Ausgewählter Zeitraum: {jahr_start} - {jahr_ende}"
