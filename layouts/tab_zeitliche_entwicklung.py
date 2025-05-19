import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.validators.scatter.marker import SymbolValidator
from dash import dash_table
import matplotlib.pyplot as plt
import io
import base64

# Importieren der gemeinsamen Daten
from layouts.data import load_data

#Variabeln
color_women= "maroon"
color_men = "royalblue"
color_all = "black"


#------
#Daten laden
opfer = pd.read_csv("/Users/karinhugentobler/PycharmProjects/dashboard_haeusliche_gewalt/data/geschaedigte_tidy.csv")
taeter = pd.read_csv("/Users/karinhugentobler/PycharmProjects/dashboard_haeusliche_gewalt/data/beschuldigte_tidy.csv")

#Datenvorbereitung für Tabelle

# Nur Beziehungsart = Alle und Geschlecht = Total verwenden
taeter_filtered = taeter[(taeter["Beziehungsart"] == "Alle") & (taeter["Geschlecht"] == "Total")]

# Gruppieren nach Delikt und Jahr
taeter_grouped = taeter_filtered.groupby(['Delikt', 'Jahr'])['Anzahl_beschuldigter_Personen_Total'].sum().reset_index()

# Pivot-Tabelle: Delikt als Zeile, Jahre als Spalten
trend_pivot = taeter_grouped.pivot(index='Delikt', columns='Jahr', values='Anzahl_beschuldigter_Personen_Total')

# Fehlende Werte auffüllen (z. B. Delikte, die in 2009 oder 2024 nicht gemeldet wurden)
trend_pivot = trend_pivot.fillna(0)

# Mini-Trendliste + aktuelle Zahlen + Veränderung
trend_pivot['Anzahl'] = trend_pivot[2024]
trend_pivot['Trend'] = trend_pivot.apply(lambda row: row.loc[2009:2024].tolist(), axis=1)
trend_pivot['Veränderung (%)'] = ((trend_pivot[2024] - trend_pivot[2009]) / trend_pivot[2009].replace(0, 1)) * 100

# Sortieren nach Anzahl (2024)
trend_pivot_sorted = trend_pivot.sort_values(by='Anzahl', ascending=False).reset_index()



#Datenvorbereitung Grafiken
#Filtern nach Delikte gesamt
taeter = taeter[taeter["Delikt"] == "Total Häusliche Gewalt"]
opfer = opfer[opfer["Delikt"] == "Total Häusliche Gewalt"]

#Filtern nach Beziehungsart alle
taeter = taeter[taeter["Beziehungsart"] == "Alle"]
opfer = opfer[opfer["Beziehungsart"] == "Alle"]

#Filtern nach geschlecht
taeter_maenlich = taeter[taeter["Geschlecht"] == "männlich"]
taeter_weiblich = taeter[taeter["Geschlecht"] == "weiblich"]
taeter_total = taeter[taeter["Geschlecht"] == "Total"]

opfer_maenlich = opfer[opfer["Geschlecht"] == "männlich"]
opfer_weiblich = opfer[opfer["Geschlecht"] == "weiblich"]
opfer_total = opfer[opfer["Geschlecht"] == "Total"]





#----

# Layout für den ersten Tab (Zeitliche Entwicklung)
layout = html.Div([
    # Zeitraum-Information
    html.Div(id='zeitraum-info-tab1', style={'textAlign': 'center', 'marginBottom': 20}),

    # Überschrift & Zeitraum-Slider
    dbc.Row([
        dbc.Col([
            html.H3("Zeitliche Entwicklung von Opfern und Tätern nach Geschlecht",
                    style={'textAlign': 'left', 'marginTop': 20, 'marginLeft': 20})
        ], width=3),
        dbc.Col([
            html.H4("Zeitraum auswählen:", style={'marginBottom': 10}),
            dcc.RangeSlider(
                id='jahr-slider-tab1',
                min=2009,
                max=2024,
                value=[2009, 2024],
                marks={year: str(year) for year in range(2009, 2025)},
                step=1,
                tooltip={"placement": "bottom", "always_visible": False},
                className='schwarzer-slider'  # Noch im CSS anpassen (To Do)
            )
        ], width=2)
    ]),

    # Haupt-Grafik + Zusammenfassung
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='zeitliche-entwicklung-straftaten'),
            width=8
        ),
        dbc.Col([
            html.H4("Zusammenfassung"),
            html.P("Mehrfach gemeldete Straftaten werden entsprechend gekennzeichnet."),
            html.H2("16'349", style={'marginTop': 10}),
            html.P("Straftaten 2024")
        ], width=4, style={'marginTop': 20})
    ]),

    # Tabelle + weitere Visualisierungen
    dbc.Row([


        dbc.Col(
            dcc.Graph(id='zeitliche-entwicklung-taeter-opfer'),
            width=8
        ),

        dbc.Col([
            html.H4("Zusätzliche Informationen"),
            html.P("Mehrfach gemeldete Straftaten..."),
            dbc.Row([
                dbc.Col([
                    html.H2("16'349"),
                    html.P("Opfer 2024")
                ]),
                dbc.Col([
                    html.H2("5'671"),
                    html.P("Täter")
                ])
            ])
        ], width=4)
    ]),

    # Fußnote
    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009–2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])


