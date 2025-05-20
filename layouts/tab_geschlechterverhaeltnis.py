import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Farben
color_women = "#7B1E1E"
color_men = "Royalblue"
color_all = "black"

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

# Layout
layout = html.Div([
    html.H3("Geschlechterverhältnis im Zeitverlauf", style={'textAlign': 'left', 'marginTop': 20}),


    dbc.Row([
        dbc.Col(dcc.Graph(id='graph-taeter'),width=5),
        dbc.Col(dcc.Graph(id='graph-opfer'),width=5),

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


    def update_taeter_graph():
        m = taeter_maenlich.groupby('Jahr')['Anzahl_beschuldigter_Personen_Total'].sum()
        w = taeter_weiblich.groupby('Jahr')['Anzahl_beschuldigter_Personen_Total'].sum()
        t = taeter_total.groupby('Jahr')['Anzahl_beschuldigter_Personen_Total'].sum()
        df = pd.DataFrame({'männlich': m, 'weiblich': w, 'total': t}).reset_index()
        df['% männlich'] = df['männlich'] / df['total'] * 100
        df['% weiblich'] = df['weiblich'] / df['total'] * 100

        fig = go.Figure()
        fig.add_bar(x=df['Jahr'], y=df['% männlich'], name='Männliche Täter', marker_color=color_men, marker=dict(
                              line=dict(width=0),
                          ),)
        fig.add_bar(x=df['Jahr'], y=df['% weiblich'], name='Weibliche Täter', marker_color=color_women,marker=dict(
                              line=dict(width=0),
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
        fig.add_bar(x=df['Jahr'], y=df['% männlich'], name='Männlich', marker_color=color_men, marker=dict(
                              line=dict(width=0),
                          ))
        fig.add_bar(x=df['Jahr'], y=df['% weiblich'], name='Weiblich', marker_color=color_women, marker=dict(
                              line=dict(width=0),
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
        Input('toggle-set', 'value')
    )
    def update_graphs(toggle_value):
        if toggle_value == 'set1':
            return update_taeter_graph(), update_opfer_graph()
        else:
            return update_entwicklung_taeter(), update_entwicklung_opfer()
