import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Farben
color_women = "maroon"
color_men = "royalblue"
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
    html.H3("Geschlechterverhältnis im Zeitverlauf", style={'textAlign': 'center', 'marginTop': 20}),
    html.Div([
        dcc.Graph(id='graph-opfer', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='graph-taeter', style={'width': '48%', 'display': 'inline-block'})
    ], style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col(dcc.Graph(id='zeitliche-entwicklung-taeter'), width=6),
        dbc.Col(dcc.Graph(id='zeitliche-entwicklung-opfer'), width=6)
    ]),
    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009–2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])

# Callbacks
def register_callbacks(app):
    @app.callback(
        Output('graph-opfer', 'figure'),
        Input('graph-opfer', 'id')
    )
    def update_opfer_graph(_):
        m = opfer_maenlich.groupby('Jahr')['Anzahl_geschaedigter_Personen_Total'].sum()
        w = opfer_weiblich.groupby('Jahr')['Anzahl_geschaedigter_Personen_Total'].sum()
        t = opfer_total.groupby('Jahr')['Anzahl_geschaedigter_Personen_Total'].sum()
        df = pd.DataFrame({'männlich': m, 'weiblich': w, 'total': t}).reset_index()
        df['% männlich'] = df['männlich'] / df['total'] * 100
        df['% weiblich'] = df['weiblich'] / df['total'] * 100

        fig = go.Figure()
        fig.add_bar(x=df['Jahr'], y=df['% männlich'], name='Männliche Opfer', marker_color=color_men)
        fig.add_bar(x=df['Jahr'], y=df['% weiblich'], name='Weibliche Opfer', marker_color=color_women)
        fig.update_layout(barmode='stack', title="Opfer nach Geschlecht", yaxis_title="Prozent (%)", template="plotly_white")
        return fig

    @app.callback(
        Output('graph-taeter', 'figure'),
        Input('graph-taeter', 'id')
    )
    def update_taeter_graph(_):
        m = taeter_maenlich.groupby('Jahr')['Anzahl_beschuldigter_Personen_Total'].sum()
        w = taeter_weiblich.groupby('Jahr')['Anzahl_beschuldigter_Personen_Total'].sum()
        t = taeter_total.groupby('Jahr')['Anzahl_beschuldigter_Personen_Total'].sum()
        df = pd.DataFrame({'männlich': m, 'weiblich': w, 'total': t}).reset_index()
        df['% männlich'] = df['männlich'] / df['total'] * 100
        df['% weiblich'] = df['weiblich'] / df['total'] * 100

        fig = go.Figure()
        fig.add_bar(x=df['Jahr'], y=df['% männlich'], name='Männliche Täter', marker_color=color_men)
        fig.add_bar(x=df['Jahr'], y=df['% weiblich'], name='Weibliche Täter', marker_color=color_women)
        fig.update_layout(barmode='stack', title="Täter nach Geschlecht", yaxis_title="Prozent (%)", template="plotly_white")
        return fig

    @app.callback(
        Output('zeitliche-entwicklung-taeter', 'figure'),
        Input('zeitliche-entwicklung-taeter', 'id')
    )
    def update_entwicklung_taeter(_):
        # Linie für gesammt Täter
        fig.add_trace(go.Scatter(
            x=taeter_total['Jahr'],
            y=taeter_total['Anzahl_beschuldigter_Personen_Total'],
            mode='lines+markers',
            name='Beschuldigte gesamt',
            marker=dict(symbol='star-diamond', size=10),
            line=dict(width=1.5, color=color_all)

        ))

        fig.add_trace(go.Scatter(
            x=opfer_total['Jahr'],
            y=opfer_total['Anzahl_geschaedigter_Personen_Total'],
            mode='lines+markers',
            name='Geschädigte gesamt',
            marker=dict(size=9),
            line=dict(width=1.5, color=color_all, dash='dot')

        ))

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

        # Layout anpassen
        fig.update_layout(
            template='plotly_white',
            hovermode='x unified',
            xaxis=dict(
                range=[jahr_start - 0.2, jahr_ende + 0.2],
                tickmode='linear',
                dtick=1  # Jährliche Ticks
            ),

            yaxis=dict(range=[0, 12000]),
            legend_title='Geschlecht'
        )

        # Layout anpassen
        fig.update_layout(
            title=f"Entwicklung der Täterzahlen nach Geschlecht ({jahr_start}-{jahr_ende})",
            xaxis_title="Jahr",
            yaxis_title="Anzahl Personen",
            legend_title="Gruppe",
            template="plotly_white",
            hovermode="x unified"
        )

        return fig

    @app.callback(
        Output('zeitliche-entwicklung-opfer', 'figure'),
        Input('zeitliche-entwicklung-opfer', 'id')
    )
    def update_entwicklung_opfer(_):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=opfer_total['Jahr'], y=opfer_total['Anzahl_geschaedigter_Personen_Total'],
                                 mode='lines+markers', name='Opfer gesamt', line=dict(color=color_all)))
        fig.add_trace(go.Scatter(x=opfer_maenlich['Jahr'], y=opfer_maenlich['Anzahl_geschaedigter_Personen_Total'],
                                 mode='lines+markers', name='Opfer männlich', line=dict(color=color_men)))
        fig.add_trace(go.Scatter(x=opfer_weiblich['Jahr'], y=opfer_weiblich['Anzahl_geschaedigter_Personen_Total'],
                                 mode='lines+markers', name='Opfer weiblich', line=dict(color=color_women)))
        fig.update_layout(title="Opferzahlen im Zeitverlauf", xaxis_title="Jahr", yaxis_title="Anzahl", template="plotly_white")
        return fig
