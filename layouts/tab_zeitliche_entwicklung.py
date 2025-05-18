import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Importieren der gemeinsamen Daten
from layouts.data import load_data

# Daten laden
data_dict = load_data()
opfer_yearly = data_dict['opfer_yearly']
taeter_yearly = data_dict['taeter_yearly']

# Layout für den ersten Tab (Zeitliche Entwicklung)
layout = html.Div([
    # Globaler Zeitregler (Slider)
    html.Div([
        html.H4("Zeitraum auswählen:", style={'marginBottom': 10}),
        dcc.RangeSlider(
            id='jahr-slider-tab1',  # Eindeutige ID
            min=2009,
            max=2024,
            value=[2009, 2024],  # Standardmäßig den gesamten Zeitraum anzeigen
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
    def update_zeitraum_info_tab1(jahr_bereich):
        jahr_start, jahr_ende = jahr_bereich
        if jahr_start == jahr_ende:
            return f"Ausgewähltes Jahr: {jahr_start}"
        else:
            return f"Ausgewählter Zeitraum: {jahr_start} - {jahr_ende}"
