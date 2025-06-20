# === Datei: tab_zeitliche_entwicklung.py ===

# --- Imports ---
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
from dash import ctx  # ctx erkennt, welcher Button ausgelöst wurde

#--- Variabeln ---

# Schrift
import plotly.io as pio
plotly_font = dict(
    family="Arimo, sans-serif",
    size=14,
    color="black"
)
pio.templates["arimo"] = go.layout.Template(layout=dict(font=plotly_font))
pio.templates.default = "arimo"

# --- Farben ---
color_women = "#811616"
color_men = "#0a0a35"
color_all = "black"

# --- Daten laden ---
opfer = pd.read_csv("data/geschaedigte_tidy.csv")
taeter = pd.read_csv("data/beschuldigte_tidy.csv")



# --- Datenaufbereitung: Grafiken  ---

# Nur Gesamtdelikte: "Total Häusliche Gewalt"
taeter = taeter[taeter["Delikt"] == "Total Häusliche Gewalt"]
opfer = opfer[opfer["Delikt"] == "Total Häusliche Gewalt"]

# Filter: nur Beziehungsart "Alle"
taeter = taeter[taeter["Beziehungsart"] == "Alle"]
opfer = opfer[opfer["Beziehungsart"] == "Alle"]

# Aufteilen nach Geschlecht
taeter_maenlich = taeter[taeter["Geschlecht"] == "männlich"]
taeter_weiblich = taeter[taeter["Geschlecht"] == "weiblich"]
taeter_total = taeter[taeter["Geschlecht"] == "Total"]

opfer_maenlich = opfer[opfer["Geschlecht"] == "männlich"]
opfer_weiblich = opfer[opfer["Geschlecht"] == "weiblich"]
opfer_total = opfer[opfer["Geschlecht"] == "Total"]

# --- Layout: Tab "Zeitliche Entwicklung" ---

layout = html.Div([
    html.H2("Wie viele Straftaten und Betroffene werden erfasst – und wie oft erleben diese wiederholte Gewalt?",
            style={'textAlign': 'left', 'marginLeft': 40, 'marginTop': 48,  'fontWeight': 600 }),

    html.P("Entwicklung der Anzahl Straftaten, mehrfach Straftaten und Betroffenen",
           style={'textAlign': 'left', 'marginLeft': 40}),

    # Store zur Speicherung des aktuellen View-Modus
    dcc.Store(id='toggle-view-state', data='straftaten'),

    dbc.Row([
        dbc.Col([
            # Button-Group für Umschalten der View
            dbc.ButtonGroup([
                dbc.Button("Straftaten", id="btn-straftaten", n_clicks=0, className="toggle-btn active"),
                dbc.Button("Betroffene Personen", id="btn-betroffene", n_clicks=0, className="toggle-btn"),
            ], style={"width": "350px", "margin": "20px auto", "marginLeft": "40px"}),

            # Graph: Balken oder Linie, je nach Modus
            dcc.Graph(id='zeitliche-entwicklung-gesamt',
                      style={'height': '65vh','minHeight': '300px', 'overflow': 'visible', 'font-family': 'arimo'})
        ], width=8),

        # Infobereich rechts
        dbc.Col([
            html.Div(id='infotext-block')
        ], width=4, style={'marginTop': 40})
    ]),

    # Quellenangabe unten
    html.Div([
        html.Hr(),
        html.P("Quelle: BFS – Polizeiliche Kriminalstatistik (PKS), Datenstand: 14.02.2025",
               style={'textAlign': 'left', 'marginLeft':40, 'fontStyle': 'italic', 'fontSize': 16, 'color': 'black'}),
        html.P("Für die Richtigkeit, Vollständigkeit und Aktualität der dargestellten Daten übernehmen wir keine Gewähr. "
               "Die Angaben basieren auf den zum genannten Zeitpunkt veröffentlichten Informationen des Bundesamts für Statistik.",
               style={'textAlign': 'left', 'marginLeft': 40, 'fontStyle': 'italic', 'fontSize': 16, 'color': 'black'}),
    ])
])

# --- Callbacks für Tab ---


