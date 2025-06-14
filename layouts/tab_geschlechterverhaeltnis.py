# === Datei 1: tab_geschlechterverhaeltnis.py ===

# --- Imports ---
import dash
from dash import dcc, html, ctx  # ctx wird verwendet, um den auslösenden Button zu erkennen
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio

# --- Plotly-Schriftart definieren ---
plotly_font = dict(
    family="Arimo, sans-serif",
    size=14,
    color="black"
)
pio.templates["arimo"] = go.layout.Template(layout=dict(font=plotly_font))
pio.templates.default = "arimo"

# --- Farben und Klassen ---
dark_border_class = "toggle-btn active"  # CSS-Klasse für aktiven Button
default_class = "toggle-btn"  # CSS-Klasse für inaktiven Button
color_women = "#cb4d1d"
color_men = "#4992b2"
color_all = "black"

# Optional: Roboto als alternative Schrift
pio.templates["roboto"] = go.layout.Template(layout=dict(font=dict(family="roboto", size=14, color="black")))
pio.templates.default = "roboto"

# --- Daten laden ---
opfer = pd.read_csv("data/geschaedigte_tidy.csv")
taeter = pd.read_csv("data/beschuldigte_tidy.csv")

# Nur relevante Daten auswählen (häusliche Gewalt, Beziehungsart = Alle)
opfer = opfer[(opfer["Delikt"] == "Total Häusliche Gewalt") & (opfer["Beziehungsart"] == "Alle")]
taeter = taeter[(taeter["Delikt"] == "Total Häusliche Gewalt") & (taeter["Beziehungsart"] == "Alle")]

# Nach Geschlecht aufteilen für spätere Auswertungen
opfer_maenlich = opfer[opfer["Geschlecht"] == "männlich"]
opfer_weiblich = opfer[opfer["Geschlecht"] == "weiblich"]
opfer_total = opfer[opfer["Geschlecht"] == "Total"]

taeter_maenlich = taeter[taeter["Geschlecht"] == "männlich"]
taeter_weiblich = taeter[taeter["Geschlecht"] == "weiblich"]
taeter_total = taeter[taeter["Geschlecht"] == "Total"]

# --- Layout der Seite ---
layout = html.Div([
    html.H2("Wie hat sich das Geschlechterverhältnis verändert?",
            style={'textAlign': 'left', 'marginLeft': 40, 'marginTop': 48,  'fontWeight': 600 }),

    html.P("Entwicklung des Geschlechterverhältnis in absoluten und relativen Zahlen",
           style={'textAlign': 'left', 'marginLeft': 40}),

    # Speichert den Button-Zustand ("percent" oder "absolute")
    dcc.Store(id='button-state', data='percent'),

    # Umschalt-Buttons für Darstellungstyp
    html.Div([
        dbc.ButtonGroup([
            dbc.Button("Prozentuale Verteilung", id="btn-set1", n_clicks=0, className=dark_border_class),
            dbc.Button("Absolute Zahlen", id="btn-set2", n_clicks=0, className=default_class),
        ], size="md", className="mb-4",
           style={"width": "350px", "margin": "40px auto", "marginLeft": "40px", 'marginTop': '20px'})
    ]),

    # Zwei nebeneinanderstehende Diagramme
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-taeter', style={'height': '65vh', 'minHeight': '300px'}), width=6),
        dbc.Col(dcc.Graph(id='graph-opfer', style={'height': '65vh', 'minHeight': '300px'}), width=6),
    ]),

    # Quellenangabe
    html.Div([
        html.Hr(),
        html.P("Quelle: BFS – Polizeiliche Kriminalstatistik (PKS), Datenstand: 14.02.2025",
               style={'textAlign': 'left', 'marginLeft': 40, 'fontStyle': 'italic', 'fontSize': 16, 'color': 'black'}),
        html.P("Für die Richtigkeit, Vollständigkeit und Aktualität der dargestellten Daten übernehmen wir keine Gewähr. "
               "Die Angaben basieren auf den zum genannten Zeitpunkt veröffentlichten Informationen des Bundesamts für Statistik.",
               style={'textAlign': 'left', 'marginLeft': 40, 'fontStyle': 'italic', 'fontSize': 16, 'color': 'black'}),
    ])
])

