import dash
from dash import html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import io
import base64

app = dash.Dash(__name__)

# Jahresliste
years = list(range(2009, 2025))

# Simulierte Daten
num_rows = 5
data = {
    'Name': [f'Delikt {i}' for i in range(1, num_rows + 1)],
    'Werte': [np.random.randint(50, 150, size=len(years)).tolist() for _ in range(num_rows)],
    'Frauen_2024': [np.random.randint(20, 80) for _ in range(num_rows)],
}
df = pd.DataFrame(data)
df['Maenner_2024'] = 100 - df['Frauen_2024']

# Funktion: Plot zu Bild
def fig_to_base64(fig):
    buffer = io.BytesIO()
    fig.write_image(buffer, format='png', width=100, height=40)
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"

# Tabellenkopf
table_rows = [html.Tr([
    html.Th("Name", style={'textAlign': 'left', 'width': '150px'}),
    html.Th("Delikte 2024", style={'textAlign': 'right', 'width': '70px'}),
    html.Th("Trend", style={'textAlign': 'left', 'width': '110px'}),
    html.Th("Δ (%)", style={'textAlign': 'left', 'width': '70px'}),
    html.Th("Geschlechterverteilung 2024", style={'textAlign': 'left', 'width': '120px'}),
    html.Th("", style={'textAlign': 'left', 'width': '80px'}),
])]

# Tabellenzeilen
for _, row in df.iterrows():
    werte = row['Werte']
    wert_2024 = werte[-1]
    start, end = werte[0], werte[-1]
    delta_percent = ((end - start) / start) * 100
    arrow = "▲" if delta_percent >= 0 else "▼"
    delta_str = f"{arrow} {abs(delta_percent):.1f}%"

    # Trendgrafik
    fig = go.Figure(
        data=[go.Scatter(x=years, y=werte, mode='lines', line=dict(color='steelblue'))],
        layout=go.Layout(
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=40,
            width=100,
        )
    )
    img_src = fig_to_base64(fig)

    # Geschlechterverteilung
    frauen = row['Frauen_2024']
    maenner = 100 - frauen
    gender_bar = html.Div([
        html.Div(title=f"{frauen}% Frauen", style={
            'display': 'inline-block',
            'width': f'{frauen}%',
            'height': '12px',
            'backgroundColor': '#e74c3c',
        }),
        html.Div(title=f"{maenner}% Männer", style={
            'display': 'inline-block',
            'width': f'{maenner}%',
            'height': '12px',
            'backgroundColor': '#3498db',
        }),
    ], style={
        'width': '100px',
        'border': '1px solid #ccc',
        'textAlign': 'left'
    })

    # Tabellenzeile
    table_rows.append(html.Tr([
        html.Td(row['Name'], style={'textAlign': 'left'}),
        html.Td(f"{wert_2024}", style={'textAlign': 'right'}),
        html.Td(html.Img(src=img_src, style={'height': '35px'})),
        html.Td(delta_str, style={'textAlign': 'left'}),
        html.Td(gender_bar),
        html.Td("Details →", style={'color': '#555', 'fontStyle': 'italic'})
    ]))

# Layout
app.layout = html.Div([
    html.H4("Delikte mit Zeitverlauf, aktuellem Stand und Geschlechterverteilung", style={'textAlign': 'left'}),
    html.Table(
        table_rows,
        style={
            'borderCollapse': 'collapse',
            'width': '100%',
            'fontSize': '12px',
            'tableLayout': 'fixed'
        }
    )
])

if __name__ == '__main__':
    app.run(debug=True)