def register_callbacks(app):
    #viewToggle
    @app.callback(
        Output("btn-straftaten", "className"),
        Output("btn-betroffene", "className"),
        Output("toggle-view-state", "data"),
        Input("btn-straftaten", "n_clicks"),
        Input("btn-betroffene", "n_clicks"),
        prevent_initial_call=True
    )
    def update_toggle_view(n1, n2):
        # Aktive Button-Klasse setzen, je nach Auswahl
        triggered = ctx.triggered_id
        if triggered == "btn-betroffene":
            return "toggle-btn", "toggle-btn active", "betroffene"
        else:
            return "toggle-btn active", "toggle-btn", "straftaten"
    #Text und Grafik anzeigen
    @app.callback(
        Output("zeitliche-entwicklung-gesamt", "figure"),
        Output("infotext-block", "children"),
        Input("toggle-view-state", "data")
    )

    def update_grafik_und_text(view_mode):
        if view_mode == "straftaten":
            # --- Diagramm: Straftaten (Balken) ---
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=opfer_total['Jahr'],
                y=opfer_total['Straftaten_Total'],
                name='Straftaten Total',
                marker=dict(color='grey'),
                hovertemplate = "%{y:.0f}<br>Straftaten (%{x})<extra></extra>"
            ))
            fig.add_trace(go.Bar(
                x=opfer_total['Jahr'],
                y=opfer_total['davon_mehrfach'],
                name='Davon mehrfach',
                marker=dict(color=color_all),
                hovertemplate="%{y:.0f}<br>Davon mehrfach (%{x})<extra></extra>"
            ))
            fig.update_layout(
                barmode='overlay',
                template='plotly_white',
                title=dict(
                    text="Anzahl registrierte Straftaten Häuslicher Gewalt 2009–2024",
                    x=0.03,
                    xanchor="left"
                ),
                title_font_family="Arimo, sans-serif",
                title_font_size=20,
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
                    zeroline=False,
                    tickformat = "'d"
                ),
                legend=dict(
                    orientation="v",
                    yanchor="bottom",
                    y=0.85,
                    xanchor="left",
                    x=0.018,

                ),
                hoverlabel=dict(
                    bgcolor="white",
                    bordercolor="black",
                    font=dict(color="black", size=14, family="Arimo, sans-serif"),
                    align='left',
                    namelength=-1
                ),

            )

            # --- Textblock: Zusatzinfos Straftaten ---
            text = html.Div([
                html.H4(["Was ist Häusliche Gewalt ", html.Br(), "und wie viele Straftaten gibt es?"]),
                html.P("Unter Häuslicher Gewalt versteht man körperliche, psychische oder sexuelle Gewalt "
                       "innerhalb einer Familie oder Beziehung."),
                dbc.Row([
                    dbc.Col([html.H1("21'127"), html.P("Straftaten Häusliche Gewalt 2024")]),
                    dbc.Col([html.H1("5695"), html.P("Davon mehrfach 2024")])
                ]),
                html.P([
                    "Der ", html.B("Strafbestand wird mit Mehrfach gekennzeichnet"),
                    ", wenn die gleiche Person derselben Täterschaft zu mehreren Zeitpunkten auf die gleiche Art wiederholt geschädigt wird."
                ]),
            ], style={'marginTop': 95, 'marginRight': 40})

        else:
            # --- Diagramm: Betroffene (Linie) ---
            opfer_gefiltert = opfer_total[(opfer_total['Jahr'] >= 2009) & (opfer_total['Jahr'] <= 2024)]
            taeter_gefiltert = taeter_total[(taeter_total['Jahr'] >= 2009) & (taeter_total['Jahr'] <= 2024)]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=opfer_gefiltert['Jahr'],
                y=opfer_gefiltert['Anzahl_geschaedigter_Personen_Total'],
                mode='lines+markers',
                name='Opfer gesamt',
                marker=dict(size=9),
                line=dict(width=1.5, color=color_all, dash='dot')
            ))
            fig.add_trace(go.Scatter(
                x=taeter_gefiltert['Jahr'],
                y=taeter_gefiltert['Anzahl_beschuldigter_Personen_Total'],
                mode='lines+markers',
                name='Täter:innen gesamt',
                marker=dict(symbol='star-diamond', size=10),
                line=dict(width=1.5, color=color_all)
            ))
            fig.update_layout(
                template='plotly_white',
                hovermode='x unified',
                hoverlabel=dict(
                    bgcolor="white",
                    bordercolor="black",
                    font=dict(color="black", size=14, family="Arimo, sans-serif"),
                    align='left',
                    namelength=-1
                ),
                title=dict(
                    text="Anzahl betroffene Personen Häuslicher Gewalt 2009–2024",
                    x=0.03,
                    xanchor="left"
                ),
                title_font_family="Arimo, sans-serif",
                title_font_size=20,
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
                    title="",
                    tickformat = "'d"
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

            # --- Textblock: Zusatzinfos Betroffene ---
            text = html.Div([
                html.H4("Wie viele Personen sind betroffen?"),
                dbc.Row([
                    dbc.Col([html.H1("11'041"), html.P("Täter:innen im Jahr 2024")]),
                    dbc.Col([html.H1("11'849"), html.P("Opfer im Jahr 2024")])
                ]),
                html.P([
                    html.B("Die Dunkelziffer bei häuslicher Gewalt wird als sehr hoch eingeschätzt."),
                    " Laut einer Untersuchung der Universität St. Gallen werden beispielsweise nur 28,9 % der Tätlichkeiten und Körperverletzungen und lediglich 10,5 % der sexuellen Gewaltdelikte angezeigt ",
                    html.A(
                        "(Quelle: Universität St. Gallen, 2023, zuletzt abgerufen: 09.06.2025 )",
                        href="https://www.unisg.ch/de/newsdetail/news/hsg-strafrechtlerin-leuchtet-die-dunkelziffer-der-haeuslichen-gewalt-aus/",
                        target="_blank",
                        style={"marginLeft": "4px", "color": "black", "textDecoration": "none"}
                    )
                ])
            ], style={'marginTop': 95, 'marginRight': 40})

        return fig, text
