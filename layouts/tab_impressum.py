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

#------ Variabeln überall gleich

#Variabeln
color_women = "#811616"
color_men = "#0a0a35"
color_all = "black"

# Roboto-Template definieren (bei allen seiten machen?)
pio.templates["roboto"] = go.layout.Template(
    layout=dict(
        font=dict(
            family="roboto",
            size=14,
            color="black"
        )
    )
)

# Roboto als Standard setzen
pio.templates.default = "roboto"
#------



#----

# Layout für den ersten Tab (Zeitliche Entwicklung)
layout = html.Div([
    html.H3("Wie verändert sich die Anzahl Straftaten und Betroffene in Häuslicher Gewalt?",
            style={'textAlign': 'left', 'marginTop': 20, 'marginLeft': 20,'paddingBottom': 0}),
    # Haupt-Grafik + Zusammenfassung
    dbc.Row([
        dbc.Col([
            html.H4("Was ist Häusliche Gewalt?"),
            html.P(
                "Unter Häuslicher Gewalt versteht man körperliche, psychische oder sexuelle Gewalt innerhalb einer Familie oder in einer aktuellen oder aufgelösten Paarbeziehung."),
            html.P([
                "Der ", html.B("Strafbestand wir mit Mehrfach gekennzeichnet"),
                " wenn die gleiche Person derselben Täterschaft zu mehreren Zeitpunkten auf die gleiche Art wiederholt geschädigt wird, ohne dass eine separate Anzeige bzw. ein separater Rapport erfolgt",

                " gekennzeichnet."
            ]),
            html.H1("21'127", style={'marginTop': 10}),
            html.P("Straftaten Häusliche Gewalt 2024")
        ], width=4, style={'marginTop': 40}),

        dbc.Col([
            html.H4("Was ist Häusliche Gewalt?"),
            html.P("Unter Häuslicher Gewalt versteht man körperliche, psychische oder sexuelle Gewalt innerhalb einer Familie oder in einer aktuellen oder aufgelösten Paarbeziehung."),
            html.P([
                "Der ", html.B("Strafbestand wir mit Mehrfach gekennzeichnet"),
                " wenn die gleiche Person derselben Täterschaft zu mehreren Zeitpunkten auf die gleiche Art wiederholt geschädigt wird, ohne dass eine separate Anzeige bzw. ein separater Rapport erfolgt",

                " gekennzeichnet."
            ]),
            html.H1("21'127", style={'marginTop': 10}),
            html.P("Straftaten Häusliche Gewalt 2024")
        ], width=4, style={'marginTop': 40}),
    ]),

    # Tabelle + weitere Visualisierungen
    dbc.Row([

        dbc.Col([
            html.H4("Wie viele Personen sind betroffen?"),
            dbc.Row([
                dbc.Col([
                    html.H2("11'041"),
                    html.P("Täter:innen im Jahr 2024")
                ]),
                dbc.Col([
                    html.H2("11'849"),
                    html.P("Opfer im Jahr 2024")
                ])
            ]),

            html.P([html.B(" Die Dunkelziffer bei Häuslicher Gewalt wird sehr hoch geschätzt."),
                    " Bei Tätlichkeiten und Körperverletzungen werden beispielsweise 28,9 Prozent, bei sexueller Gewalt 10,5 Prozent der Fälle angezeigt (Uni St.Gallen 2023)."]),

        ], width=4, style={'marginTop': 40}),

        dbc.Col([
            html.H4("Wie viele Personen sind betroffen?"),
            dbc.Row([
                dbc.Col([
                    html.H2("11'041"),
                    html.P("Täter:innen im Jahr 2024")
                ]),
                dbc.Col([
                    html.H2("11'849"),
                    html.P("Opfer im Jahr 2024")
                ])
            ]),

html.P([html.B(" Die Dunkelziffer bei Häuslicher Gewalt wird sehr hoch geschätzt."),
        " Bei Tätlichkeiten und Körperverletzungen werden beispielsweise 28,9 Prozent, bei sexueller Gewalt 10,5 Prozent der Fälle angezeigt (Uni St.Gallen 2023)."]),

        ],  width=4, style={'marginTop': 40}),
    ]),



    # Fußnote
    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009–2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])


def register_callbacks(app):
    @app.callback(
        Output('impressum', 'figure'),
        Input('impressum', 'id')
    )
    def update_impressum(_):
        fig = go.Figure()
        return fig



