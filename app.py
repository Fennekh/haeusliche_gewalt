import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from layouts import tab_zeitliche_layout, tab_geschlecht_layout, tab_trend_layout

# Dash-Instanz
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                suppress_callback_exceptions=True)
server = app.server

# Layout mit Tabs
app.layout = html.Div([
    html.H1("Statistik zu häuslicher Gewalt in der Schweiz",
            style={'textAlign': 'center', 'color': '#505050', 'marginTop': 20, 'marginBottom': 20}),
            
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='Zeitliche Entwicklung', value='tab1'),
        dcc.Tab(label='Geschlechterverhältnis', value='tab2'),
        dcc.Tab(label='Trend-Analyse', value='tab3'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'), Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab1':
        return tab_zeitliche_layout.layout
    elif tab == 'tab2':
        return tab_geschlecht_layout.layout
    elif tab == 'tab3':
        return tab_trend_layout.layout

# Registriere die Callbacks aus allen Layout-Modulen
tab_zeitliche_layout.register_callbacks(app)
tab_geschlecht_layout.register_callbacks(app)
tab_trend_layout.register_callbacks(app)

# Starte die App
if __name__ == '__main__':
    app.run(debug=True)
