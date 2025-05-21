import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# Farben
color_women = "#811616"
color_men = "#0a0a35"
color_all = "black"

# CSV einlesen
opfer = pd.read_csv("data/geschaedigte_tidy.csv")
taeter = pd.read_csv("data/beschuldigte_tidy.csv")

# Filter auf Total Häusliche Gewalt + Beziehungsart = Alle
opfer = opfer[(opfer["Delikt"] == "Total Häusliche Gewalt") & (opfer["Beziehungsart"] == "Alle")]
taeter = taeter[(taeter["Delikt"] == "Total Häusliche Gewalt") & (taeter["Beziehungsart"] == "Alle")]

# Altersgruppen-Spalten
age_order = [
    '<10 Jahre', '10 - 19 Jahre',
    '20 - 29 Jahre', '30 - 39 Jahre', '40 - 49 Jahre', '50 - 59 Jahre',
    '60 - 69 Jahre', '70 Jahre und +'
]

for col in age_order:
    if col in taeter.columns:
        taeter[col] = pd.to_numeric(taeter[col], errors='coerce')
for col in age_order:
    if col in opfer.columns:
        opfer[col] = pd.to_numeric(opfer[col], errors='coerce')





#-----------

layout = html.Div([

    html.Div([
        html.H3("Entwicklung der Altersgruppen über die Jahre", style={'textAlign': 'left', 'marginTop': 30}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='jahr-start-dropdown-tab3',
                    options=[{'label': str(j), 'value': j} for j in range(2009, 2025)],
                    value=2009,
                    clearable=False,
                    style={'width': '150px', 'marginRight': '10px'}
                ),
                dcc.Dropdown(
                    id='jahr-end-dropdown-tab3',
                    options=[{'label': str(j), 'value': j} for j in range(2009, 2025)],
                    value=2024,
                    clearable=False,
                    style={'width': '150px'}
                )
            ], style={'display': 'flex'}),

            dcc.RadioItems(
                id='trend-selector',
                options=[
                    {'label': 'Opfer', 'value': 'opfer'},
                    {'label': 'Täter', 'value': 'taeter'}
                ],
                value='opfer',
                labelStyle={'marginRight': 20},
                style={'display': 'inline-block', 'marginRight': 30}
            ),

            dcc.Dropdown(
                id='gender-selector-trend',
                options=[
                    {'label': 'Männlich', 'value': 'männlich'},
                    {'label': 'Weiblich', 'value': 'weiblich'},
                    {'label': 'Total', 'value': 'Total'}
                ],
                value='Total',
                style={'width': '200px', 'display': 'inline-block'}
            )
        ], style={'textAlign': 'left', 'marginBottom': 20}),

        dbc.Row([
            dbc.Col(dcc.Graph(id='altersgruppen-trend'), width=8),
            dbc.Col(dcc.Graph(id='alterspyramide'), width=4)
        ])
    ]),


    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009-2024)",
               style={'textAlign': 'left', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])

#----
def register_callbacks(app):
    @app.callback(
        Output('altersgruppen-trend', 'figure'),
        [Input('trend-selector', 'value'),
         Input('gender-selector-trend', 'value'),
         Input('jahr-start-dropdown-tab3', 'value'),
         Input('jahr-end-dropdown-tab3', 'value')]
    )
    def update_altersgruppen_trend(perspektive, geschlecht, jahr_start, jahr_ende):
        if jahr_start > jahr_ende:
            raise PreventUpdate

        df = opfer if perspektive == 'taeter' else taeter
        df['Jahr'] = pd.to_numeric(df['Jahr'], errors='coerce')  # oder .astype(int), wenn du sicher bist

        # Filtern
        df_filtered = df[
            (df['Geschlecht'] == geschlecht) &
            (df['Jahr'] >= jahr_start) &
            (df['Jahr'] <= jahr_ende)
            ]

        # Farbschema je nach Geschlecht
        if geschlecht == 'männlich':
            color_scale = px.colors.sequential.Blues
        elif geschlecht == 'Total':
            color_scale = px.colors.sequential.Greys
        else:
            color_scale = px.colors.sequential.Reds
        farben = color_scale

        fig = go.Figure()

        for i, altersklasse in enumerate(age_order):
            if altersklasse in df_filtered.columns:
                x_vals = df_filtered['Jahr']
                y_vals = df_filtered[altersklasse]

                # Hauptlinie
                fig.add_trace(go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode='lines+markers',
                    name=str(altersklasse),
                    line=dict(color=farben[i]),
                    showlegend=True
                ))
        #Beschriftung Linien
                fig.add_annotation(
                    x=x_vals.iloc[-1],
                    y=y_vals.iloc[-1],
                    text=str(altersklasse),
                    showarrow=False,
                    xanchor="left",
                    yanchor="middle",
                    xshift=4,  # Verschiebt den Text 4 Pixel nach rechts
                    font=dict(color=farben[i])
                )



        fig.update_layout(
            title=f"Entwicklung der Altersgruppen bei {geschlecht.lower()}n {'Opfern' if perspektive == 'opfer' else 'Tätern'} ({jahr_start}-{jahr_ende})",
            xaxis_title="Jahr",
            yaxis_title="Anzahl Personen",
            xaxis=dict(range= [2009,2025+2]),
            legend_title="Altersgruppe",
            showlegend=False,
            template="plotly_white",
            hovermode="x unified"

        )
        return fig
