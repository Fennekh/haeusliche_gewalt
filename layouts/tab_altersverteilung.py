import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
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
        html.H3("Wie ist die Altersverteilung über Täter:Innen und Opfer", style={'textAlign': 'left', 'marginTop': 20, 'marginLeft': 20}),
        #html.H6("Entwicklung Anzahl Betroffene",style={'textAlign': 'left', 'marginTop': 20, 'marginLeft': 20}),

        # Linke und rechte Spalte
        dbc.Row([
            # Linke Spalte: Filter + Trend-Grafik
            dbc.Col([
                # Alle Filter in einer horizontalen Reihe
                html.Div([

                    dcc.Dropdown(
                        id='gender-selector-trend',
                        options=[
                            {'label': 'Männlich', 'value': 'männlich'},
                            {'label': 'Weiblich', 'value': 'weiblich'},
                            {'label': 'Alle Geschlechter', 'value': 'Total'}
                        ],
                        value='Total',
                        style={'width': '200px'}
                    ),

                    dcc.RadioItems(
                        id='trend-selector',
                        options=[
                            {'label': 'Opfer', 'value': 'opfer'},
                            {'label': 'Täter:innen', 'value': 'taeter'}
                        ],
                        value='opfer',
                        labelStyle={'display': 'inline-block', 'marginLeft': '20px'},
                        style={'marginRight': '30px'}
                    ),
                ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '10px', }),

                # Trend-Grafik
                dcc.Graph(id='altersgruppen-trend',  style={
        'height': '65vh',
        'minHeight': '300px'
    })
            ], width=8),

            # Rechte Spalte: Dropdown + Pyramide
            dbc.Col([
                html.Div([
                    dcc.Dropdown(
                        id='jahr-pyramide-dropdown-tab3',
                        options=[{'label': str(j), 'value': j} for j in range(2009, 2025)],
                        value=2024,
                        clearable=False,
                        style={'width': '100%', 'marginBottom': '20px'}
                    )
                ], style={'marginBottom': '10px'}),

                dcc.Graph(id='alterspyramide',style={
        'height': '65vh',
        'minHeight': '300px'
    })
            ], width=4)
        ], style={'alignItems': 'flex-start', 'marginLeft': '20px'}),
    ]),

    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009–2024)",
               style={'textAlign': 'left', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])




#----
def register_callbacks(app):
    @app.callback(
        Output('altersgruppen-trend', 'figure'),
        [Input('trend-selector', 'value'),
         Input('gender-selector-trend', 'value'),]
    )
    def update_altersgruppen_trend(perspektive, geschlecht):

        jahr_start = 2009
        jahr_ende = 2024
        df = opfer if perspektive == 'opfer' else taeter
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
            max_range = 4000
        else:
            color_scale = px.colors.sequential.Reds
        farben = color_scale
        max_range = 4000

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
                    showlegend=True,
                    hoverlabel=dict(
                        font=dict(size=12),
                    ),
                    hovertemplate=f'%{{y:.0f}} Personen<br>{altersklasse}<br>%{{x}}<extra></extra>'
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
                    font=dict(color=color_all),

                )



        fig.update_layout(
            title=f"Entwicklung der Altersgruppen bei {geschlecht.lower()} {'Opfer' if perspektive == 'opfer' else 'Täter:innen'} ({jahr_start}-{jahr_ende})",
            xaxis_title="Jahr",
            yaxis_title="Anzahl Personen",
            yaxis = dict(range=[0, max_range]),
            xaxis=dict(range= [2009,2024+2]),
            legend_title="Altersgruppe",
            showlegend=False,
            template="plotly_white",
            hoverlabel=dict(
                bgcolor="white",
                font_size=18,

            )


        )
        return fig
#-----



    @app.callback(
        Output('alterspyramide', 'figure'),
        [Input('trend-selector', 'value'),
        Input('jahr-pyramide-dropdown-tab3', 'value')]
    )
    def update_alterspyramide(perspektive,jahr):
        age_order = ['<10 Jahre', '10 - 19 Jahre', '20 - 29 Jahre', '30 - 39 Jahre',
                     '40 - 49 Jahre', '50 - 59 Jahre', '60 - 69 Jahre', '70 Jahre und +']

        df = opfer if perspektive == 'opfer' else taeter
        # Daten für ein Jahr filtern
        titel_perspektive =   "Opfer" if perspektive == 'opfer' else "Täter:innen"

        pattern = "/" if perspektive == 'taeter' else "\\"

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
            marker_color= color_women,
            marker=dict(

                pattern=dict(
                    shape="",  # diagonales Muster
                    bgcolor=color_women,  # deutlichere Kontrastfarbe
                    size=20,
                    solidity=0.05,
                    fgopacity=0.4

                )
            )
        ))

        fig.add_trace(go.Bar(
            y=y_labels,
            x=x_men,
            orientation='h',
            name='Männlich',
            marker_color=color_men,
            marker=dict(

                pattern=dict(
                    shape="",  # diagonales Muster
                    bgcolor=color_men,  # deutlichere Kontrastfarbe
                    size=20,
                    solidity=0.05,
                    fgopacity=0.4

                )
            )
        ))

        # Layout
        fig.update_layout(
            title=f"Altersverteilung von Anzahl {titel_perspektive} ({jahr})",
            barmode='relative',
            xaxis=dict(
                title='Anzahl Personen',
                tickvals=[-2500, -2000, -1500,-1000, -500, 0, 500, 1000,1500,2000,2500],
                ticktext=[2500, 2000, 1500,1000, 500, 0, 500, 1000,1500,2000,2500],
                range = [-2700, 2700]
            ),

            yaxis=dict(
                title='',
                categoryorder='array',
                categoryarray=age_order  # Umdrehen der Altersgruppen
            ),
            template='plotly_white',
            bargap=0.1,
            legend = dict(
                x=1,  # Rechts (1 = 100 %)
                y=1,  # Oben (1 = 100 %)
                xanchor="right",
                yanchor="top"
            )
        )

        return fig






#-----
    #Bevölkerungspyramide opfer

    @app.callback(
        Output('alterspyramide-opfer', 'figure'),
        [Input('jahr-pyramide-dropdown-tab3', 'value')]
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
                categoryarray=age_order
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

