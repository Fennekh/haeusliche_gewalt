import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Farben
color_women = "#7B1E1E"
color_men = "Royalblue"
color_all = "black"

# Daten laden und filtern
opfer = pd.read_csv("data/geschaedigte_tidy.csv")
taeter = pd.read_csv("data/beschuldigte_tidy.csv")

opfer = opfer[(opfer["Delikt"] == "Total Häusliche Gewalt") & (opfer["Anzahl_geschaedigter_Personen_Total"])]
taeter = taeter[(taeter["Delikt"] == "Total Häusliche Gewalt") & (taeter["Anzahl_beschuldigter_Personen_Total"])]

opfer_maenlich = opfer[opfer["Geschlecht"] == "männlich"]
opfer_weiblich = opfer[opfer["Geschlecht"] == "weiblich"]


taeter_maenlich = taeter[taeter["Geschlecht"] == "männlich"]
taeter_weiblich = taeter[taeter["Geschlecht"] == "weiblich"]


# Layout
layout = html.Div([
    html.H3("Geschlechterverhältnis im Zeitverlauf", style={'textAlign': 'left', 'marginTop': 20}),

    dbc.Row([
        dbc.Col(dcc.Graph('graph-beziehung'), width=8),
        dbc.Col(html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009–2024)"))
    ]),
    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009–2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])

# Callbacks
def register_callbacks(app):


    @app.callback(
        Output('graph-beziehung', 'figure'),
        Input('graph-beziehung', 'id')
    )
    def update_beziehung_graph(_):
        # Beispiel-Daten
        gruppen = ['männlich', 'weiblich']
        Beziehungsart = ['Partnerschaft',
   'ehemalige Partnerschaft',
   'Eltern-Kind-Beziehung',
   'andere Verwandtschaftsbeziehung']

        # Fiktive Werte
        werte = {
            'männlich': [50, 80, 30, 60],
            'weiblich': [40, 70, 20, 90]
        }

        # Leere Scatter-Traces
        fig = go.Figure()

        for gruppe in gruppen:
            fig.add_trace(go.Scatter(
                x=Beziehungsart,
                y=[gruppe] * len(Beziehungsart),
                mode='markers',
                marker=dict(
                    size=opfer["Anzahl_geschaedigter_Personen_Total"],
                    sizemode='area',
                    sizeref=2. * max(opfer["Anzahl_geschaedigter_Personen_Total"]) / 100 ** 2,
                    sizemin=5,
                    line=dict(width=1, color='DarkSlateGrey')
                ),
                name=gruppe
            ))

        # Layout anpassen
        fig.update_layout(
            title='Bubble Plot mit 2x4 Kategorien',
            xaxis_title='Gruppe',
            yaxis_title='Altersgruppe',
            showlegend=True,
            height=600
        )

        return fig