# --- Callbacks registrieren ---
def register_callbacks(app):

    # --- Prozentuale Darstellung der Täter:innen nach Geschlecht ---
    def update_taeter_graph():
        # Daten aggregieren und prozentual berechnen
        m = taeter_maenlich.groupby('Jahr')['Anzahl_beschuldigter_Personen_Total'].sum()
        w = taeter_weiblich.groupby('Jahr')['Anzahl_beschuldigter_Personen_Total'].sum()
        t = taeter_total.groupby('Jahr')['Anzahl_beschuldigter_Personen_Total'].sum()
        df = pd.DataFrame({'männlich': m, 'weiblich': w, 'total': t}).reset_index()
        df['% männlich'] = df['männlich'] / df['total'] * 100
        df['% weiblich'] = df['weiblich'] / df['total'] * 100

        # Gestapeltes Balkendiagramm
        fig = go.Figure()
        fig.add_bar(x=df['Jahr'], y=df['% männlich'], name='Männliche Täter', marker_color=color_men,
                    hovertemplate='%{y:.1f}%<br>Täter<br>%{x}<extra></extra>')
        fig.add_bar(x=df['Jahr'], y=df['% weiblich'], name='Weibliche Täter', marker_color=color_women,
                    hovertemplate='%{y:.1f}%<br>Täterinnen<br>%{x}<extra></extra>')

        fig.update_layout(
            barmode='stack',
            title='Täter:innen nach Geschlecht (2009–2024, Anteile in %)',
            yaxis_title="",
            showlegend=False,
            template="plotly_white",
            bargap=0.1,
            title_font_family="Arimo, sans-serif",
            title_font_size=20,
        )
        return fig

    # --- Absolute Zahlen der Täter:innen als Linienchart ---
    def update_entwicklung_taeter():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=taeter_maenlich['Jahr'], y=taeter_maenlich['Anzahl_beschuldigter_Personen_Total'],
                                 mode='lines+markers', name='Täter männlich', line=dict(width=1.5, color=color_men)))
        fig.add_trace(go.Scatter(x=taeter_weiblich['Jahr'], y=taeter_weiblich['Anzahl_beschuldigter_Personen_Total'],
                                 mode='lines+markers', name='Täter weiblich', line=dict(width=1.5, color=color_women)))
        fig.add_trace(go.Scatter(x=taeter_total['Jahr'], y=taeter_total['Anzahl_beschuldigter_Personen_Total'],
                                 mode='lines+markers', name='Gesamt', line=dict(width=1.5, color=color_all),
                                 opacity=0.1, showlegend=False))

        fig.update_layout(
            title="Täter:innen nach Geschlecht (2009–2024, Anzahl Personen)",
            xaxis_title="Jahr",
            yaxis_title="",
            template="plotly_white",
            hovermode="x unified",
            yaxis=dict(range=[0, 12000]),
            showlegend=False,
            title_font_family="Arimo, sans-serif",
            title_font_size=20,
        )
        return fig

    # --- Prozentuale Darstellung der Opfer nach Geschlecht ---
    def update_opfer_graph():
        m = opfer_maenlich.groupby('Jahr')['Anzahl_geschaedigter_Personen_Total'].sum()
        w = opfer_weiblich.groupby('Jahr')['Anzahl_geschaedigter_Personen_Total'].sum()
        t = m + w
        df = pd.DataFrame({'männlich': m, 'weiblich': w, 'total': t}).reset_index()
        df['% männlich'] = df['männlich'] / df['total'] * 100
        df['% weiblich'] = df['weiblich'] / df['total'] * 100

        fig = go.Figure()
        fig.add_bar(x=df['Jahr'], y=df['% männlich'], name='Männlich', marker_color=color_men,
                    hovertemplate='%{y:.1f}%<br>Männliche Opfer<br>%{x}<extra></extra>')
        fig.add_bar(x=df['Jahr'], y=df['% weiblich'], name='Weiblich', marker_color=color_women,
                    hovertemplate='%{y:.1f}%<br>Weibliche Opfer<br>%{x}<extra></extra>')

        fig.update_layout(
            barmode='stack',
            title='Opfer nach Geschlecht (2009–2024, Anteile in %)',
            template="plotly_white",
            bargap=0.1,
            showlegend=True,
            title_font_family="Arimo, sans-serif",
            title_font_size=20,
            legend=dict(
                title="",
                x=0.98,
                y=1.1,
                xanchor='right',
                yanchor='top',
                bgcolor='rgba(255,255,255,0.5)',
                bordercolor='lightgrey',
                borderwidth=1,
                font=dict(color='black', family='Arimo'),
            )
        )
        return fig

    # --- Absolute Zahlen der Opfer als Linienchart ---
    def update_entwicklung_opfer():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=opfer_weiblich['Jahr'], y=opfer_weiblich['Anzahl_geschaedigter_Personen_Total'],
                                 mode='lines+markers', name='Weiblich', line=dict(width=1.5, color=color_women)))
        fig.add_trace(go.Scatter(x=opfer_maenlich['Jahr'], y=opfer_maenlich['Anzahl_geschaedigter_Personen_Total'],
                                 mode='lines+markers', name='Männlich', line=dict(width=1.5, color=color_men)))
        fig.add_trace(go.Scatter(x=opfer_total['Jahr'], y=opfer_total['Anzahl_geschaedigter_Personen_Total'],
                                 mode='lines+markers', name='Gesamt', line=dict(width=1.5, color=color_all), opacity=0.1))

        fig.update_layout(
            title="Opfer nach Geschlecht (2009–2024, Anzahl Personen)",
            xaxis_title="Jahr",
            yaxis_title="Anzahl Personen",
            title_font_family="Arimo, sans-serif",
            title_font_size=20,
            template="plotly_white",
            hovermode="x unified",
            showlegend=True,
            legend=dict(
                title="",
                x=0.98,
                y=1.19,
                xanchor='right',
                yanchor='top',
                bgcolor='rgba(255,255,255,0.5)',
                bordercolor='lightgrey',
                borderwidth=1,
                font=dict(color='black', family='Arimo', size=12),
            ),
            yaxis=dict(range=[0, 12000]),
            font=dict(family="Arimo, sans-serif", size=14, color="black")
        )
        return fig

    # --- Callback zur Button-Auswahl (absolute vs. Prozent) ---
    @app.callback(
        Output("btn-set1", "className"),
        Output("btn-set2", "className"),
        Output("button-state", "data"),
        Input("btn-set1", "n_clicks"),
        Input("btn-set2", "n_clicks"),
        prevent_initial_call=True
    )
    def update_buttons(n1, n2):
        if ctx.triggered_id == "btn-set2":
            # Absolute Zahlen anzeigen
            return default_class, dark_border_class, "absolute"
        else:
            # Prozentuale Darstellung anzeigen
            return dark_border_class, default_class, "percent"

    # --- Callback zum Rendern der Diagramme basierend auf Button-Zustand ---
    @app.callback(
        Output('graph-taeter', 'figure'),
        Output('graph-opfer', 'figure'),
        Input('button-state', 'data')
    )
    def update_graphs(mode):
        if mode == "absolute":
            return update_entwicklung_taeter(), update_entwicklung_opfer()
        else:
            return update_taeter_graph(), update_opfer_graph()
