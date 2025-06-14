import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import base64
import plotly.io as pio
from dash import ctx
plotly_font = dict(
    family="Arimo, sans-serif",
    size=14,
    color="black"
)
pio.templates["arimo"] = go.layout.Template(layout=dict(font=plotly_font))
pio.templates.default = "arimo"


# --- Farben ---
color_women = "#cb4d1d"
color_men = "#4992b2"
color_all = "black"

# --- Daten laden ---
opfer = pd.read_csv("data/geschaedigte_tidy.csv")
taeter = pd.read_csv("data/beschuldigte_tidy.csv")

# --- Altersgruppen ---
altersgruppen = [
    '<10 Jahre', '10 - 19 Jahre', '20 - 29 Jahre', '30 - 39 Jahre',
    '40 - 49 Jahre', '50 - 59 Jahre', '60 - 69 Jahre', '70 Jahre und +'
]

# --- Funktionen ---
def häufigstes_alter(df, alters_cols, label):
    top_info = {}
    df = df[df["Jahr"] == 2024].copy()

    for col in alters_cols:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    for delikt in df["Delikt"].unique():
        subset = df[df["Delikt"] == delikt]
        total = subset[alters_cols].sum().sum()

        if total > 0:
            max_count = 0
            top_ages = set()
            for _, row in subset.iterrows():
                for age in alters_cols:
                    count = row[age]
                    if count > max_count:
                        max_count = count
                        top_ages = {age}
                    elif count == max_count:
                        top_ages.add(age)
            if len(top_ages) > 1:
                top_age_label = "Mehrere"
            else:
                top_age_label = list(top_ages)[0]
        else:
            top_age_label = "–"
            max_count = 0

        top_info[delikt] = {
            f"Häufigstes Alter ({label})": top_age_label,
            f"Anzahl ({label})": max_count
        }

    return top_info


def häufigste_beziehung(df, jahr, label, wert_col):
    top_bez = {}
    gefiltert = df[(df["Jahr"] == jahr) & (df["Beziehungsart"] != "Alle")]

    for delikt in gefiltert["Delikt"].unique():
        delikt_df = gefiltert[gefiltert["Delikt"] == delikt]
        total = delikt_df[wert_col].sum()

        if total > 0:
            max_val = delikt_df[wert_col].max()
            top_rows = delikt_df[delikt_df[wert_col] == max_val]
            if len(top_rows) > 1:
                beziehungsart = "Mehrere"
            else:
                beziehungsart = top_rows.iloc[0]["Beziehungsart"]
        else:
            beziehungsart = "–"
            max_val = 0

        top_bez[delikt] = {
            f"Häufigste Beziehung ({label})": beziehungsart,
            f"Anzahl Beziehung ({label})": max_val
        }

    return top_bez




def geschlechter_balken_plotly(m, w):
    total = m + w

    if total == 0:
        # Weißer Balken bei fehlenden Daten
        fig = go.Figure(data=[
            go.Bar(
                x=[1],  # 100% weißer Balken
                y=[""],
                orientation='h',
                marker_color='white',
                marker_line=dict(color='lightgray', width=1),
                showlegend=False,
                hoverinfo='skip'
            )
        ])
    else:
        ratio_m = m / total
        ratio_w = w / total

        fig = go.Figure(data=[
            go.Bar(
                x=[ratio_w],
                y=[""],
                orientation='h',
                marker_color=color_women,
                showlegend=False,
                hoverinfo='skip'
            ),
            go.Bar(
                x=[ratio_m],
                y=[""],
                orientation='h',
                base=[ratio_w],
                marker_color=color_men,
                showlegend=False,
                hoverinfo='skip'
            ),
        ])


    fig.update_layout(
        barmode='stack',
        xaxis=dict(range=[0, 1], visible=False, fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True),
        margin=dict(l=0, r=0, t=0, b=0),
        height=24,
        width=200,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return base64.b64encode(fig.to_image(format='png')).decode('utf-8')



# --- Trenddaten ---
taeter_filtered = taeter[(taeter["Beziehungsart"] == "Alle") & (taeter["Geschlecht"] == "Total")]
trend_data = taeter_filtered[taeter_filtered["Jahr"].between(2009, 2024)]
trend_summary = []

jahre_voll = list(range(2009, 2025))  # <- fest definierter Bereich

for delikt in trend_data["Delikt"].unique():
    delikt_data = trend_data[trend_data["Delikt"] == delikt][["Jahr", "Straftaten_Total"]]
    delikt_data = delikt_data.set_index("Jahr").reindex(jahre_voll, fill_value=0).reset_index()

    jahre = delikt_data["Jahr"].tolist()
    werte = delikt_data["Straftaten_Total"].tolist()

    anzahl_2024 = delikt_data.loc[delikt_data["Jahr"] == 2024, "Straftaten_Total"].values[0]
    anzahl_2009 = delikt_data.loc[delikt_data["Jahr"] == 2009, "Straftaten_Total"].values[0]
    # Optional: Prozentveränderung beschränken, um extreme Zahlen zu vermeiden
    if anzahl_2009 == 0:
        if anzahl_2024 == 0:
            veraenderung = 0  # Keine Fälle damals und heute
        else:
            veraenderung = 100  # Oder "∞ %", wenn du das willst
    else:
        veraenderung = ((anzahl_2024 - anzahl_2009) / anzahl_2009) * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=jahre, y=werte, mode='lines', line=dict(color=color_all, width=2)))
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=0, b=0),
        height=30,
        width=150,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    img_bytes = fig.to_image(format="png")
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    trend_summary.append({
        "Delikt": delikt,
        "Anzahl": int(anzahl_2024),
        "Veränderung": f"{veraenderung:.1f} %",
        "Trend_img": f"data:image/png;base64,{img_base64}"
    })

