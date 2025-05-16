import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go




# CSV-Datei laden
df = pd.read_csv("/Users/karinhugentobler/PycharmProjects/dashboard_haeusliche_gewalt/data/geschaedigte_tidy.csv")

# Alterskategorien, die zusammengeführt werden sollen
age_columns_to_convert = [
    '10 - 14 Jahre', '15 - 17 Jahre', '17 - 19 Jahre',
    '20 - 24 Jahre', '25 - 29 Jahre',
    '30 - 34 Jahre', '35 - 39 Jahre'
]

# Alterskategorien, die unverändert bleiben
final_age_groups = [
    '<10 Jahre', '10 - 19 Jahre', '20 - 29 Jahre', '30 - 39 Jahre',
    '40 - 49 Jahre', '50 - 59 Jahre', '60 - 69 Jahre', '70 Jahre und +'
]

age_order = ["<10 Jahre", "10 - 19 Jahre", "20 - 29 Jahre", "30 - 39 Jahre",
             "40 - 49 Jahre", "50 - 59 Jahre", "60 - 69 Jahre", "70 Jahre und +"]

print(df.iloc[0])

# Jahre und Delikte extrahieren
jahre = sorted(df["Jahr"].dropna().unique())
delikte = sorted(df["Delikt"].dropna().unique())

# Dash-App
app = dash.Dash(__name__)
server = app.server

# Layout
app.layout = html.Div([
    html.H2("Tatverdächtige nach Alterskategorie und Geschlecht", style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Label("Jahr:"),
            dcc.Slider(
                id="jahr-slider",
                min=min(jahre),
                max=max(jahre),
                value=max(jahre),
                marks={int(j): str(int(j)) for j in jahre},
                step=None
            )
        ], style={"width": "70%", "display": "inline-block", "padding": "0 20px"}),

        html.Div([
            html.Label("Delikt:"),
            dcc.Dropdown(
                id="delikt-dropdown",
                options=[{"label": d, "value": d} for d in delikte],
                value="Total Häusliche Gewalt",
                clearable=False
            )
        ], style={"width": "28%", "display": "inline-block", "verticalAlign": "top"})
    ], style={"margin": "20px 10px"}),

    dcc.Graph(id="radial-plot")
])


# Callback mit Jahr + Delikt
@app.callback(
    Output("radial-plot", "figure"),
    [Input("jahr-slider", "value"),
     Input("delikt-dropdown", "value")]
)
def update_figure(selected_year, selected_delikt):
    df_filtered = df[
        (df['Jahr'] == selected_year) &
        (df['Delikt'] == selected_delikt) &
        (df['Beziehungsart'] == 'Alle') &
        (df['Geschlecht'].isin(['männlich', 'weiblich']))
    ]

    df_delikt = df[(df['Delikt'] == selected_delikt) &
                (df['Beziehungsart'] == 'Alle')
                       ]


    if df_filtered.empty:
        return go.Figure().update_layout(
            title=f"Keine Daten für {selected_year} – {selected_delikt} vorhanden"
        )

    maennlich_row = df_filtered[df_filtered['Geschlecht'] == 'männlich'].iloc[0]
    weiblich_row = df_filtered[df_filtered['Geschlecht'] == 'weiblich'].iloc[0]

    maennlich = pd.to_numeric(maennlich_row[age_order], errors="coerce").fillna(0)
    weiblich = pd.to_numeric(weiblich_row[age_order], errors="coerce").fillna(0)


    fig = go.Figure()



    fig.add_trace(go.Scatterpolar(
        r=maennlich.values,
        theta=final_age_groups,
        fill='toself',
        name='Männlich',
        line=dict(color="#2D5E89")
    ))

    fig.add_trace(go.Scatterpolar(
        r=weiblich.values,
        theta=final_age_groups,
        fill='toself',
        name='Weiblich',
        line=dict(color="#E63946")
    ))

    fig.update_layout(
        polar=dict(
            angularaxis=dict(
                direction="clockwise",  # oder "counterclockwise"
                rotation=90  # Startwinkel in Grad (z. B. 0 = rechter Rand, 90 = oben)
            ),
            radialaxis=dict(
                visible=True,
                range=[0, 3000]
            )
        ),
        showlegend=True,
        title=f"{selected_delikt} ({selected_year}) nach Alterskategorie und Geschlecht"
    )

    return fig


# App starten
if __name__ == "__main__":
    app.run(debug=True)
