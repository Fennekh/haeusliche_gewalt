import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio


# --- Variabeln ---
plotly_font = dict(
    family="Arimo, sans-serif",
    size=14,
    color="black"
)
pio.templates["arimo"] = go.layout.Template(layout=dict(font=plotly_font))
pio.templates.default = "arimo"

# Farben
color_women = "#cb4d1d"
color_men = "#4992b2"

# --- Daten laden und vorbereiten ---
opfer = pd.read_csv("data/geschaedigte_tidy.csv")
taeter = pd.read_csv("data/beschuldigte_tidy.csv")

opfer = opfer[(opfer["Delikt"] == "Total Häusliche Gewalt") & (opfer["Beziehungsart"] == "Alle")]
taeter = taeter[(taeter["Delikt"] == "Total Häusliche Gewalt") & (taeter["Beziehungsart"] == "Alle")]


# Daten für Beziehungsarten vorbereiten
df = pd.read_csv("data/geschaedigte_tidy.csv")
df_be = pd.read_csv("data/beschuldigte_tidy.csv")

df["Beziehungsart"] = df["Beziehungsart"].str.strip()
df_be["Beziehungsart"] = df_be["Beziehungsart"].str.strip()

relevante_beziehungen = [
    "Partnerschaft",
    "ehemalige Partnerschaft",
    "Eltern-Kind-Beziehung",
    "andere Verwandtschaftsbeziehung"
]

df = df[
    (df["Delikt"] == "Total Häusliche Gewalt") &
    (df["Beziehungsart"].isin(relevante_beziehungen)) &
    (df["Geschlecht"].isin(["männlich", "weiblich"]))
]
df = df[["Jahr", "Geschlecht", "Beziehungsart", "Anzahl_geschaedigter_Personen_Total"]].dropna()
df["Anzahl_geschaedigter_Personen_Total"] = df["Anzahl_geschaedigter_Personen_Total"].astype(float)
df["Jahr"] = df["Jahr"].astype(int)

df_be = df_be[
    (df_be["Delikt"] == "Total Häusliche Gewalt") &
    (df_be["Beziehungsart"].isin(relevante_beziehungen)) &
    (df_be["Geschlecht"].isin(["männlich", "weiblich"]))
]
df_be = df_be[["Jahr", "Geschlecht", "Beziehungsart", "Anzahl_beschuldigter_Personen_Total"]].dropna()
df_be["Anzahl_beschuldigter_Personen_Total"] = df_be["Anzahl_beschuldigter_Personen_Total"].astype(float)
df_be["Jahr"] = df_be["Jahr"].astype(int)

# Layout
layout = html.Div([
    html.Div([
        html.H2([
            "Tatort Beziehung: Wo treffen Täter:innen auf ihre Opfer?",
            html.Span(" ℹ️", id="info-icon", style={"cursor": "pointer", "marginLeft": "10px"}),
        html.H3([
            "Ob im sozialen Umfeld, in der Familie oder unter Fremden – diese Infografik zeigt, in welchen Beziehungen Täter:innen und Opfer zueinander stehen und wie häufig diese Konstellationen sind.",
        ],
            style={'textAlign': 'left', 'marginLeft': 40, 'paddingBottom': '8px', 'marginTop': 48,  'fontWeight': 600 }),

        dbc.Tooltip(
            "Die Zahlen Bei Täter:innen und Opfer können sich unterscheiden, da Täter:innen mehrere Opfer haben können und umgekehrt. Wird eine Person beispielsweise von der Mutter und dem Bruder bedroht, so zählt dies je einmal in den Kategorien Eltern-Kind-Beziehung und andere Verwandtschaftsbeziehung.",
            target="info-icon",
            style={'textAlign': 'left'},
            placement="right"
        ),
    ]),

    html.Div([
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='jahr-dropdown',
                options=[{"label": str(j), "value": j} for j in sorted(df["Jahr"].unique())],
                value=2024,
                clearable=False,
                style={"width": "150px"}
            ), width="auto", style={ "marginTop": "20px"})
        ], style={"marginLeft": "30px"})
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-beziehung-taeter-stacked', style={
            'height': '65vh',
            'minHeight': '300px',
            'textAlign': 'left',
        }), width=6),
        dbc.Col(dcc.Graph(id='graph-beziehung-opfer-stacked', style={
            'height': '65vh',
            'minHeight': '300px',
            'textAlign': 'left',
            'font_family': 'arimo',
        }), width=6),
    ], ),

    html.Div([
        html.Hr(),



        html.P("Quelle: BFS – Polizeiliche Kriminalstatistik (PKS), Datenstand: 14.02.2025 ",
               style={'textAlign': 'left', 'marginLeft':40, 'fontStyle': 'italic', 'fontSize': 16, 'color': 'black'}),

        html.P("Für die Richtigkeit, Vollständigkeit und Aktualität der dargestellten Daten übernehmen wir keine Gewähr. Die Angaben basieren auf den zum genannten Zeitpunkt veröffentlichten Informationen des Bundesamts für Statistik.",
               style={'textAlign': 'left', 'marginLeft': 40, 'fontStyle': 'italic', 'fontSize': 16, 'color': 'black'}),
    ])
])