# --- Alters- und Beziehungsinfos ---
top_alter_opfer = häufigstes_alter(opfer, altersgruppen, "Opfer")
top_alter_taeter = häufigstes_alter(taeter, altersgruppen, "Täter")
top_beziehung_opfer = häufigste_beziehung(opfer, 2024, "Opfer", "Anzahl_geschaedigter_Personen_Total")
top_beziehung_taeter = häufigste_beziehung(taeter, 2024, "Täter", "Anzahl_beschuldigter_Personen_Total")

# --- Geschlechterverhältnisse ---
opfer_2024 = opfer[(opfer["Jahr"] == 2024) & (opfer["Geschlecht"].isin(["männlich", "weiblich"])) & (opfer["Beziehungsart"] == "Alle")]
geschlecht_pivot = opfer_2024.groupby(["Delikt", "Geschlecht"]).sum().unstack(fill_value=0)

taeter_2024 = taeter[(taeter["Jahr"] == 2024) & (taeter["Geschlecht"].isin(["männlich", "weiblich"])) & (taeter["Beziehungsart"] == "Alle")]
geschlecht_pivot_taeter = taeter_2024.groupby(["Delikt", "Geschlecht"]).sum().unstack(fill_value=0)

# --- Zusammenführen ---
trend_summary.sort(key=lambda x: x["Anzahl"], reverse=True)
table_data = []
for item in trend_summary:
    delikt = item["Delikt"]
    alt_info = {**top_alter_opfer.get(delikt, {}), **top_alter_taeter.get(delikt, {})}
    bez_info = {**top_beziehung_opfer.get(delikt, {}), **top_beziehung_taeter.get(delikt, {})}

    m = geschlecht_pivot.loc[delikt]["Anzahl_geschaedigter_Personen_Total"]["männlich"] if delikt in geschlecht_pivot.index else 0
    w = geschlecht_pivot.loc[delikt]["Anzahl_geschaedigter_Personen_Total"]["weiblich"] if delikt in geschlecht_pivot.index else 0
    img_gender_opfer = geschlechter_balken_plotly(m, w)

    m_t = geschlecht_pivot_taeter.loc[delikt]["Anzahl_beschuldigter_Personen_Total"]["männlich"] if delikt in geschlecht_pivot_taeter.index else 0
    w_t = geschlecht_pivot_taeter.loc[delikt]["Anzahl_beschuldigter_Personen_Total"]["weiblich"] if delikt in geschlecht_pivot_taeter.index else 0
    img_gender_taeter = geschlechter_balken_plotly(m_t, w_t)

    table_data.append({
        "Delikt": delikt,
        "Anzahl": item["Anzahl"],
        "Trend_src": item["Trend_img"],
        "Veränderung": item["Veränderung"],
        "Geschlechterverhältnis_src": f"data:image/png;base64,{img_gender_opfer}",
        "Geschlechterverhältnis_taeter_src": f"data:image/png;base64,{img_gender_taeter}",
        "Häufigstes_Alter_Opfer": alt_info.get("Häufigstes Alter (Opfer)", "–"),
        "Häufigstes_Alter_Taeter": alt_info.get("Häufigstes Alter (Täter)", "–"),
        "Häufigste_Beziehungsart_Opfer": bez_info.get("Häufigste Beziehung (Opfer)", "–"),
        "Häufigste_Beziehungsart_Taeter": bez_info.get("Häufigste Beziehung (Täter)", "–")
    })
