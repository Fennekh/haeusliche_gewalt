import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.io as pio
plotly_font = dict(
    family="Arimo, sans-serif",
    size=14,
    color="black"
)
pio.templates["arimo"] = go.layout.Template(layout=dict(font=plotly_font))
pio.templates.default = "arimo"

# --- Farben und Template ---
color_women = "#cb4d1d"
color_men = "#4992b2"
color_all = "black"


# --- Daten einlesen und vorbereiten ---
opfer = pd.read_csv("data/geschaedigte_tidy.csv")
taeter = pd.read_csv("data/beschuldigte_tidy.csv")

opfer = opfer[(opfer["Delikt"] == "Total Häusliche Gewalt") & (opfer["Beziehungsart"] == "Alle")]
taeter = taeter[(taeter["Delikt"] == "Total Häusliche Gewalt") & (taeter["Beziehungsart"] == "Alle")]

age_order = ['<10 Jahre', '10 - 19 Jahre', '20 - 29 Jahre', '30 - 39 Jahre',
             '40 - 49 Jahre', '50 - 59 Jahre', '60 - 69 Jahre', '70 Jahre und +']

for df in [opfer, taeter]:
    for col in age_order:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

# --- Layout ---
layout = html.Div([
    html.Div([
        html.H2("Wie ist die Altersverteilung über Täter:Innen und Opfer", style={'textAlign': 'left', 'marginLeft': 40, 'paddingBottom': 0, 'marginTop': 48,  'fontWeight': 600 }),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Dropdown(
                        id='gender-selector-trend',
                        options=[
                            {'label': 'Männlich', 'value': 'männlich'},
                            {'label': 'Weiblich', 'value': 'weiblich'},
                            {'label': 'Alle Geschlechter', 'value': 'Total'}
                        ],
                        value='Total',
                        style={'width': '200px', 'marginLeft': '20px'}
                    ),
                    dcc.RadioItems(
                        id='trend-selector',
                        options=[
                            {'label': 'Opfer', 'value': 'opfer'},
                            {'label': 'Täter:innen', 'value': 'taeter'}
                        ],
                        value='opfer',
                        labelStyle={'display': 'inline-block', 'marginLeft': '20px'}
                    ),
                ], style={'display': 'flex', 'gap': '10px', 'marginTop': '20px', 'marginBottom': '16px'}),
                dcc.Graph(id='altersgruppen-trend', style={'height': '65vh', 'marginLeft': '40px'})
            ], width=8),

            dbc.Col([
                dcc.Graph(id='alterspyramide', style={'height': '70vh','marginTop': '40px'})
            ], width=4)
        ], style={'marginTop': '36px'})
    ]),
    html.Hr(),
    html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009–2024)",
           style={'textAlign': 'left', 'fontStyle': 'italic', 'fontSize': 14, 'color': '#888'})
])

