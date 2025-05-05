from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Excel-Datei laden
xls_taeter = pd.ExcelFile("data/beschuldigte.xlsx")
xls_opfer = pd.ExcelFile("data/geschaedigte.xlsx")
delikte = pd.read_csv("data/delikte.csv")

print(delikte)
# Dictionary: Sheetname → DataFrame
dfs = {sheet: pd.read_excel(xls_taeter, sheet_name=sheet, header=5) for sheet in xls_taeter.sheet_names}
#
dfs_opfer = {sheet: pd.read_excel(xls_opfer, sheet_name=sheet, header=5) for sheet in xls_opfer.sheet_names}

# Dash App
app = Dash(__name__)



# Funktion zum Erzeugen eines kleinen Polar-Charts nach deinen Vorgaben
def generate_custom_polar_chart(index, values):
    angles = [45,135, 215, 305]

    # werte aus df rauslesen
    values = values.iloc[:, index].values

    # Farben: [Täter-Mann, Täter-Frau, Opfer-Mann, Opfer-Frau]
    colors = ['blue', 'red','red', 'blue']
    names = ['Täter (M)', 'Täter (F)', 'Opfer (M)', 'Opfer (F)']

    traces = []
    for i in range(4):
        traces.append(go.Barpolar(
            r=[values[i]],
            theta=[angles[i]],
            name=names[i],
            marker_color=colors[i],
            opacity=0.9
        ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        polar=dict(

            angularaxis=dict(
                showticklabels=False,
                ticks='',
                rotation=90,
                direction="clockwise"
            ),
            #radialaxis=dict(range=[0, 4003], ticks='outside'),
        )
    )
    return fig
# Values für Polarchart
steps = 11
delikte_df = pd.DataFrame()
for delikt_nr in range(len(delikte)+1):
    row1 = 1 + delikt_nr * steps
    row6 = 6 + delikt_nr * steps
    col = 6  # Spalte 7 → Index 6

    # Werte für Täter und Opfer extrahieren
    taeter_wert_m = dfs["2024"].iloc[row1, col]
    taeter_wert_w = dfs["2024"].iloc[row6, col]
    opfer_wert_m = dfs_opfer["2024"].iloc[row1, col]
    opfer_wert_w = dfs_opfer["2024"].iloc[row6, col]
    delikt_name = delikte.iloc[delikt_nr-1,0]
    # Neue Spalte mit genau 2 Werten (oben Täter, unten Opfer)
    spalte = pd.Series([taeter_wert_m,taeter_wert_w,opfer_wert_w,opfer_wert_m], name=delikt_name)

    # An delikte_df anhängen
    delikte_df = pd.concat([delikte_df, spalte], axis=1)

print(delikte_df)

# Chart-Gitter erzeugen mit 30 Charts
polar_chart_grid = html.Div(
    children=[
        html.Div([
            dcc.Graph(figure=generate_custom_polar_chart(i,delikte_df),
                      config={'displayModeBar': False},
                      style={'height': '200px'}),
            html.Div(f"{delikte.iloc[i-1,0]}", style={'textAlign': 'center', 'marginTop': '5px', 'fontSize': '14px'})
        ], style={'width': '16%', 'display': 'inline-block', 'padding': '10px'})
        for i in range(30)
    ],
    style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'}
)


# Layout der App
app.layout = html.Div([
    # Graph für die Frauen
    dcc.Graph(id='barpolar-graph-females'),

    # Graph für die Männer
    dcc.Graph(id='barpolar-graph-males'),

    # Slider für die Jahre 2009 bis 2024 (immer nur ein Jahr auswählbar)
    dcc.Slider(
        id='year-slider',
        min=2009,
        max=2024,
        step=1,
        value=2020,  # Standardwert ist 2020
        marks={year: str(year) for year in range(2009, 2025)},
    ),

    html.Hr(),
    html.H3("Delikte Übersicht (Dummy-Daten)", style={'textAlign': 'center'}),
    polar_chart_grid
])


# Callback, um das Diagramm für die Männer basierend auf dem gewählten Jahr zu aktualisieren
@app.callback(
    Output('barpolar-graph-males', 'figure'),
    [Input('year-slider', 'value')]
)
def update_male_figure(selected_year):
    # Lade das DataFrame für das ausgewählte Jahr
    age_data = dfs[str(selected_year)].iloc[:, 7:19]

    # Kombiniere die Altersgruppen für die gewünschte Visualisierung
    age_data['10 - 19 Jahre'] = age_data['10 - 14 Jahre'] + age_data['15 - 17 Jahre'] + age_data['18 - 19 Jahre']
    age_data['20 - 29 Jahre'] = age_data['20 - 24 Jahre'] + age_data['25 - 29 Jahre']
    age_data['30 - 39 Jahre'] = age_data['30 - 34 Jahre'] + age_data['35 - 39 Jahre']

    # Entferne die gemergeden Zeilen
    age_data = age_data.drop(
        columns=['10 - 14 Jahre', '15 - 17 Jahre', '18 - 19 Jahre', '20 - 24 Jahre', '25 - 29 Jahre', '30 - 34 Jahre',
                 '35 - 39 Jahre'])

    # Neue Reihenfolge der Altersklassen
    new_order = ['<10 Jahre', '10 - 19 Jahre', '20 - 29 Jahre', '30 - 39 Jahre',
                 '40 - 49 Jahre', '50 - 59 Jahre', '60 - 69 Jahre', '70 Jahre und +']
    age_data = age_data[new_order]

    # Nur Männer (Daten für Männer befinden sich in Zeilen 2 bis 5)
    age_data_m = age_data.iloc[2:6, :]

    partnerschaft_m = age_data_m.iloc[0].values
    ehem_partner_m = age_data_m.iloc[1].values
    eltern_kind_m = age_data_m.iloc[2].values
    andere_m = age_data_m.iloc[3].values

    # Erstelle das Diagramm für Männer
    fig_males = go.Figure()

    fig_males.add_trace(go.Barpolar(
        r=partnerschaft_m[::-1],  # Umkehrung der Werte für Partnerschaft (Männer)
        name='Partnerschaft (Männer)',
        marker_color='rgb(106,81,163)'
    ))
    fig_males.add_trace(go.Barpolar(
        r=ehem_partner_m[::-1],  # Umkehrung der Werte für ehem_partner (Männer)
        name='Ehem. Partner (Männer)',
        marker_color='rgb(158,154,200)'
    ))
    fig_males.add_trace(go.Barpolar(
        r=eltern_kind_m[::-1],  # Umkehrung der Werte für eltern_kind (Männer)
        name='Eltern-Kind (Männer)',
        marker_color='rgb(203,201,226)'
    ))
    fig_males.add_trace(go.Barpolar(
        r=andere_m[::-1],  # Umkehrung der Werte für andere (Männer)
        name='Andere (Männer)',
        marker_color='rgb(242,240,247)'
    ))

    # Layout für das Männer-Diagramm
    fig_males.update_layout(
        title=dict(text=f'Straftaten Häusliche Gewalt Männer ({selected_year})'),
        font_size=16,
        legend_font_size=16,
        polar_radialaxis_ticksuffix='',  # Entfernen der Prozentzeichen
        polar_angularaxis_rotation=90,
        polar_angularaxis=dict(
            tickmode='array',
            tickvals=[i * (360 / 8) for i in range(8)],  # Berechnung der tickvals im Uhrzeigersinn
            ticktext=['70 Jahre und +', '60 - 69 Jahre', '50 - 59 Jahre', '40 - 49 Jahre', '30 - 39 Jahre',
                      '20 - 29 Jahre', '10 - 19 Jahre', '<10 Jahre'],  # Altersklassen umgekehrt
            tickangle=0,  # Winkel der Beschriftungen, damit sie sich nicht überlappen
            showticksuffix='last',  # Zeigt den Suffix (Altersgruppen) nur an der letzten Achse
            tickfont=dict(size=12),  # Schriftgröße der Altersklassen
        ),
        polar=dict(
            radialaxis=dict(showticksuffix='last'),  # Radiale Achse ohne Prozentzeichen
        )
    )

    return fig_males


# Callback, um das Diagramm für die Frauen basierend auf dem gewählten Jahr zu aktualisieren
@app.callback(
    Output('barpolar-graph-females', 'figure'),
    [Input('year-slider', 'value')]
)
def update_female_figure(selected_year):
    # Lade das DataFrame für das ausgewählte Jahr
    age_data = dfs[str(selected_year)].iloc[:, 7:19]

    # Kombiniere die Altersgruppen für die gewünschte Visualisierung
    age_data['10 - 19 Jahre'] = age_data['10 - 14 Jahre'] + age_data['15 - 17 Jahre'] + age_data['18 - 19 Jahre']
    age_data['20 - 29 Jahre'] = age_data['20 - 24 Jahre'] + age_data['25 - 29 Jahre']
    age_data['30 - 39 Jahre'] = age_data['30 - 34 Jahre'] + age_data['35 - 39 Jahre']

    # Entferne die gemergeden Zeilen
    age_data = age_data.drop(
        columns=['10 - 14 Jahre', '15 - 17 Jahre', '18 - 19 Jahre', '20 - 24 Jahre', '25 - 29 Jahre', '30 - 34 Jahre',
                 '35 - 39 Jahre'])

    # Neue Reihenfolge der Altersklassen
    new_order = ['<10 Jahre', '10 - 19 Jahre', '20 - 29 Jahre', '30 - 39 Jahre',
                 '40 - 49 Jahre', '50 - 59 Jahre', '60 - 69 Jahre', '70 Jahre und +']
    age_data = age_data[new_order]

    # Nur Frauen (Daten für Frauen befinden sich in Zeilen 8 bis 11)
    age_data_f = age_data.iloc[8:12, :]

    partnerschaft_f = age_data_f.iloc[0].values
    ehem_partner_f = age_data_f.iloc[1].values
    eltern_kind_f = age_data_f.iloc[2].values
    andere_f = age_data_f.iloc[3].values

    # Erstelle das Diagramm für Frauen
    fig_females = go.Figure()

    fig_females.add_trace(go.Barpolar(
        r=partnerschaft_f[::-1],  # Umkehrung der Werte für Partnerschaft (Frauen)
        name='Partnerschaft (Frauen)',
        marker_color='rgb(106,81,163)'
    ))
    fig_females.add_trace(go.Barpolar(
        r=ehem_partner_f[::-1],  # Umkehrung der Werte für ehem_partner (Frauen)
        name='Ehem. Partner (Frauen)',
        marker_color='rgb(158,154,200)'
    ))
    fig_females.add_trace(go.Barpolar(
        r=eltern_kind_f[::-1],  # Umkehrung der Werte für eltern_kind (Frauen)
        name='Eltern-Kind (Frauen)',
        marker_color='rgb(203,201,226)'
    ))
    fig_females.add_trace(go.Barpolar(
        r=andere_f[::-1],  # Umkehrung der Werte für andere (Frauen)
        name='Andere (Frauen)',
        marker_color='rgb(242,240,247)'
    ))

    # Layout für das Frauen-Diagramm
    fig_females.update_layout(
        title=dict(text=f'Straftaten Häusliche Gewalt Frauen ({selected_year})'),
        font_size=16,
        legend_font_size=16,
        polar_radialaxis_ticksuffix='',  # Entfernen der Prozentzeichen
        polar_angularaxis_rotation=90,
        polar_angularaxis=dict(
            tickmode='array',
            tickvals=[i * (360 / 8) for i in range(8)],  # Berechnung der tickvals im Uhrzeigersinn
            ticktext=['70 Jahre und +', '60 - 69 Jahre', '50 - 59 Jahre', '40 - 49 Jahre', '30 - 39 Jahre',
                      '20 - 29 Jahre', '10 - 19 Jahre', '<10 Jahre'],  # Altersklassen umgekehrt
            tickangle=0,  # Winkel der Beschriftungen, damit sie sich nicht überlappen
            showticksuffix='last',  # Zeigt den Suffix (Altersgruppen) nur an der letzten Achse
            tickfont=dict(size=12),  # Schriftgröße der Altersklassen
        ),
        polar=dict(
            radialaxis=dict(showticksuffix='last'),  # Radiale Achse ohne Prozentzeichen
        )
    )

    return fig_females





# App ausführen
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