# Hier registrieren wir die Callbacks für diesen Tab
def register_callbacks(app):
    @app.callback(
        Output('zeitliche-entwicklung-straftaten', 'figure'),
        [Input('zeitliche-entwicklung-straftaten', 'id'),
         Input('jahr-slider-tab1', 'value')]
    )
    def update_zeitliche_entwicklung_straftaten(_, jahr_bereich):
        jahr_start, jahr_ende = jahr_bereich

        # Daten nach Zeitraum filtern
        opfer_gefiltert = opfer_total[(opfer_total['Jahr'] >= jahr_start) & (opfer_total['Jahr'] <= jahr_ende)]

        # Opfer über Zeit Visualisierung erstellen
        # Erstelle die Grafik
        fig = go.Figure()

        # bar für Straftaten total


        fig.add_trace(go.Bar(
            x=opfer_total['Jahr'],
            y=opfer_total['Straftaten_Total'],
            name='Straftaten Total',
            width=0.8,
            marker_color=color_all,
        marker = dict(
            color=color_all,  # Hintergrundfarbe
            pattern=dict(
                shape="x",  # Musterform
                fgcolor='white',  # Musterfarbe
                size=20,
                solidity=0.05,
                fgopacity=0.4
            )
        )
        ))

        fig.add_trace(go.Bar(
            x=opfer_total['Jahr'],
            y=opfer_total['davon_mehrfach'],
            name='Davon mehrfach Total',
            width=0.8,

            marker=dict(
                color=color_all,  # Hintergrundfarbe
                pattern=dict(
                    shape="x",  # Musterform
                    fgcolor='white',  # Musterfarbe
                    size=20,
                    solidity=0.2,
                    fgopacity=1
                )
            )
        ))




        # Layout anpassen
        fig.update_layout(
            barmode='overlay',
            title='Anzahl Registrierter Straftaten',
            xaxis_title='Jahr',
            yaxis_title='Anzahl Straftaten',
            template='plotly_white',
            bargap=0.5,
            xaxis = dict(
                range=[jahr_start - 0.5, jahr_ende + 0.5],
                tickmode='linear',
                dtick=1  # Jährliche Ticks
            ),
        )

        return fig

    # Grafik Zeitliche Entwilcung Opfer
    @app.callback(
        Output('zeitliche-entwicklung-taeter-opfer', 'figure'),
        [Input('zeitliche-entwicklung-taeter-opfer', 'id'),
         Input('jahr-slider-tab1', 'value')]
    )

    def update_zeitliche_entwicklung(_, jahr_bereich):
        jahr_start, jahr_ende = jahr_bereich

        # Daten nach Zeitraum filtern
        opfer_gefiltert = opfer_total[(opfer_total['Jahr'] >= jahr_start) & (opfer_total['Jahr'] <= jahr_ende)]
        taeter_gefiltert = taeter_total[(taeter_total['Jahr'] >= jahr_start) & (taeter_total['Jahr'] <= jahr_ende)]



        # Visualisierung erstellen
        # Erstelle die Figur
        fig = go.Figure()


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



        # Layout anpassen
        fig.update_layout(
            template='plotly_white',
            hovermode='x unified',
            xaxis=dict(
                range=[jahr_start-0.2, jahr_ende+0.2],
                tickmode='linear',
                dtick=1  # Jährliche Ticks
            ),

            yaxis=dict(range=[0, 12000]),
            legend_title='Geschlecht'
        )

        # Layout anpassen
        fig.update_layout(
            title=f"Zeitliche Entwicklung von Opfern und Tätern ({jahr_start}-{jahr_ende})",
            xaxis_title="Jahr",
            yaxis_title="Anzahl Personen",
            legend_title="Gruppe",
            template="plotly_white",
            hovermode="x unified"
        )

        return fig


    # Callback für die Anzeige des ausgewählten Zeitraums
    @app.callback(
        Output('zeitraum-info-tab1', 'children'),
        [Input('jahr-slider-tab1', 'value')]
    )
    def update_zeitraum_info_tab1(jahr_bereich):
        jahr_start, jahr_ende = jahr_bereich
        if jahr_start == jahr_ende:
            return f"Ausgewähltes Jahr: {jahr_start}"
        else:
            return f"Ausgewählter Zeitraum: {jahr_start} - {jahr_ende}"
