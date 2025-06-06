import dash
from dash import dcc, html, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio

# --- Farben ---
dark_border_class = "toggle-btn active"
default_class = "toggle-btn"
color_women = "#cb4d1d"
color_men = "#4992b2"
color_all = "black"

# Roboto-Template definieren
pio.templates["roboto"] = go.layout.Template(
    layout=dict(
        font=dict(
            family="roboto",
            size=14,
            color="black"
        )
    )
)
pio.templates.default = "roboto"

# Daten laden
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

# Prozentanteil berechnen
df["Prozentanteil"] = df.groupby(["Jahr", "Geschlecht"])["Anzahl_geschaedigter_Personen_Total"].transform(lambda x: 100 * x / x.sum())
df_year = df[df["Jahr"] == 2024]

df_be["Prozentanteil"] = df_be.groupby(["Jahr", "Geschlecht"])["Anzahl_beschuldigter_Personen_Total"].transform(lambda x: 100 * x / x.sum())
df_be_year = df_be[df_be["Jahr"] == 2024]

# Layout
layout = html.Div([
    html.Div([
        html.H3([
            "In welcher Beziehung standen Täter:innen und Opfer?",
            html.Span(" ℹ️", id="info-icon", style={"cursor": "pointer", "marginLeft": "10px"})
        ],
            style={'textAlign': 'left', 'marginTop': 20, 'marginLeft': 20}),

        dbc.Tooltip(
            "Die Zahlen Bei Täter:innen und Opfer unterscheiden sich, da Täter:innen mehrere Opfer haben können und umgekehrt.",
            target="info-icon",
            placement="right"
        ),
    ]),

    dcc.Store(id='button-bez-state', data='absolute'),

    html.Div([
        dbc.Row([
            dbc.Col(dbc.ButtonGroup([
                dbc.Button("Prozentuale Verteilung", id="btn-bez-set1", n_clicks=0, className=default_class),
                dbc.Button("Absolute Zahlen", id="btn-bez-set2", n_clicks=0, className=dark_border_class),
            ], size="md", className="mb-4"), width="auto"),
            dbc.Col(dcc.Dropdown(
                id='jahr-dropdown',
                options=[{"label": str(j), "value": j} for j in sorted(df["Jahr"].unique())],
                value=2024,
                clearable=False,
                style={"width": "150px"}
            ), width="auto", style={"marginLeft": "20px", "marginTop": "5px"})
        ], style={"marginLeft": "20px", "gap": "10px"})
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
        }), width=6),
    ], style={'margin-left': '40px'}),

    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009–2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])

# Callbacks
def register_callbacks(app):
    @app.callback(
        Output('graph-beziehung-opfer-stacked', 'figure'),
        Input('button-bez-state', 'data'),
        Input('jahr-dropdown', 'value')
    )
    def update_beziehung_opfer_stacked(view_mode, selected_year):
        df_year = df[df["Jahr"] == selected_year]

        if view_mode == 'absolute':
            grouped = df_year.groupby(['Beziehungsart', 'Geschlecht'])[
                'Anzahl_geschaedigter_Personen_Total'].sum().reset_index()
            y_axis_title = ''
            title_text = f'Opfer nach Beziehungsart zur Täterschaft ({selected_year}, absolute Zahlen)'
        else:
            grouped = df_year.groupby(['Beziehungsart', 'Geschlecht'])['Prozentanteil'].sum().reset_index()
            y_axis_title = 'Anteil in %'
            title_text = f'Opfer nach Beziehungsart zur Täterschaft ({selected_year}, Anteile nach Geschlecht in %)'

        grouped['Beziehungsart'] = pd.Categorical(grouped['Beziehungsart'], categories=relevante_beziehungen,
                                                  ordered=True)
        grouped = grouped.sort_values('Beziehungsart')

        fig = go.Figure()

        weiblich = grouped[grouped["Geschlecht"] == "weiblich"]
        fig.add_trace(go.Bar(
            x=weiblich["Beziehungsart"],
            y=weiblich.iloc[:, 2],
            name='weiblich',
            marker_color=color_women
        ))

        maennlich = grouped[grouped["Geschlecht"] == "männlich"]
        fig.add_trace(go.Bar(
            x=maennlich["Beziehungsart"],
            y=maennlich.iloc[:, 2],
            name='männlich',
            marker_color=color_men
        ))

        fig.update_layout(
            barmode='group',
            xaxis_title='Beziehungsart',
            yaxis_title=y_axis_title,
            legend_title='Geschlecht',
            title=dict(
                text=title_text,
                x=0.01,
                xanchor="left"
            ),
        xaxis = dict(
            tickangle=0,  # horizontal
            tickfont=dict(size=11)  # kleinere Schrift
        )
        )

        return fig

    @app.callback(
        Output('graph-beziehung-taeter-stacked', 'figure'),
        Input('button-bez-state', 'data'),
        Input('jahr-dropdown', 'value')
    )
    def update_beziehung_taeter_stacked(view_mode, selected_year):
        df_be_year = df_be[df_be["Jahr"] == selected_year]

        if view_mode == 'absolute':
            grouped = df_be_year.groupby(['Beziehungsart', 'Geschlecht'])[
                'Anzahl_beschuldigter_Personen_Total'].sum().reset_index()
            y_axis_title = ''
            title_text = f'Täter:innen nach Beziehungsart zum Opfer ({selected_year}, absolute Zahlen)'
        else:
            grouped = df_be_year.groupby(['Beziehungsart', 'Geschlecht'])['Prozentanteil'].sum().reset_index()
            y_axis_title = ''
            title_text = f'Täter:innen nach Beziehungsart zum Opfer ({selected_year}, Anteile nach Geschlecht in %)'


        grouped['Beziehungsart'] = pd.Categorical(grouped['Beziehungsart'], categories=relevante_beziehungen,
                                                  ordered=True)
        grouped = grouped.sort_values('Beziehungsart')

        fig = go.Figure()

        weiblich = grouped[grouped["Geschlecht"] == "weiblich"]
        fig.add_trace(go.Bar(
            x=weiblich["Beziehungsart"],
            y=weiblich.iloc[:, 2],
            name='weiblich',
            marker_color=color_women
        ))

        maennlich = grouped[grouped["Geschlecht"] == "männlich"]
        fig.add_trace(go.Bar(
            x=maennlich["Beziehungsart"],
            y=maennlich.iloc[:, 2],
            name='männlich',
            marker_color=color_men
        ))

        fig.update_layout(
            barmode='group',
            xaxis_title='Beziehungsart',
            yaxis_title=y_axis_title,
            legend_title='',
            showlegend=False,
            title=dict(
                text=title_text,
                x=0.01,
                xanchor="left"
            ),
            xaxis=dict(
                tickangle=0,  # horizontal
                tickfont=dict(size=11)  # kleinere Schrift
            )
        )

        return fig

    @app.callback(
        Output("btn-bez-set1", "className"),
        Output("btn-bez-set2", "className"),
        Output("button-bez-state", "data"),
        Input("btn-bez-set1", "n_clicks"),
        Input("btn-bez-set2", "n_clicks"),
        prevent_initial_call=True
    )
    def update_buttons(n1, n2):
        if ctx.triggered_id == "btn-bez-set2":
            return default_class, dark_border_class, "absolute"
        else:
            return dark_border_class, default_class, "percent"
