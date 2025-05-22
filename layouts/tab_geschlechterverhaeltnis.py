import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio



#------ Variabeln überall gleich

#Variabeln
color_women = "#cb4d1d"
color_men = "#4992b2"
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

    html.H3("Wie hat sich das Geschlechter verhältnis verändert?", style={'textAlign': 'left', 'marginTop': 20, 'marginLeft': 20}),
    html.H6("Geschlechterverhältnis im Zeitverlauf", style={'textAlign': 'left', 'marginTop': 20, 'marginLeft': 20}),


    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-taeter'),width=6),
        dbc.Col(dcc.Graph(id='graph-opfer'),width=6),
    ]),

    html.Div([
        dbc.ButtonGroup(
            [
                dbc.Button("Prozentuale Verteilung", id="btn-set1", n_clicks=0, className="toggle-btn"),
                dbc.Button("Absolute Zahlen", id="btn-set2", n_clicks=0, className="toggle-btn"),
            ],
            size="md",
            className="mb-4",
            style={"justifyContent": "center", "display": "flex", "gap": "10px", 'padding': '6px 12px',
    'fontSize': '14px',
    'width': 'auto',   # <- wichtig!
    'display': 'inline-block'}
        )
    ], style={'textAlign': 'left'}),



    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009–2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])

