from app import app
from dash.dependencies import Input, Output
import components.spider_taeter as spider_taeter

@app.callback(
    Output('output-id', 'children'),
    Input('input-id', 'value')
)
def update_output(value):
    return f"Du hast {value} gewählt"


