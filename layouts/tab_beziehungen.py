# === Datei: tab_beziehungen.py ===

# --- Imports ---
import dash
from dash import dcc, html  # Dash Core Components & HTML-Elemente
import dash_bootstrap_components as dbc  # Für hübsche Layout-Komponenten
from dash.dependencies import Input, Output  # Für Callback-Funktionen
import plotly.graph_objects as go  # Für interaktive Diagramme
import pandas as pd  # Für Datenmanipulation
import plotly.io as pio  # Für Theme-Konfiguration

# --- Design- und Darstellungs-Variablen ---

# Schrift
plotly_font = dict(
    family="Arimo, sans-serif",
    size=14,
    color="black"
)
pio.templates["arimo"] = go.layout.Template(layout=dict(font=plotly_font))
pio.templates.default = "arimo"

# Farbdefinitionen für Geschlechter
color_women = "#cb4d1d"
color_men = "#4992b2"

# --- Daten einlesen und filtern ---

# Grunddaten zu Opfern und Tätern laden
opfer = pd.read_csv("data/geschaedigte_tidy.csv")
taeter = pd.read_csv("data/beschuldigte_tidy.csv")

# Nur Daten zur "häuslichen Gewalt – Total" mit Beziehungsart "Alle" behalten
opfer = opfer[(opfer["Delikt"] == "Total Häusliche Gewalt") & (opfer["Beziehungsart"] == "Alle")]
taeter = taeter[(taeter["Delikt"] == "Total Häusliche Gewalt") & (taeter["Beziehungsart"] == "Alle")]

# --- Daten für Beziehungsarten vorbereiten ---

# Daten nochmal neu laden für genauere Analyse nach Beziehungsart
df = pd.read_csv("data/geschaedigte_tidy.csv")
df_be = pd.read_csv("data/beschuldigte_tidy.csv")

# Leerzeichen in Beziehungsart-Spalten entfernen
df["Beziehungsart"] = df["Beziehungsart"].str.strip()
df_be["Beziehungsart"] = df_be["Beziehungsart"].str.strip()

# Nur relevante Beziehungsarten betrachten
relevante_beziehungen = [
    "Partnerschaft",
    "ehemalige Partnerschaft",
    "Eltern-Kind-Beziehung",
    "andere Verwandtschaftsbeziehung"
]

# Filter für Opferdaten
df = df[
    (df["Delikt"] == "Total Häusliche Gewalt") &
    (df["Beziehungsart"].isin(relevante_beziehungen)) &
    (df["Geschlecht"].isin(["männlich", "weiblich"]))
]

# Nur benötigte Spalten behalten und Datentypen anpassen
df = df[["Jahr", "Geschlecht", "Beziehungsart", "Anzahl_geschaedigter_Personen_Total"]].dropna()
df["Anzahl_geschaedigter_Personen_Total"] = df["Anzahl_geschaedigter_Personen_Total"].astype(float)
df["Jahr"] = df["Jahr"].astype(int)

# Gleiches Vorgehen für Täterdaten
df_be = df_be[
    (df_be["Delikt"] == "Total Häusliche Gewalt") &
    (df_be["Beziehungsart"].isin(relevante_beziehungen)) &
    (df_be["Geschlecht"].isin(["männlich", "weiblich"]))
]
df_be = df_be[["Jahr", "Geschlecht", "Beziehungsart", "Anzahl_beschuldigter_Personen_Total"]].dropna()
df_be["Anzahl_beschuldigter_Personen_Total"] = df_be["Anzahl_beschuldigter_Personen_Total"].astype(float)
df_be["Jahr"] = df_be["Jahr"].astype(int)

