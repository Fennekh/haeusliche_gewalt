from dash import html, dcc
import dash_bootstrap_components as dbc
from components import text_box_detail, bar_beziehungen, spider_taeter

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            text_box_detail.component,
            bar_beziehungen.component
        ], width=3),

        dbc.Col([
            dbc.Row([
                dbc.Col(spider_taeter.fig, width=6),
                #dbc.Col(spider_opfer.component, width=6)
            ])
        ], width=9)
    ])
], fluid=True)