cell_style = {'padding': '0 10px', 'whiteSpace': 'nowrap','height': '40px'}
title_cell_style = {**cell_style, 'whiteSpace': 'normal'}
header_style = {'padding': '0 10px', 'whiteSpace': 'normal'}

# --- Dash Layout ---
layout = html.Div([
    html.H2([
        "Welche Delikte gibt es?",
        html.Span(" ℹ️", id="info-icon2", style={"cursor": "pointer", "marginLeft": "10px"})
    ],
        style={'textAlign': 'left', 'marginLeft': 40, 'paddingBottom': '8px', 'marginTop': 48, 'fontWeight': 600}),

    dbc.Tooltip(
        "Bei zu niedrigen Datenwerten, wird keine Aussage zum Alter gemacht",
        target="info-icon2",
        placement="right",
        style={'textAlign': 'left'},

    ),

    dcc.Store(id='sort-direction', data='desc'),

        html.Div([
            dbc.ButtonGroup([
                dbc.Button("Absteigend nach Anzahl Straftaten", id="btn-desc", n_clicks=0, className="toggle-btn active"),
                dbc.Button("Aufsteigend nach Anzahl Straftaten", id="btn-asc", n_clicks=0, className="toggle-btn"),
            ], style={'marginLeft': '40px', 'marginTop': '20px'})
        ]),


#Legende
    html.Div([
        html.Span(style={
            'display': 'inline-block',
            'width': '15px',
            'height': '15px',
            'backgroundColor': color_women,
            'marginRight': '5px'
        }),
        html.Span("Weiblich", style={'marginRight': '15px'}),

        html.Span(style={
            'display': 'inline-block',
            'width': '15px',
            'height': '15px',
            'backgroundColor': color_men,
            'marginRight': '5px'
        }),
        html.Span("Männlich")
    ], style={'marginLeft': '40px', 'marginTop': '20px'}),

    html.Table([
        html.Thead(html.Tr([
            html.Th("Delikt nach Strafgesetzbuch Artikel", style=header_style),
            html.Th("Straftaten (2024)", style={**header_style, 'textAlign': 'right', 'width': '100px'}),
            html.Th(["Straftaten Trend ", html.Br(), " (2009 – 2024)"], style=header_style),
            html.Th(["Veränderung Straftaten", html.Br(), " 2009 vs. 2024 (in %)"], style={**header_style, 'textAlign': 'right', }),
            html.Th(["Geschlechterverhältnis", html.Br(), "(Täter:innen, 2024)"], style=header_style),
            html.Th(["Geschlechterverhältnis", html.Br(), "(Opfer, 2024)"], style=header_style),
            html.Th(["Häufigste Beziehungsart", html.Br(), "(Täter:innen, 2024)"], style=header_style),
            html.Th(["Häufigste Beziehungsart ", html.Br(), "(Opfer, 2024)"], style=header_style),
            html.Th(["Häufigstes Alter ", html.Br(), "(Täter:inne, 2024)"], style=header_style),
            html.Th(["Häufigstes Alter ", html.Br(), "(Opfer, 2024)"], style=header_style)
        ])),
        html.Tbody(id="delikte-table"),
    ], style={
        'width': '95%',
        'margin': 40,
        'marginTop': 16,
        'fontSize': '13px',
        'borderCollapse': 'collapse'
    }),
    html.Div([
        html.P("Hinweise", style={'textAlign': 'left', 'fontSize': 18, 'color': 'black', 'marginLeft': 40, 'font-weight': '600', 'padding': '0px'}),
        html.P("*Sexueller Übergriff und sexuelle Nötigung (Art. 189) war bis 30. Juni 2024 Sexuelle Nötigung (Art. 189).", style={'textAlign': 'left', 'fontStyle': 'italic', 'fontSize': 16, 'color': 'black', 'marginLeft': 40}),
        html.P("**Missbrauch einer urteilsunfähigen oder zum Widerstand unfähigen Person (Art. 191) war bis 30. Juni 2024 Schändung (Art. 191).", style={'textAlign': 'left', 'fontStyle': 'italic', 'fontSize': 16, 'color': 'black', 'marginLeft': 40}),
        html.P("***Ausnützung einer Notlage oder Abhängigkeit (Art. 193) war bis 30. Juni 2024 Ausnützung der Notlage (Art. 193).", style={'textAlign': 'left', 'fontStyle': 'italic', 'fontSize': 16, 'color': 'black', 'marginLeft': 40}),
        html.P("",
               style={'textAlign': 'left', 'fontStyle': 'italic', 'fontSize': 16, 'color': 'black', 'marginLeft': 40, 'marginBottom': '40px'}),
    ]),

    html.Div([
        html.Hr(),
        html.P("Quelle: BFS – Polizeiliche Kriminalstatistik (PKS), Datenstand: 14.02.2025 ",
               style={'textAlign': 'left', 'marginLeft': 40, 'fontStyle': 'italic', 'fontSize': 16, 'color': 'black'})
    ])


])


