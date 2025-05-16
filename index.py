from dash import dcc, html
from app import app
from layouts import tab_detail_layout, tab_overview_layout

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='Übersicht', value='tab1'),
        dcc.Tab(label='Weitere Analyse', value='tab2'),
    ]),
    html.Div(id='tabs-content')
])

# Callback zur Umschaltung der Tabs
from dash.dependencies import Input, Output
@app.callback(Output('tabs-content', 'children'), Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab1':
        return tab_detail_layout.layout
    elif tab == 'tab2':
        return tab_overview_layout.layout

if __name__ == '__main__':
    app.run_server(debug=True)