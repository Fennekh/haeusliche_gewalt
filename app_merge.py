import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Beispiel-Daten
bar_data = pd.DataFrame({
    'Altersgruppe': ['<18', '18-25', '26-35', '36-50', '51+'],
    'Fälle': [50, 120, 180, 140, 60]
})

spider_data_1 = {
    'Kategorie': ['Physisch', 'Psychisch', 'Sexuell', 'Finanziell', 'Sozial'],
    'Ausprägung': [80, 60, 40, 30, 50]
}

spider_data_2 = {
    'Kategorie': ['Partner', 'Ex-Partner', 'Eltern', 'Bekannte', 'Unbekannt'],
    'Ausprägung': [100, 70, 50, 30, 20]
}

# Bar chart
bar_chart = px.bar(
    bar_data,
    x='Fälle', y='Altersgruppe',
    orientation='h',
    title='Fälle nach Altersgruppe'
)

# Spider chart 1
spider_chart_1 = go.Figure()
spider_chart_1.add_trace(go.Scatterpolar(
    r=spider_data_1['Ausprägung'],
    theta=spider_data_1['Kategorie'],
    fill='toself',
    name='Formen der Gewalt'
))
spider_chart_1.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                             showlegend=False,
                             title="Formen häuslicher Gewalt")

# Spider chart 2
spider_chart_2 = go.Figure()
spider_chart_2.add_trace(go.Scatterpolar(
    r=spider_data_2['Ausprägung'],
    theta=spider_data_2['Kategorie'],
    fill='toself',
    name='Täterprofil'
))
spider_chart_2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                             showlegend=False,
                             title="Beziehung zum Täter")

# Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4("Bericht zur häuslichen Gewalt", className="mb-3"),
                html.P("Diese Übersicht zeigt verschiedene Aspekte häuslicher Gewalt in Deutschland anhand von fiktiven Daten.")
            ], className="p-3 bg-light rounded"),

            dcc.Graph(figure=bar_chart)
        ], width=3),

        dbc.Col([
            dbc.Row([
                dbc.Col(dcc.Graph(figure=spider_chart_1), width=6),
                dbc.Col(dcc.Graph(figure=spider_chart_2), width=6),
            ])
        ], width=9)
    ])
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)
