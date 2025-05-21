import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
from matplotlib.pyplot import legend

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


# Daten laden und filtern
opfer = pd.read_csv("data/geschaedigte_tidy.csv")
taeter = pd.read_csv("data/beschuldigte_tidy.csv")

opfer = opfer[(opfer["Delikt"] == "Total Häusliche Gewalt") & (opfer["Beziehungsart"] == "Alle")]
taeter = taeter[(taeter["Delikt"] == "Total Häusliche Gewalt") & (taeter["Beziehungsart"] == "Alle")]

opfer_maenlich = opfer[opfer["Geschlecht"] == "männlich"]
opfer_weiblich = opfer[opfer["Geschlecht"] == "weiblich"]
opfer_total = opfer[opfer["Geschlecht"] == "Total"]

taeter_maenlich = taeter[taeter["Geschlecht"] == "männlich"]
taeter_weiblich = taeter[taeter["Geschlecht"] == "weiblich"]
taeter_total = taeter[taeter["Geschlecht"] == "Total"]

##DAtenaufbereitung beziehung
# Daten einlesen (ersetze Pfad bei Bedarf)
df = pd.read_csv("data/geschaedigte_tidy.csv")
df_be = pd.read_csv("data/beschuldigte_tidy.csv")

# Daten bereinigen
df["Beziehungsart"] = df["Beziehungsart"].str.strip()
df_be["Beziehungsart"] = df_be["Beziehungsart"].str.strip()
relevante_beziehungen = [
    "Partnerschaft",
    "ehemalige Partnerschaft",
    "Eltern-Kind-Beziehung",
    "andere Verwandtschaftsbeziehung"
]
#für beschädigte
df = df[
    (df["Delikt"] == "Total Häusliche Gewalt") &
    (df["Beziehungsart"].isin(relevante_beziehungen)) &
    (df["Geschlecht"].isin(["männlich", "weiblich"]))
]
df = df[["Jahr", "Geschlecht", "Beziehungsart", "Anzahl_geschaedigter_Personen_Total"]].dropna()
df["Anzahl_geschaedigter_Personen_Total"] = df["Anzahl_geschaedigter_Personen_Total"].astype(float)
df["Jahr"] = df["Jahr"].astype(int)

#für beschuligte
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
# Nur ein Jahr verwenden (z.B. 2024)
df_year = df[df["Jahr"] == 2024]
df_maennlich = df_year[df_year["Geschlecht"] == "männlich"]
df_weiblich = df_year[df_year["Geschlecht"] == "weiblich"]

# Prozentanteil berechnen
df_be["Prozentanteil"] = df_be.groupby(["Jahr", "Geschlecht"])["Anzahl_beschuldigter_Personen_Total"].transform(lambda x: 100 * x / x.sum())
# Nur ein Jahr verwenden (z.B. 2024)
df_be_year = df_be[df_be["Jahr"] == 2024]
df_be_maennlich = df_be_year[df_be_year["Geschlecht"] == "männlich"]
df_be_weiblich = df_be_year[df_be_year["Geschlecht"] == "weiblich"]




# Layout
layout = html.Div([



    html.H3("In welcher Beziehung stehen Opfer und Täter in Beziehung?", style={'textAlign': 'left', 'marginTop': 20, 'marginLeft': 20}),
    html.H6("Prozentuale verteilung nach Beziehungsart", style={'textAlign': 'left', 'marginTop': 20, 'marginLeft': 20}),

    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-beziehung-taeter'),width=6),
        dbc.Col(dcc.Graph(id='graph-beziehung-opfer'), width=6),
    ]),

    html.Div([
        dcc.RadioItems(
                id='toggle-set',
                options=[
                    {'label': 'Prozentuale Verteilung', 'value': 'set1'},
                    {'label': 'Absolute Zahlen', 'value': 'set2'}
                ],
                value='set1',
                labelStyle={'display': 'inline-block', 'marginRight': '10px'}
            ),
            ], style={'textAlign': 'center'}),

    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009–2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])

# Callbacks
def register_callbacks(app):


    @app.callback(
        Output('graph-beziehung-opfer', 'figure'),
        Input('graph-beziehung-opfer', 'id')
    )
    def update_beziehungs_opfer_graph(_):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_maennlich["Beziehungsart"],
            y=df_maennlich["Prozentanteil"],
            name="männlich",
            marker=dict(

                pattern=dict(
                    shape="\\",  # diagonales Muster
                    bgcolor=color_men,  # deutlichere Kontrastfarbe
                    size=20,
                    solidity=0.05,
                    fgopacity=0.6

                )
            )
        ))
        fig.add_trace(go.Bar(
            x=df_weiblich["Beziehungsart"],
            y=df_weiblich["Prozentanteil"],
            name="weiblich",
            marker=dict(

                pattern=dict(
                    shape="\\",  # diagonales Muster
                    bgcolor=color_women,  # deutlichere Kontrastfarbe
                    size=20,
                    solidity=0.05,
                    fgopacity=0.6

                )
            )
        ))

        fig.update_layout(
            barmode="group",
            title="Opfer (2024)",
            #xaxis_title="Beziehungsart",
            yaxis_title="Anteil in %",

        )

        return fig

    @app.callback(
        Output('graph-beziehung-taeter', 'figure'),
        Input('graph-beziehung-taeter', 'id')
    )
    def update_beziehungs_taeter_graph(_):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_be_maennlich["Beziehungsart"],
            y=df_be_maennlich["Prozentanteil"],
            name="männlich",

            marker=dict(
                pattern=dict(
                    bgcolor=color_men,
                    shape="/",  # diagonales Muster
                    fgcolor='white',
                    size=20,
                    solidity=0.05,
                    fgopacity=0.4
                )
            )
        ))

        fig.add_trace(go.Bar(
            x=df_be_weiblich["Beziehungsart"],
            y=df_be_weiblich["Prozentanteil"],
            name="weiblich",
            marker=dict(

                pattern=dict(
                    shape="/",  # diagonales Muster
                    bgcolor=color_women,  # deutlichere Kontrastfarbe
                    size=20,
                    solidity=0.05,
                    fgopacity=0.4

                )
            )

        ))

        fig.update_layout(
            barmode="group",
            title="Beziehungsverhältnis von Täter:innen zu Opfer (2024)",
            #xaxis_title="Beziehungsart",
            yaxis_title="Anteil in %",
            showlegend=False,

        )

        return fig



    @app.callback(
        Output('graph-taeter_bez', 'figure'),
        Output('graph-opfer_bez', 'figure'),
        Input('toggle-set', 'value')
    )
    def update_graphs(toggle_value):
        if toggle_value == 'set1':
            return update_beziehungs_taeter_graph(), update_beziehungs_opfer_graph()
        else:
            return update_entwicklung_taeter(), update_entwicklung_opfer()