# Callbacks
def register_callbacks(app):
    @app.callback(
        Output('graph-beziehung-opfer-stacked', 'figure'),
        Input('jahr-dropdown', 'value')
    )
    def update_beziehung_opfer_stacked(selected_year):
        df_year = df[df["Jahr"] == selected_year]
        grouped = df_year.groupby(['Beziehungsart', 'Geschlecht'])[
            'Anzahl_geschaedigter_Personen_Total'].sum().reset_index()
        y_axis_title = ''
        title_text = f'Opfer nach Beziehungsart zur Täterschaft ({selected_year}, absolute Zahlen)'

        grouped['Beziehungsart'] = pd.Categorical(grouped['Beziehungsart'], categories=relevante_beziehungen, ordered=True)
        grouped = grouped.sort_values('Beziehungsart')

        fig = go.Figure()

        weiblich = grouped[grouped["Geschlecht"] == "weiblich"]
        fig.add_trace(go.Bar(
            x=weiblich["Beziehungsart"],
            y=weiblich["Anzahl_geschaedigter_Personen_Total"],
            name='Weiblich',
            marker_color=color_women
        ))

        maennlich = grouped[grouped["Geschlecht"] == "männlich"]
        fig.add_trace(go.Bar(
            x=maennlich["Beziehungsart"],
            y=maennlich["Anzahl_geschaedigter_Personen_Total"],
            name='Männlich',
            marker_color=color_men
        ))

        fig.update_layout(
            barmode='group',
            xaxis_title='Beziehungsart',
            yaxis_title=y_axis_title,
            font_family="Arimo, sans-serif",  # bleibt erhalten
            title_font_family="Arimo, sans-serif",
            title_font_size=20,
            title=dict(text=title_text, x=0.05, xanchor="left"),
            xaxis=dict(tickangle=0, tickfont=dict(size=11)),
        showlegend = True,
        legend = dict(
            title="",
            x=0.98,
            y=0.98,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255,255,255,0.5)',  # halbtransparenter Hintergrund
            bordercolor='lightgrey',
            borderwidth=1,
            font=dict(color='black')

        )
        )

        return fig

    @app.callback(
        Output('graph-beziehung-taeter-stacked', 'figure'),
        Input('jahr-dropdown', 'value')
    )
    def update_beziehung_taeter_stacked(selected_year):
        df_be_year = df_be[df_be["Jahr"] == selected_year]
        grouped = df_be_year.groupby(['Beziehungsart', 'Geschlecht'])[
            'Anzahl_beschuldigter_Personen_Total'].sum().reset_index()
        y_axis_title = ''
        title_text = f'Täter:innen nach Beziehungsart zum Opfer ({selected_year}, absolute Zahlen)'

        grouped['Beziehungsart'] = pd.Categorical(grouped['Beziehungsart'], categories=relevante_beziehungen, ordered=True)
        grouped = grouped.sort_values('Beziehungsart')

        fig = go.Figure()

        weiblich = grouped[grouped["Geschlecht"] == "weiblich"]
        fig.add_trace(go.Bar(
            x=weiblich["Beziehungsart"],
            y=weiblich["Anzahl_beschuldigter_Personen_Total"],
            name='weiblich',
            marker_color=color_women
        ))

        maennlich = grouped[grouped["Geschlecht"] == "männlich"]
        fig.add_trace(go.Bar(
            x=maennlich["Beziehungsart"],
            y=maennlich["Anzahl_beschuldigter_Personen_Total"],
            name='männlich',
            marker_color=color_men
        ))

        fig.update_layout(

            barmode='group',
            xaxis_title='Beziehungsart',
            yaxis_title=y_axis_title,
            legend_title='',
            font_family="Arimo, sans-serif",
            showlegend=False,
            title_font_family="Arimo, sans-serif",
            title_font_size=20,
            title=dict(
                text=title_text,
                x=0.05,
                xanchor="left"
            ),
            xaxis=dict(tickangle=0, tickfont=dict(size=11))
        )

        return fig
