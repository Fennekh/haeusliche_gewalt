import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
# Tab-Callback

from dash.dependencies import Input, Output

from layouts import tab_detail_layout, tab_overview_layout  # deine beiden Tabs

# Dash-Instanz
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# Layout mit Tabs
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='Übersicht', value='tab1'),
        dcc.Tab(label='Weitere Analyse', value='tab2'),
    ]),
    html.Div(id='tabs-content')
])


@app.callback(Output('tabs-content', 'children'), Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab1':
        return tab_detail_layout.layout
    elif tab == 'tab2':
        return tab_overview_layout.layout

# Starte die App
if __name__ == '__main__':
    app.run(debug=True)