# Callbacks
def register_callbacks(app):


    def update_taeter_graph():
        m = taeter_maenlich.groupby('Jahr')['Anzahl_beschuldigter_Personen_Total'].sum()
        w = taeter_weiblich.groupby('Jahr')['Anzahl_beschuldigter_Personen_Total'].sum()
        t = taeter_total.groupby('Jahr')['Anzahl_beschuldigter_Personen_Total'].sum()
        df = pd.DataFrame({'männlich': m, 'weiblich': w, 'total': t}).reset_index()
        df['% männlich'] = df['männlich'] / df['total'] * 100
        df['% weiblich'] = df['weiblich'] / df['total'] * 100

        fig = go.Figure()
        fig.add_bar(x=df['Jahr'], y=df['% männlich'],
                    name='Männliche Täter',
                    marker_color=color_men,
                    marker=dict(
                        line=dict(width=0),
                        color=color_men,  # Hintergrundfarbe
                        pattern=dict(
                            shape="",  # Musterform
                            fgcolor='white',  # Musterfarbe
                            size=20,
                            solidity=0.05,
                            fgopacity=0.4
                        ),
                    ),)

        fig.add_bar(x=df['Jahr'],
                    y=df['% weiblich'],
                    name='Weibliche Täter',
                    marker_color=color_women,
                    marker=dict(
                        line=dict(width=0),
                        color=color_women,  # Hintergrundfarbe
                        pattern=dict(
                            shape="",  # Musterform
                            fgcolor='white',  # Musterfarbe
                            size=20,
                            solidity=0.05,
                            fgopacity=0.4
                        )


                          ),)
        fig.update_layout(barmode='stack',
                          title="Täter:innen nach Geschlecht",
                          yaxis_title="Prozent (%)",
                          showlegend=False,
                          template="plotly_white",
                          bargap=0.1,
                          )
        return fig


    def update_opfer_graph():
        m = opfer_maenlich.groupby('Jahr')['Anzahl_geschaedigter_Personen_Total'].sum()
        w = opfer_weiblich.groupby('Jahr')['Anzahl_geschaedigter_Personen_Total'].sum()
        t = opfer_maenlich.groupby('Jahr')['Anzahl_geschaedigter_Personen_Total'].sum() + opfer_weiblich.groupby('Jahr')['Anzahl_geschaedigter_Personen_Total'].sum()
        df = pd.DataFrame({'männlich': m, 'weiblich': w, 'total': t}).reset_index()
        df['% männlich'] = df['männlich'] / df['total'] * 100
        df['% weiblich'] = df['weiblich'] / df['total'] * 100

        fig = go.Figure()
        fig.add_bar(x=df['Jahr'], y=df['% männlich'],
                    name='Männlich',
                    marker_color=color_men,
                    marker=dict(
                        line=dict(width=0),
                        color=color_men,  # Hintergrundfarbe
                        pattern=dict(
                            shape="",  # Musterform
                            fgcolor='white',  # Musterfarbe
                            size=20,
                            solidity=0.05,
                            fgopacity=0.4
                        )
                          ))
        fig.add_bar(x=df['Jahr'], y=df['% weiblich'],
                    name='Weiblich',
                    marker_color=color_women,
                    marker=dict(
                        line=dict(width=0),
                        color=color_women,  # Hintergrundfarbe
                        pattern=dict(
                            shape="",  # Musterform
                            fgcolor='white',  # Musterfarbe
                            size=20,
                            solidity=0.05,
                            fgopacity=0.4
                        )
                          ),)
        fig.update_layout(barmode='stack',
                          title="Opfer nach Geschlecht",

                          showlegend=True,
                          template="plotly_white",
                          bargap=0.1,
                          ),
        return fig

    def update_entwicklung_taeter():
        # Linie für gesammt Täter
        # Linie für gesammt Täter
        fig = go.Figure()

        # Linie für männliche Täter
        fig.add_trace(go.Scatter(
            x=taeter_maenlich['Jahr'],
            y=taeter_maenlich['Anzahl_beschuldigter_Personen_Total'],
            mode='lines+markers',
            name='Täter männlich',
            marker=dict(symbol='star-diamond', size=10),
            line=dict(width=1.5, color=color_men)
        ))

        # Linie für weibliche Täter
        fig.add_trace(go.Scatter(
            x=taeter_weiblich['Jahr'],
            y=taeter_weiblich['Anzahl_beschuldigter_Personen_Total'],
            mode='lines+markers',
            name='Täter weiblich',
            marker=dict(symbol='star-diamond', size=10),
            line=dict(width=1.5, color=color_women)  # Optional: gestrichelte Linie
        ))

        fig.add_trace(go.Scatter(
            x=taeter_total['Jahr'],
            y=taeter_total['Anzahl_beschuldigter_Personen_Total'],
            mode='lines+markers',
            name='Beschuldigte gesamt',
            marker=dict(symbol='star-diamond', size=10),
            line=dict(width=1.5, color=color_all),
            opacity=0.1,
            showlegend=False,

        ))

        # Layout anpassen
        fig.update_layout(
            template='plotly_white',
            hovermode='x unified',
            xaxis=dict(
                range=[2009 - 0.2, 2025 + 0.2],
                tickmode='linear',
                dtick=1  # Jährliche Ticks
            ),

            yaxis=dict(range=[0, 12000]),
            legend_title='Geschlecht'
        )

        # Layout anpassen
        fig.update_layout(
            title=f"Entwicklung der Täterzahlen nach Geschlecht 2009 bis 2025)",
            xaxis_title="Jahr",
            yaxis_title="Anzahl Personen",
            legend_title="Gruppe",
            template="plotly_white",
            hovermode="x unified",
            showlegend = False,
        )

        return fig

    def update_entwicklung_opfer():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=opfer_maenlich['Jahr'], y=opfer_maenlich['Anzahl_geschaedigter_Personen_Total'],
                                 mode='lines+markers', name='Opfer männlich', line=dict(width=1.5, color=color_men),marker=dict(size=10, color=color_men)))
        fig.add_trace(go.Scatter(x=opfer_weiblich['Jahr'], y=opfer_weiblich['Anzahl_geschaedigter_Personen_Total'],
                                 mode='lines+markers', name='Opfer weiblich', line=dict(width=1.5, color=color_women),marker=dict(size=10)))
        fig.add_trace(go.Scatter(x=opfer_total['Jahr'], y=opfer_total['Anzahl_geschaedigter_Personen_Total'],
                                 mode='lines+markers', name='Opfer gesamt', line=dict(width=1.5, color=color_all),
                                 marker=dict(size=10), opacity=0.1))
        # Layout anpassen
        fig.update_layout(
            title='Opferzahlen nach Geschlecht (2009–2024)',
            xaxis_title='Jahr',
            yaxis_title='Anzahl geschaedigter Personen',
            template='plotly_white',
            hovermode='x unified',
            xaxis=dict(
                range=[2009 - 0.2, 2025 + 0.2],
                tickmode='linear',
                dtick=1  # Jährliche Ticks
            ),

            yaxis=dict(range=[0, 12000]),
            legend_title='Geschlecht'
        )

        # Layout anpassen
        fig.update_layout(
            title=f"Entwicklung der Opfer nach Geschlecht (2009-2025)",
            xaxis_title="Jahr",
            yaxis_title="Anzahl Personen",
            legend_title="Gruppe",
            template="plotly_white",
            hovermode="x unified"
        )

        return fig



    @app.callback(
        Output('graph-taeter', 'figure'),
        Output('graph-opfer', 'figure'),
        Input('btn-set1', 'n_clicks'),
        Input('btn-set2', 'n_clicks'),
    )
    def update_graphs(n1, n2):
        if n2 > n1:
            return update_entwicklung_taeter(), update_entwicklung_opfer()
        return update_taeter_graph(), update_opfer_graph()