# --- Layout ---
layout = html.Div([
    html.Div([
        html.H2([
            "In welcher Beziehung stehen Täter:innen und Opfer zueinander?",
            html.Span(" ℹ️", id="info-icon", style={"cursor": "pointer", "marginLeft": "10px"})
        ], style={
            'textAlign': 'left',
            'marginLeft': 40,
            'marginTop': 48,
            'fontWeight': 600
        }),

        # Tooltip neben Titel
        dbc.Tooltip(
            "Die Zahlen bei Täter:innen und Opfern können sich unterscheiden, da Täter:innen mehrere Opfer haben können und umgekehrt. "
            "Wird eine Person beispielsweise von der Mutter und dem Bruder bedroht, so zählt dies je einmal in den Kategorien Eltern-Kind-Beziehung "
            "und andere Verwandtschaftsbeziehung.",
            target="info-icon",
            placement="right",
            style={'textAlign': 'left'}
        ),
    ]),

    html.P(
        "Beziehung von Täter:innen und Opfer zueinander und ihre Häufigkeit",
        style={'textAlign': 'left', 'marginLeft': 40}
    ),

    # Dropdown für Jahresauswahl
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='jahr-dropdown',
                options=[{"label": str(j), "value": j} for j in sorted(df["Jahr"].unique())],
                value=2024,
                clearable=False,
                style={"width": "150px"}
            ), width="auto", style={"marginTop": "20px"})
        ], style={"marginLeft": "30px"})
    ]),

    # Zwei Diagramme (Täter:innen / Opfer)
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-beziehung-taeter', style={
            'height': '65vh',
            'minHeight': '300px',
            'textAlign': 'left',
        }), width=6),
        dbc.Col(dcc.Graph(id='graph-beziehung-opfer', style={
            'height': '65vh',
            'minHeight': '300px',
            'textAlign': 'left',
            'font_family': 'arimo',
        }), width=6),
    ]),

    # Fußzeile
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

    # Callback: Bar Chart für Opfer nach Beziehungsart und Geschlecht
    @app.callback(
        Output('graph-beziehung-opfer', 'figure'),
        Input('jahr-dropdown', 'value')
    )
    def update_beziehung_opfer(selected_year):
        # Filtere Daten nach ausgewähltem Jahr
        df_year = df[df["Jahr"] == selected_year]

        # Gruppieren nach Beziehungsart und Geschlecht
        grouped = df_year.groupby(['Beziehungsart', 'Geschlecht'])[
            'Anzahl_geschaedigter_Personen_Total'].sum().reset_index()

        # Achsentitel und Diagrammtitel definieren
        title_text = f'Opfer nach Beziehungsart zur Täterschaft ({selected_year}, absolute Zahlen)'

        # Sortiere Beziehungsarten in vordefinierter Reihenfolge
        grouped['Beziehungsart'] = pd.Categorical(grouped['Beziehungsart'], categories=relevante_beziehungen, ordered=True)
        grouped = grouped.sort_values('Beziehungsart')

        fig = go.Figure()

        # Balken für weibliche Opfer
        weiblich = grouped[grouped["Geschlecht"] == "weiblich"]
        fig.add_trace(go.Bar(
            x=weiblich["Beziehungsart"],
            y=weiblich["Anzahl_geschaedigter_Personen_Total"],
            name='Weiblich',
            marker_color=color_women
        ))

        # Balken für männliche Opfer
        maennlich = grouped[grouped["Geschlecht"] == "männlich"]
        fig.add_trace(go.Bar(
            x=maennlich["Beziehungsart"],
            y=maennlich["Anzahl_geschaedigter_Personen_Total"],
            name='Männlich',
            marker_color=color_men
        ))

        # Layout anpassen
        fig.update_layout(
            barmode='group',
            xaxis_title='Beziehungsart',
            yaxis_title='',
            font_family="Arimo, sans-serif",
            title_font_family="Arimo, sans-serif",
            title_font_size=20,
            title=dict(text=title_text, x=0.05, xanchor="left"),
            xaxis=dict(tickangle=0, tickfont=dict(size=11)),
            showlegend=True,
            yaxis=dict(range=[0, 4500]),
            legend=dict(
                title="",
                x=0.98,
                y=0.98,
                xanchor='right',
                yanchor='top',
                bgcolor='rgba(255,255,255,0.5)',
                bordercolor='lightgrey',
                borderwidth=1,
                font=dict(color='black')

            )
        )

        return fig

    # Callback: Bar Chart für Täter:innen nach Beziehungsart und Geschlecht
    @app.callback(
        Output('graph-beziehung-taeter', 'figure'),
        Input('jahr-dropdown', 'value')
    )
    def update_beziehung_taeter(selected_year):
        # Filtere Daten nach Jahr
        df_be_year = df_be[df_be["Jahr"] == selected_year]

        # Gruppieren nach Beziehungsart und Geschlecht
        grouped = df_be_year.groupby(['Beziehungsart', 'Geschlecht'])[
            'Anzahl_beschuldigter_Personen_Total'].sum().reset_index()

        title_text = f'Täter:innen nach Beziehungsart zum Opfer ({selected_year}, absolute Zahlen)'

        # Sortiere Beziehungsarten
        grouped['Beziehungsart'] = pd.Categorical(grouped['Beziehungsart'], categories=relevante_beziehungen, ordered=True)
        grouped = grouped.sort_values('Beziehungsart')

        fig = go.Figure()

        # Balken für weibliche Täter:innen
        weiblich = grouped[grouped["Geschlecht"] == "weiblich"]
        fig.add_trace(go.Bar(
            x=weiblich["Beziehungsart"],
            y=weiblich["Anzahl_beschuldigter_Personen_Total"],
            name='weiblich',
            marker_color=color_women,

        ))

        # Balken für männliche Täter:innen
        maennlich = grouped[grouped["Geschlecht"] == "männlich"]
        fig.add_trace(go.Bar(
            x=maennlich["Beziehungsart"],
            y=maennlich["Anzahl_beschuldigter_Personen_Total"],
            name='männlich',
            marker_color=color_men,

        ))

        # Layout definieren
        fig.update_layout(
            barmode='group',
            xaxis_title='Beziehungsart',
            yaxis_title='',
            legend_title='',
            font_family="Arimo, sans-serif",
            showlegend=False,  # Keine Legende für dieses Diagramm
            title_font_family="Arimo, sans-serif",
            title_font_size=20,
            title=dict(text=title_text, x=0.05, xanchor="left"),
            xaxis=dict(tickangle=0, tickfont=dict(size=11)),
            yaxis = dict(range=[0, 4500]),
        )

        return fig
