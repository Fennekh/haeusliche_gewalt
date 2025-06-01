import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from layouts import tab_zeitliche_entwicklung, tab_geschlechterverhaeltnis, tab_altersverteilung, tab_beziehungen, tab_uebersicht_delikte, tab_impressum
import plotly.io as pio
import plotly.graph_objects as go

# Roboto-Template definieren
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



# Dash-Instanz
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True, title='Statistik Häusliche Gewalt')
server = app.server

# Layout mit Tabs
app.layout = html.Div([
    html.H5("Statistik zu Häuslicher Gewalt in der Schweiz 2009-2024",
            style={'textAlign': 'left', 'color': 'black', 'fontWeight': 'regular', 'marginTop': 20, 'marginBottom': 20, 'marginLeft': 20}),

    dcc.Tabs(id="tabs", value='tab1',
             className="tab-container", children=[
        dcc.Tab(label='Übersicht einzelne Delikte', value='tab1'),
        dcc.Tab(label='Entwicklung Gesamt', value='tab2'),
        dcc.Tab(label='Entwicklung Geschlechterverhältnis', value='tab3'),
        dcc.Tab(label='Beziehungen', value='tab4'),
        dcc.Tab(label='Entwicklung Altersverteilung', value='tab5'),
        dcc.Tab(label='Impressum', value='tab6'),

    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'), Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab1':
        return tab_uebersicht_delikte.layout
    elif tab == 'tab2':
        return tab_zeitliche_entwicklung.layout
    elif tab == 'tab3':
        return tab_geschlechterverhaeltnis.layout
    elif tab == 'tab4':
        return tab_altersverteilung.layout
    elif tab == 'tab5':
        return tab_beziehungen.layout
    elif tab == 'tab6':
        return tab_impressum.layout

# Registriere die Callbacks aus allen Layout-Modulen
tab_uebersicht_delikte.register_callbacks(app)
tab_zeitliche_entwicklung.register_callbacks(app)
tab_geschlechterverhaeltnis.register_callbacks(app)
tab_altersverteilung.register_callbacks(app)
tab_beziehungen.register_callbacks(app)
tab_impressum.register_callbacks(app)



# Starte die App
if __name__ == '__main__':
    app.run(debug=False)