# Hier registrieren wir die Callbacks für diesen Tab
def register_callbacks(app):

    # Toggle Button Logik
    @app.callback(
        Output("btn-asc", "className"),
        Output("btn-desc", "className"),
        Output("sort-direction", "data"),
        Input("btn-asc", "n_clicks"),
        Input("btn-desc", "n_clicks"),
        prevent_initial_call=True
    )
    def update_sort_direction(n_asc, n_desc):
        if ctx.triggered_id == "btn-asc":
            return "toggle-btn active", "toggle-btn", "asc"
        else:
            return "toggle-btn", "toggle-btn active", "desc"

    # Tabelle aktualisieren je nach Sortierung
    @app.callback(
        Output("delikte-table", "children"),
        Input("sort-direction", "data")
    )
    def update_table(sort_order):
        sorted_summary = sorted(trend_summary, key=lambda x: x["Anzahl"], reverse=(sort_order == "desc"))

        rows = []
        for item in sorted_summary:
            delikt = item["Delikt"]
            alt_info = {**top_alter_opfer.get(delikt, {}), **top_alter_taeter.get(delikt, {})}
            bez_info = {**top_beziehung_opfer.get(delikt, {}), **top_beziehung_taeter.get(delikt, {})}

            m = geschlecht_pivot.loc[delikt]["Anzahl_geschaedigter_Personen_Total"]["männlich"] if delikt in geschlecht_pivot.index else 0
            w = geschlecht_pivot.loc[delikt]["Anzahl_geschaedigter_Personen_Total"]["weiblich"] if delikt in geschlecht_pivot.index else 0
            img_gender_opfer = geschlechter_balken_plotly(m, w)

            m_t = geschlecht_pivot_taeter.loc[delikt]["Anzahl_beschuldigter_Personen_Total"]["männlich"] if delikt in geschlecht_pivot_taeter.index else 0
            w_t = geschlecht_pivot_taeter.loc[delikt]["Anzahl_beschuldigter_Personen_Total"]["weiblich"] if delikt in geschlecht_pivot_taeter.index else 0
            img_gender_taeter = geschlechter_balken_plotly(m_t, w_t)

            row = html.Tr([
                html.Td(delikt, style={**title_cell_style, 'fontWeight': 'bold'}),
                html.Td(f"{item['Anzahl']:,}", style={**cell_style, 'textAlign': 'right'}),
                html.Td(html.Img(src=item['Trend_img'], style={'height': '30px'}), style=cell_style),
                html.Td(item["Veränderung"], style={**cell_style, 'textAlign': 'right'}),
                html.Td(html.Img(src=f"data:image/png;base64,{img_gender_taeter}", style={'height': '20px'}), style=cell_style),
                html.Td(html.Img(src=f"data:image/png;base64,{img_gender_opfer}", style={'height': '20px'}), style=cell_style),
                html.Td(bez_info.get("Häufigste Beziehung (Täter)", "–"), style=cell_style),
                html.Td(bez_info.get("Häufigste Beziehung (Opfer)", "–"), style=cell_style),
                html.Td(alt_info.get("Häufigstes Alter (Täter)", "–"), style=cell_style),
                html.Td(alt_info.get("Häufigstes Alter (Opfer)", "–"), style=cell_style)
            ], style={'borderBottom': '1px solid #ddd', 'lineHeight': '1.8'})

            rows.append(row)

        return rows
    # Callback für die Anzeige des ausgewählten Zeitraums
    @app.callback(
        Output('zeitraum-info-tab2', 'children'),
        [Input('jahr-slider-tab2', 'value')]
    )
    def update_zeitraum_info_tab2(jahr_bereich):
        jahr_start, jahr_ende = jahr_bereich
        if jahr_start == jahr_ende:
            return f"Ausgewähltes Jahr: {jahr_start}"
        else:
            return f"Ausgewählter Zeitraum: {jahr_start} - {jahr_ende}"