# --- Callbacks ---
def register_callbacks(app):
    @app.callback(
        Output('altersgruppen-trend', 'figure'),
        [Input('trend-selector', 'value'),
         Input('gender-selector-trend', 'value')]
    )
    def update_altersgruppen_trend(perspektive, geschlecht):
        jahr_start = 2009
        jahr_ende = 2024
        df = opfer if perspektive == 'opfer' else taeter
        df['Jahr'] = pd.to_numeric(df['Jahr'], errors='coerce')

        df_filtered = df[
            (df['Geschlecht'] == geschlecht) &
            (df['Jahr'] >= jahr_start) &
            (df['Jahr'] <= jahr_ende)
            ]

        # Linienfarbe nach Geschlecht
        if geschlecht == 'männlich':
            linienfarbe = color_men
        elif geschlecht == 'weiblich':
            linienfarbe = color_women
        else:
            linienfarbe = color_all

        fig = go.Figure()

        for altersklasse in age_order:
            if altersklasse in df_filtered.columns:
                x_vals = df_filtered['Jahr']
                y_vals = df_filtered[altersklasse]

                fig.add_trace(go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode='lines+markers',
                    name=str(altersklasse),
                    line=dict(color=linienfarbe),
                    showlegend=False,  # keine Legende
                    hoverlabel=dict(font=dict(size=12)),
                    hovertemplate=f'%{{y:.0f}} Personen<br>{altersklasse}<br>%{{x}}<extra></extra>'
                ))

                # Letzten Punkt beschriften
                if len(x_vals) > 0 and len(y_vals) > 0:
                    fig.add_annotation(
                        x=x_vals.iloc[-1],
                        y=y_vals.iloc[-1],
                        text=str(altersklasse),
                        showarrow=False,
                        xanchor="left",
                        yanchor="middle",
                        xshift=4,
                        font=dict(color=linienfarbe),
                    )

        fig.update_layout(
            title=f"Entwicklung der Altersgruppen bei {geschlecht.lower()} {'Opfer' if perspektive == 'opfer' else 'Täter:innen'} ({jahr_start}-{jahr_ende})",
            xaxis_title="Jahr",
            yaxis_title="Anzahl Personen",
            font_family="Arimo, sans-serif",
            font_size=14,
            yaxis=dict(range=[0, 4000]),
            xaxis=dict(range=[2009, 2026]),
            showlegend=False,
            template="plotly_white",
            hoverlabel=dict(bgcolor="white", font_size=14),
            margin=dict(t=40, b=40, l=60, r=30)
        )

        return fig

    @app.callback(
        Output('alterspyramide', 'figure'),
        [Input('altersgruppen-trend', 'clickData'),
         Input('trend-selector', 'value'),
        Input('gender-selector-trend', 'value')]
    )
    def update_alterspyramide(clickData, perspektive,geschlecht):
        if clickData is None:
            return go.Figure(layout=go.Layout(
                xaxis={"visible": False},
                yaxis={"visible": False},
                shapes=[dict(
                    type="path",
                    path=("M 0.02 1.0 L 0.98 1.0 Q 1.0 1.0 1.0 0.98 L 1.0 0.12 "
                          "Q 1.0 0.1 0.98 0.1 L 0.02 0.1 Q 0.0 0.1 0.0 0.12 "
                          "L 0.0 0.98 Q 0.0 1.0 0.02 1.0 Z"),
                    xref="paper", yref="paper",
                    line=dict(color="lightgrey", width=1),
                    fillcolor="white", layer="below"
                )],
                annotations=[dict(
                    text="← Klicke auf <br>einen Datenpunkt <br>auf dem Linienchart <br>um mehr über <br>ein Jahr zu erfahren",
                    xref="paper", yref="paper",
                    x=0.5, y=0.875,
                    showarrow=False,
                    font=dict(size=30, color="lightgrey"),
                    align="center"
                )]
            ))

        try:
            jahr = int(clickData['points'][0]['x'])
        except Exception:
            raise PreventUpdate

        df = opfer if perspektive == 'opfer' else taeter
        df_year = df[df['Jahr'] == jahr]

        fig = go.Figure()

        if geschlecht in ['weiblich', 'Total']:
            df_weiblich = df_year[df_year['Geschlecht'] == 'weiblich']
            x_women = [-df_weiblich[g].values[0] if g in df_weiblich else 0 for g in age_order]
            fig.add_trace(go.Bar(
                y=age_order,
                x=x_women,
                orientation='h',
                name='Weiblich',
                marker_color=color_women
            ))

        if geschlecht in ['männlich', 'Total']:
            df_maennlich = df_year[df_year['Geschlecht'] == 'männlich']
            x_men = [df_maennlich[g].values[0] if g in df_maennlich else 0 for g in age_order]
            fig.add_trace(go.Bar(
                y=age_order,
                x=x_men,
                orientation='h',
                name='Männlich',
                marker_color=color_men
            ))

        fig.update_layout(
            title=f"Anzahl {'Opfer' if perspektive == 'opfer' else 'Täter:innen'} nach Alter und Geschlecht ({jahr})",
            barmode='relative',
            font_family="Arimo, sans-serif",
            font_size=14,
            xaxis=dict(
                tickvals=[-2500, -1500, -500, 0, 500, 1500, 2500],
                ticktext=[2500, 1500, 500, 0, 500, 1500, 2500],
                range=[-2700, 2700]
            ),
            yaxis=dict(categoryorder='array', categoryarray=age_order),
            template='plotly_white',
            bargap=0.1,
            showlegend=True,
            legend=dict(
                title=f"{'Opfer' if perspektive == 'opfer' else 'Täter:innen'}",
                x=0.98,
                y=0.98,
                xanchor='right',
                yanchor='top',
                bgcolor='rgba(255,255,255,0.5)',  # halbtransparenter Hintergrund
                bordercolor='lightgrey',
                borderwidth=1,
                font=dict(color='black',family='Arimo', ),
            )
        )

        return fig
