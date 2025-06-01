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





#----

# Layout für den ersten Tab (Zeitliche Entwicklung)
layout = html.Div([
    html.H3("Wie verändert sich die Anzahl Straftaten und Betroffene in Häuslicher Gewalt?",
            style={'textAlign': 'left', 'marginTop': 20, 'marginLeft': 20, 'paddingBottom': 0}),

    dcc.Store(id='toggle-view-state', data='straftaten'),

    dbc.Row([
        dbc.Col([
            # Toggle-Button
            dbc.ButtonGroup([
                dbc.Button("Straftaten", id="btn-straftaten", n_clicks=0, className="toggle-btn active"),
                dbc.Button("Betroffene Personen", id="btn-betroffene", n_clicks=0, className="toggle-btn"),
            ], style={"width": "350px", "margin": "20px auto", "gap": "10px", "marginLeft": "20px"}),

            # Grafik
            dcc.Graph(id='zeitliche-entwicklung-gesamt', style={'height': '65vh', 'minHeight': '300px'})
        ], width=8),

        dbc.Col([
            html.Div(id='infotext-block')
        ], width=4, style={'marginTop': 40})
    ]),

    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009–2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])


# Hier registrieren wir die Callbacks für diesen Tab
from dash import ctx

def register_callbacks(app):
    @app.callback(
        Output("btn-straftaten", "className"),
        Output("btn-betroffene", "className"),
        Output("toggle-view-state", "data"),
        Input("btn-straftaten", "n_clicks"),
        Input("btn-betroffene", "n_clicks"),
        prevent_initial_call=True
    )
    def update_toggle_view(n1, n2):
        triggered = ctx.triggered_id
        if triggered == "btn-betroffene":
            return "toggle-btn", "toggle-btn active", "betroffene"
        else:
            return "toggle-btn active", "toggle-btn", "straftaten"

    @app.callback(
        Output("zeitliche-entwicklung-gesamt", "figure"),
        Output("infotext-block", "children"),
        Input("toggle-view-state", "data")
    )
    def update_grafik_und_text(view_mode):
        if view_mode == "straftaten":
            # Bar-Chart Ansicht
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=opfer_total['Jahr'],
                y=opfer_total['Straftaten_Total'],
                name='Straftaten Total',
                marker=dict(color='#6E6E6E')
            ))
            fig.add_trace(go.Bar(
                x=opfer_total['Jahr'],
                y=opfer_total['davon_mehrfach'],
                name='Davon mehrfach',
                marker=dict(color=color_all)
            ))
            fig.update_layout(
                barmode='overlay',
                template='plotly_white',
                title="Anzahl registrierte Straftaten Häuslicher Gewalt 2009–2024",
                xaxis=dict(
                    range=[2009 - 0.5, 2024 + 0.5],
                    tickmode='linear',
                    dtick=1,
                    linecolor='black',
                    linewidth=1,
                    showline=True,
                    showgrid=False
                ),
                yaxis=dict(
                    range=[0,20000],
                    gridcolor='#e5e5e5',
                    zeroline=False
                ),
                legend=dict(
                    orientation="v",
                    yanchor="bottom",
                    y=0.85,
                    xanchor="left",
                    x=0.018
                )
            )

            text = html.Div([
                html.H4("Was ist Häusliche Gewalt?"),
                html.P("Unter Häuslicher Gewalt versteht man körperliche, psychische oder sexuelle Gewalt "
                       "innerhalb einer Familie oder Beziehung."),
                html.P([
                    "Der ", html.B("Strafbestand wird mit Mehrfach gekennzeichnet"),
                    ", wenn die gleiche Person derselben Täterschaft zu mehreren Zeitpunkten auf die gleiche Art wiederholt geschädigt wird."
                ]),
                html.H1("21'127", style={'marginTop': 10}),
                html.P("Straftaten Häusliche Gewalt 2024")
            ])
        else:
            # Linien-Ansicht Betroffene – mit Styling aus Originalversion
            opfer_gefiltert = opfer_total[(opfer_total['Jahr'] >= 2009) & (opfer_total['Jahr'] <= 2024)]
            taeter_gefiltert = taeter_total[(taeter_total['Jahr'] >= 2009) & (taeter_total['Jahr'] <= 2024)]

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=opfer_gefiltert['Jahr'],
                y=opfer_gefiltert['Anzahl_geschaedigter_Personen_Total'],
                mode='lines+markers',
                name='Geschädigte gesamt',
                marker=dict(size=9),
                line=dict(width=1.5, color=color_all, dash='dot')
            ))

            fig.add_trace(go.Scatter(
                x=taeter_gefiltert['Jahr'],
                y=taeter_gefiltert['Anzahl_beschuldigter_Personen_Total'],
                mode='lines+markers',
                name='Beschuldigte gesamt',
                marker=dict(symbol='star-diamond', size=10),
                line=dict(width=1.5, color=color_all)
            ))

            fig.update_layout(
                template='plotly_white',
                hovermode='x unified',
                title="Anzahl betroffene Personen Häuslicher Gewalt 2009–2024",
                xaxis=dict(
                    range=[2009 - 0.2, 2024 + 0.2],
                    tickmode='linear',
                    dtick=1,
                    showgrid=False,
                    linecolor='black',
                    linewidth=1,
                    showline=True,
                    gridcolor='#e5e5e5'
                ),
                yaxis=dict(
                    range=[0, 20000],
                    title=""
                ),
                legend_title='',
                legend=dict(
                    orientation="v",
                    yanchor="bottom",
                    y=0.85,
                    xanchor="left",
                    x=0.018
                )
            )

            # Richtiger Platz für den Text zur Betroffenen-Ansicht
            text = html.Div([
                html.H4("Wie viele Personen sind betroffen?"),
                dbc.Row([
                    dbc.Col([html.H2("11'041"), html.P("Täter:innen im Jahr 2024")]),
                    dbc.Col([html.H2("11'849"), html.P("Opfer im Jahr 2024")])
                ]),
                html.P([
                    html.B("Die Dunkelziffer bei Häuslicher Gewalt wird sehr hoch geschätzt."),
                    " Bei Tätlichkeiten und Körperverletzungen werden z. B. 28,9 %, bei sexueller Gewalt 10,5 % der Fälle angezeigt (Uni St.Gallen 2023)."
                ])
            ])

        return fig, text