#-----



    @app.callback(
        Output('alterspyramide', 'figure'),
        [Input('trend-selector', 'value'),
        Input('jahr-start-dropdown-tab3', 'value')]
    )
    def update_alterspyramide(perspektive,jahr):
        age_order = ['<10 Jahre', '10 - 19 Jahre', '20 - 29 Jahre', '30 - 39 Jahre',
                     '40 - 49 Jahre', '50 - 59 Jahre', '60 - 69 Jahre', '70 Jahre und +']

        df = opfer if perspektive == 'taeter' else taeter
        # Daten für ein Jahr filtern
        df_year = df[df['Jahr'] == jahr]

        # Frauen- und Männerdaten extrahieren
        df_weiblich = df_year[df_year['Geschlecht'] == 'weiblich']
        df_maennlich = df_year[df_year['Geschlecht'] == 'männlich']

        # Leere Listen zur Befüllung
        y_labels = []
        x_women = []
        x_men = []

        for gruppe in age_order:
            # Sicherstellen, dass Spalte vorhanden ist
            if gruppe in df_weiblich.columns and gruppe in df_maennlich.columns:
                y_labels.append(gruppe)
                x_women.append(-df_weiblich[gruppe].values[0])  # negativ für linke Seite
                x_men.append(df_maennlich[gruppe].values[0])  # positiv für rechte Seite

        # Plot erstellen
        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=y_labels,
            x=x_women,
            orientation='h',
            name='Weiblich',
            marker_color='maroon'
        ))

        fig.add_trace(go.Bar(
            y=y_labels,
            x=x_men,
            orientation='h',
            name='Männlich',
            marker_color='royalblue'
        ))

        # Layout
        fig.update_layout(
            title=f"Alterspyramide Taeter:innen – Jahr {jahr}",
            barmode='relative',
            xaxis=dict(
                title='Anzahl Personen',
                tickvals=[-1000, -500, 0, 500, 1000],
                ticktext=[1000, 500, 0, 500, 1000]
            ),

            yaxis=dict(
                title='Altersgruppe',
                categoryorder='array',
                categoryarray=age_order[::-1]  # Umdrehen der Altersgruppen
            ),
            template='plotly_white',
            bargap=0.1,
            height=500
        )

        return fig






#-----
    #Bevölkerungspyramide opfer

    @app.callback(
        Output('alterspyramide-opfer', 'figure'),
        [Input('jahr-end-dropdown-tab3', 'value')]
    )
    def update_alterspyramid_opfer(jahr):
        age_order = ['<10 Jahre', '10 - 19 Jahre', '20 - 29 Jahre', '30 - 39 Jahre',
                     '40 - 49 Jahre', '50 - 59 Jahre', '60 - 69 Jahre', '70 Jahre und +']

        # Daten für ein Jahr filtern
        df_year = opfer[opfer['Jahr'] == jahr]

        # Frauen- und Männerdaten extrahieren
        df_weiblich = df_year[df_year['Geschlecht'] == 'weiblich']
        df_maennlich = df_year[df_year['Geschlecht'] == 'männlich']

        # Leere Listen zur Befüllung
        y_labels = []
        x_women = []
        x_men = []

        for gruppe in age_order:
            # Sicherstellen, dass Spalte vorhanden ist
            if gruppe in df_weiblich.columns and gruppe in df_maennlich.columns:
                y_labels.append(gruppe)
                x_women.append(-df_weiblich[gruppe].values[0])  # negativ für linke Seite
                x_men.append(df_maennlich[gruppe].values[0])  # positiv für rechte Seite

        # Plot erstellen
        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=y_labels,
            x=x_women,
            orientation='h',
            name='Weiblich',
            marker_color='maroon'
        ))

        fig.add_trace(go.Bar(
            y=y_labels,
            x=x_men,
            orientation='h',
            name='Männlich',
            marker_color='royalblue'
        ))

        # Layout
        fig.update_layout(
            title=f"Alterspyramide Opfer – Jahr {jahr}",
            barmode='relative',
            xaxis=dict(
                title='Anzahl Personen',
                tickvals=[-1000, -500, 0, 500, 1000],  # anpassen je nach Skala
                ticktext=[1000, 500, 0, 500, 1000]
            ),

            yaxis=dict(
                title='Altersgruppe',
                categoryorder='array',
                categoryarray=age_order[::-1]  # ← Umdrehen der Altersgruppen
            ),
            template='plotly_white',
            bargap=0.1,
            height=500
        )

        return fig

    @app.callback(
        Output('zeitraum-info-tab3', 'children'),
        [Input('jahr-start-dropdown-tab3', 'value'),
         Input('jahr-end-dropdown-tab3', 'value')]
    )
    def update_zeitraum_info_tab3(jahr_start, jahr_ende):
        if jahr_start == jahr_ende:
            return f"Ausgewähltes Jahr: {jahr_start}"
        else:
            return f"Ausgewählter Zeitraum: {jahr_start} - {jahr_ende}"

