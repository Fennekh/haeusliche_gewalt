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
    html.H3("Impressum & Projektdokumentation", style={'marginTop': 20, 'marginBottom': 10}),

    html.H4("Projektbeschreibung"),
    html.P("Ein interaktives Dashboard zur Visualisierung und Analyse von registrierten Straftaten im Bereich häuslicher Gewalt in der Schweiz, basierend auf Daten von 2009 bis 2024."),

    html.H4("Ziel des Dashboards"),
    html.P("Das Dashboard richtet sich an Fachpersonen aus Statistik, Prävention, Medien und Politik, um Trends, Geschlechterunterschiede und wiederholte Tatmuster schnell erfassbar zu machen."),

    html.H4("Datenquelle"),
    html.Ul([
        html.Li("Polizeiliche Kriminalstatistik Schweiz (BFS), 2009–2024"),
        html.Li("Verwendete Formate: CSV-Dateien (statisch)"),
        html.Li("Datenbasis: öffentlich zugänglich über bfs.admin.ch")
    ]),

    html.H4("Spaltenbeschreibung"),
    dash_table.DataTable(
        columns=[
            {"name": "Spalte", "id": "Spalte"},
            {"name": "Beschreibung", "id": "Beschreibung"}
        ],
        data=[
            {"Spalte": "Jahr", "Beschreibung": "Kalenderjahr der Erhebung"},
            {"Spalte": "Delikt", "Beschreibung": "Kategorie des Delikts (z. B. Körperverletzung)"},
            {"Spalte": "Beziehungsart", "Beschreibung": "Art der Beziehung zwischen Täter:in und Opfer"},
            {"Spalte": "Geschlecht", "Beschreibung": "Geschlecht der betroffenen Person"},
            {"Spalte": "Straftaten_Total", "Beschreibung": "Gesamtzahl registrierter Straftaten"},
            {"Spalte": "davon_mehrfach", "Beschreibung": "Wiederholte Fälle derselben betroffenen Person"}
        ],
        style_table={'marginBottom': '20px'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
        style_header={'fontWeight': 'bold', 'backgroundColor': '#f5f5f5'}
    ),

    html.H4("Technische Umsetzung"),
    html.Ul([
        html.Li("Python mit Dash und Plotly für interaktive Visualisierungen"),
        html.Li("Dash Bootstrap Components für responsives Layout"),
        html.Li("Statisches CSV-Datenmodell ohne Backend-Anbindung")
    ]),

    html.H4("Interaktionsmöglichkeiten"),
    html.Ul([
        html.Li("Hover-Tooltips in Diagrammen mit Detailwerten"),
        html.Li("Tabs zur Navigation durch unterschiedliche Analysebereiche"),
        html.Li("Dynamische Diagrammaktualisierung bei Filteranpassungen (z. B. nach Geschlecht)")
    ]),

    html.H4("Limitationen"),
    html.Ul([
        html.Li("Keine Prognosen oder Machine Learning-Analysen enthalten"),
        html.Li("Keine Daten auf Kantons-/Gemeindeebene"),
        html.Li("Statische Daten ohne automatische Aktualisierung"),
    ]),

    html.H4("Verbesserungsideen"),
    html.Ul([
        html.Li("Erweiterung um Deliktartenvergleich oder kantonale Ebene"),
        html.Li("Integration von Prognosefunktionen (z. B. mit Prophet oder PyCaret)"),
        html.Li("Datenaktualisierung per API oder automatisierter ETL-Prozess")
    ]),

    html.Hr(),
    html.P("Dieses Dashboard wurde im Rahmen eines Data-Science-Projekts entwickelt. Alle Daten basieren auf öffentlich zugänglichen Quellen und dienen der Veranschaulichung gesellschaftlich relevanter Themen.",
           style={'fontStyle': 'italic', 'fontSize': 12, 'color': '#888', 'textAlign': 'center'})
])



def register_callbacks(app):
    @app.callback(
        Output('impressum', 'figure'),
        Input('impressum', 'id')
    )
    def update_impressum(_):
        fig = go.Figure()
        return fig



