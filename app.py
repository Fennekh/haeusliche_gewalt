import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from layouts import tab_zeitliche_entwicklung, tab_geschlechterverhaeltnis, tab_trend_analyse, tab_beziehungen, tab_uebersicht

# Dash-Instanz
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)
server = app.server

# Layout mit Tabs
app.layout = html.Div([
    html.H1("Statistik zu häuslicher Gewalt in der Schweiz",
            style={'textAlign': 'left', 'color': '#505050', 'marginTop': 20, 'marginBottom': 20, 'marginleft': 20}),

    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='Gesammt', value='tab1'),
        dcc.Tab(label='Geschlechterverhältnis', value='tab2'),
        dcc.Tab(label='Altersverteilung', value='tab3'),
        dcc.Tab(label='Beziehungen', value='tab4'),
        dcc.Tab(label='Übersicht', value='tab5'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'), Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab1':
        return tab_zeitliche_entwicklung.layout
    elif tab == 'tab2':
        return tab_geschlechterverhaeltnis.layout
    elif tab == 'tab3':
        return tab_trend_analyse.layout
    elif tab == 'tab4':
        return tab_beziehungen.layout
    elif tab == 'tab5':
        return tab_uebersicht.layout

# Registriere die Callbacks aus allen Layout-Modulen
tab_zeitliche_entwicklung.register_callbacks(app)
tab_geschlechterverhaeltnis.register_callbacks(app)
tab_trend_analyse.register_callbacks(app)
tab_beziehungen.register_callbacks(app)
tab_uebersicht.register_callbacks(app)


# Starte die App
if __name__ == '__main__':
    app.run(debug=True)
