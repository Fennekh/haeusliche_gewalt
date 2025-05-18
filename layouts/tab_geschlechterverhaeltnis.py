import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

# Layout für den zweiten Tab (Geschlechterverhältnis)
layout = html.Div([
    # Globaler Zeitregler (Slider)
    html.Div([
        html.H4("Zeitraum auswählen:", style={'marginBottom': 10}),
        dcc.RangeSlider(
            id='jahr-slider-tab2',  # Eindeutige ID
            min=2009,
            max=2024,
            value=[2009, 2024],
            marks={year: str(year) for year in range(2009, 2025)},
            step=1
        )
    ], style={'width': '80%', 'margin': 'auto', 'marginBottom': 30, 'marginTop': 20}),

    # Information zum aktuell ausgewählten Zeitraum
    html.Div(id='zeitraum-info-tab2', style={'textAlign': 'center', 'marginBottom': 20}),

    # Geschlechterverhältnis
    html.Div([
        html.H3("Geschlechterverhältnis im Zeitverlauf",
                style={'textAlign': 'center', 'marginTop': 20}),
        dcc.Graph(id='geschlechterverhaeltnis')
    ]),

    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009-2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])

# Hier registrieren wir die Callbacks für diesen Tab
def register_callbacks(app):
    # Callback für Geschlechterverhältnis
    @app.callback(
        Output('geschlechterverhaeltnis', 'figure'),
        [Input('geschlechterverhaeltnis', 'id'),
         Input('jahr-slider-tab2', 'value')]
    )
    def update_geschlechterverhaeltnis(_, jahr_bereich):
        jahr_start, jahr_ende = jahr_bereich

        # Daten nach Zeitraum filtern
        opfer_gefiltert = opfer_yearly[(opfer_yearly['Jahr'] >= jahr_start) & (opfer_yearly['Jahr'] <= jahr_ende)]
        taeter_gefiltert = taeter_yearly[(taeter_yearly['Jahr'] >= jahr_start) & (taeter_yearly['Jahr'] <= jahr_ende)]

        # Prozentual berechnen
        opfer_percent = opfer_gefiltert.copy()
        opfer_percent['Total'] = opfer_percent['Männliche Opfer'] + opfer_percent['Weibliche Opfer']
        opfer_percent['Männliche Opfer %'] = (opfer_percent['Männliche Opfer'] / opfer_percent['Total']) * 100
        opfer_percent['Weibliche Opfer %'] = (opfer_percent['Weibliche Opfer'] / opfer_percent['Total']) * 100

        taeter_percent = taeter_gefiltert.copy()
        taeter_percent['Total'] = taeter_percent['Männliche Täter'] + taeter_percent['Weibliche Täter']
        taeter_percent['Männliche Täter %'] = (taeter_percent['Männliche Täter'] / taeter_percent['Total']) * 100
        taeter_percent['Weibliche Täter %'] = (taeter_percent['Weibliche Täter'] / taeter_percent['Total']) * 100

        # Subplot erstellen
        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=("Geschlechterverteilung bei Opfern", "Geschlechterverteilung bei Tätern"))

        # Opfer-Verteilung
        fig.add_trace(
            go.Bar(x=opfer_percent['Jahr'], y=opfer_percent['Männliche Opfer %'], name='Männliche Opfer',
                   marker_color='#2d6bbd'),
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(x=opfer_percent['Jahr'], y=opfer_percent['Weibliche Opfer %'], name='Weibliche Opfer',
                   marker_color='#64a7f5'),
            row=1, col=1
        )

        # Täter-Verteilung
        fig.add_trace(
            go.Bar(x=taeter_percent['Jahr'], y=taeter_percent['Männliche Täter %'], name='Männliche Täter',
                   marker_color='#a83232',
                   showlegend=False),
            row=1, col=2
        )
        fig.add_trace(
            go.Bar(x=taeter_percent['Jahr'], y=taeter_percent['Weibliche Täter %'], name='Weibliche Täter',
                   marker_color='#e05a5a',
                   showlegend=False),
            row=1, col=2
        )

        # Layout anpassen
        fig.update_layout(
            barmode='stack',
            title_text=f"Geschlechterverhältnis im Zeitverlauf ({jahr_start}-{jahr_ende})",
            template="plotly_white",
            height=600
        )

        # Y-Achsen anpassen
        fig.update_yaxes(title_text="Prozent (%)", range=[0, 100], row=1, col=1)
        fig.update_yaxes(title_text="Prozent (%)", range=[0, 100], row=1, col=2)

        return fig

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
