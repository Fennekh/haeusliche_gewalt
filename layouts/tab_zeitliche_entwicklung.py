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


#------

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
    ],  style={'width': '80%', 'margin': 'auto', 'marginBottom': 30, 'marginTop': 20}),

    # Information zum aktuell ausgewählten Zeitraum
    html.Div(id='zeitraum-info-tab1', style={'textAlign': 'center', 'marginBottom': 20}),

    # Zeitliche Entwicklung nach Geschlecht
    html.Div([
        html.H3("Zeitliche Entwicklung von Opfern und Tätern nach Geschlecht",
                style={'textAlign': 'left', 'marginTop': 20, 'marginLeft': 20}),
        dbc.Row([

        dbc.Col(dcc.Graph(id='zeitliche-entwicklung-straftaten'), width=8),
        dbc.Col(html.Div([
                    html.H3("Zeitliche Entwicklung von Opfern und Tätern nach Geschlecht"),
                    html.P("In Fällen, in denen die gleiche Person derselben Täterschaft zu mehreren Zeitpunkten auf die gleiche Art wiederholt geschädigt wird, ohne dass eine separate Anzeige bzw. ein separater Rapport erfolgt, wird der betreffende Straftatbestand mit „mehrfach“ gekennzeichnet. "),
                    html.H1("16'349"),
                    html.P("Straftaten 2024")

                ]), width=2, style={'marginTop': 20, 'marginLeft': 20}),


        ]),
        dbc.Row([

            dbc.Col(
            html.Div([
                html.H3("Delikte", style={'marginTop': 30}),

                dash_table.DataTable(
                    id='daten-tabelle',
                    columns=[  # Platzhalter-Spalten
                        {'name': 'Delikt', 'id': 'Delikt'},
                        {'name': 'Anzahl', 'id': 'Anzahl'},
                        {'name': 'Trend als linie', 'id': 'Anzahl'},
                        {'name': 'Veränderung Seit 2009 in prozent', 'id': 'Anzahl'},
                    ],
                    data=[],  # Leerer Start
                    style_table={'overflowX': 'auto'},
                    style_cell={'padding': '8px', 'textAlign': 'left'},
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    },
                    page_size=10  # Anzahl Zeilen pro Seite
                )
            ]), width=4 ),

            dbc.Col(dcc.Graph(id='zeitliche-entwicklung-taeter-opfer'), width=4),

            dbc.Col(html.Div([
                html.H3("Zeitliche Entwicklung von Opfern und Tätern"),
                html.P(
                    "In Fällen, in denen die gleiche Person derselben Täterschaft zu mehreren Zeitpunkten auf die gleiche Art wiederholt geschädigt wird, ohne dass eine separate Anzeige bzw. ein separater Rapport erfolgt, wird der betreffende Straftatbestand mit „mehrfach“ gekennzeichnet."
                ),
                dbc.Row([
                    dbc.Col([
                        html.H2("16'349"),
                        html.P("Opfer 2024")
                    ]),
                    dbc.Col([
                        html.H2("5'671"),
                        html.P("Täter")
                    ])
                ])
            ]), width=2),



        ])

    ]),

    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009-2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])

# Hier registrieren wir die Callbacks für diesen Tab
def register_callbacks(app):
    @app.callback(
        Output('zeitliche-entwicklung-straftaten', 'figure'),
        [Input('zeitliche-entwicklung-straftaten', 'id'),
         Input('jahr-slider-tab1', 'value')]
    )
    def update_zeitliche_entwicklung_straftaten(_, jahr_bereich):
        jahr_start, jahr_ende = jahr_bereich

        # Daten nach Zeitraum filtern
        opfer_gefiltert = opfer_total[(opfer_total['Jahr'] >= jahr_start) & (opfer_total['Jahr'] <= jahr_ende)]

        # Opfer über Zeit Visualisierung erstellen
        # Erstelle die Grafik
        fig = go.Figure()

        # bar für Straftaten total


        fig.add_trace(go.Bar(
            x=opfer_total['Jahr'],
            y=opfer_total['Straftaten_Total'],
            name='Straftaten Total',
            width=0.8,
            marker_color=color_all,
        marker = dict(
            color=color_all,  # Hintergrundfarbe
            pattern=dict(
                shape="x",  # Musterform
                fgcolor='white',  # Musterfarbe
                size=20,
                solidity=0.05,
                fgopacity=0.4
            )
        )
        ))

        fig.add_trace(go.Bar(
            x=opfer_total['Jahr'],
            y=opfer_total['davon_mehrfach'],
            name='Davon mehrfach Total',
            width=0.8,

            marker=dict(
                color=color_all,  # Hintergrundfarbe
                pattern=dict(
                    shape="x",  # Musterform
                    fgcolor='white',  # Musterfarbe
                    size=20,
                    solidity=0.2,
                    fgopacity=1
                )
            )
        ))




        # Layout anpassen
        fig.update_layout(
            barmode='overlay',
            title='Anzahl Registrierter Straftaten',
            xaxis_title='Jahr',
            yaxis_title='Anzahl Straftaten',
            template='plotly_white',
            bargap=0.5,
            xaxis = dict(
                range=[jahr_start - 0.5, jahr_ende + 0.5],
                tickmode='linear',
                dtick=1  # Jährliche Ticks
            ),
        )

        return fig

    # Grafik Zeitliche Entwilcung Opfer
    @app.callback(
        Output('zeitliche-entwicklung-taeter-opfer', 'figure'),
        [Input('zeitliche-entwicklung-taeter-opfer', 'id'),
         Input('jahr-slider-tab1', 'value')]
    )

    def update_zeitliche_entwicklung(_, jahr_bereich):
        jahr_start, jahr_ende = jahr_bereich

        # Daten nach Zeitraum filtern
        opfer_gefiltert = opfer_total[(opfer_total['Jahr'] >= jahr_start) & (opfer_total['Jahr'] <= jahr_ende)]
        taeter_gefiltert = taeter_total[(taeter_total['Jahr'] >= jahr_start) & (taeter_total['Jahr'] <= jahr_ende)]



        # Visualisierung erstellen
        # Erstelle die Figur
        fig = go.Figure()


        # Linie für gesammt Täter
        fig.add_trace(go.Scatter(
            x=taeter_total['Jahr'],
            y=taeter_total['Anzahl_beschuldigter_Personen_Total'],
            mode='lines+markers',
            name='Beschuldigte gesamt',
            marker=dict(symbol='star-diamond', size=10),
            line=dict(width=1.5, color=color_all)

        ))

        fig.add_trace(go.Scatter(
            x=opfer_total['Jahr'],
            y=opfer_total['Anzahl_geschaedigter_Personen_Total'],
            mode='lines+markers',
            name='Geschädigte gesamt',
            marker=dict(size=9),
            line=dict(width=1.5, color=color_all, dash='dot')

        ))



        # Layout anpassen
        fig.update_layout(
            template='plotly_white',
            hovermode='x unified',
            xaxis=dict(
                range=[jahr_start-0.2, jahr_ende+0.2],
                tickmode='linear',
                dtick=1  # Jährliche Ticks
            ),

            yaxis=dict(range=[0, 12000]),
            legend_title='Geschlecht'
        )

        # Layout anpassen
        fig.update_layout(
            title=f"Zeitliche Entwicklung von Opfern und Tätern ({jahr_start}-{jahr_ende})",
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
