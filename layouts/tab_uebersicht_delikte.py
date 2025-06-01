import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import base64

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
        df[col] = pd.to_numeric(df[col], errors="coerce")
    for delikt in df["Delikt"].unique():
        subset = df[df["Delikt"] == delikt]
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
        elif top_ages:
            top_age_label = list(top_ages)[0]
        else:
            top_age_label = "–"
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
        max_val = delikt_df[wert_col].max()
        top_rows = delikt_df[delikt_df[wert_col] == max_val]
        if len(top_rows) > 1:
            beziehungsart = "Mehrere"
        else:
            beziehungsart = top_rows.iloc[0]["Beziehungsart"]
        top_bez[delikt] = {
            f"Häufigste Beziehung ({label})": beziehungsart,
            f"Anzahl Beziehung ({label})": max_val
        }
    return top_bez



def geschlechter_balken_plotly(m, w):
    total = m + w
    ratio_m = m / total if total > 0 else 0
    ratio_w = w / total if total > 0 else 0

    fig = go.Figure(data=[
        go.Bar(
            x=[ratio_m],
            y=[""],
            orientation='h',
            marker_color=color_men,
            showlegend=False,
            hoverinfo='skip'
        ),
        go.Bar(
            x=[ratio_w],
            y=[""],
            orientation='h',
            base=[ratio_m],
            marker_color=color_women,
            showlegend=False,
            hoverinfo='skip'
        )
    ])

    fig.update_layout(
        barmode='stack',  # <<< das macht den Unterschied
        xaxis=dict(range=[0, 1], visible=False, fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True),
        margin=dict(l=0, r=0, t=0, b=0),
        height=24,
        width=200,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # to_image
    return base64.b64encode(fig.to_image(format='png')).decode('utf-8')


# --- Trenddaten ---
taeter_filtered = taeter[(taeter["Beziehungsart"] == "Alle") & (taeter["Geschlecht"] == "Total")]
trend_data = taeter_filtered[taeter_filtered["Jahr"].between(2009, 2024)]
trend_summary = []

for delikt in trend_data["Delikt"].unique():
    delikt_data = trend_data[trend_data["Delikt"] == delikt].sort_values("Jahr")
    jahre = delikt_data["Jahr"].tolist()
    werte = delikt_data["Anzahl_beschuldigter_Personen_Total"].tolist()
    anzahl_2024 = delikt_data[delikt_data["Jahr"] == 2024]["Anzahl_beschuldigter_Personen_Total"].sum()
    anzahl_2009 = delikt_data[delikt_data["Jahr"] == 2009]["Anzahl_beschuldigter_Personen_Total"].sum()
    veraenderung = ((anzahl_2024 - anzahl_2009) / max(anzahl_2009, 1)) * 100

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

# --- Dash Layout ---
layout = html.Div([
    html.H4("Übersicht Delikte Häusliche Gewalt (Stand 2024, aufsteigend Anzahl Straftaten)", style={'marginTop': 30, 'marginLeft': 20}),
    html.Table([
        html.Thead(html.Tr([
            html.Th("Delikt"),
            html.Th("Anzahl Straftaten 2024", style={'textAlign': 'right', 'width': '100px'}),

            html.Th("Trendlinie Straftaten (2009–2024)"),
            html.Th("Veränderung Straftaten (%)", style={'textAlign': 'right', 'width': '100px'}),
            html.Th("Geschlechterverhältnis (Täter:innen)"),
            html.Th("Geschlechterverhältnis (Opfer)"),
            html.Th("Häufigste Beziehungsart (Täter:innen)"),
            html.Th("Häufigste Beziehungsart (Opfer)"),
            html.Th("Häufigstes Alter (Täter:innen)"),
            html.Th("Häufigstes Alter (Opfer)")
        ])),
        html.Tbody([
            html.Tr([
                html.Td(row['Delikt']),
                html.Td(f"{row['Anzahl']:,}", style={'textAlign': 'right'}),
                html.Td(html.Img(src=row['Trend_src'], style={'height': '30px'})),
                html.Td(row['Veränderung'], style={'textAlign': 'right'}),
                html.Td(html.Img(src=row['Geschlechterverhältnis_taeter_src'], style={'height': '20px'})),
                html.Td(html.Img(src=row['Geschlechterverhältnis_src'], style={'height': '20px'})),
                html.Td(row['Häufigste_Beziehungsart_Taeter']),
                html.Td(row['Häufigste_Beziehungsart_Opfer']),
                html.Td(row['Häufigstes_Alter_Taeter']),
                html.Td(row['Häufigstes_Alter_Opfer'])
            ], style={'borderBottom': '1px solid #ddd', 'lineHeight': '1.8'})
            for row in table_data
        ])
    ], style={
        'width': '95%',
        'margin': 20,
        'fontSize': '12px',
        'borderCollapse': 'collapse'
    }),
    html.Div([
        html.Hr(),
        html.P("Sexueller Übergriff und sexuelle Nötigung (Art. 189) war bis 30. Juni 2024 Sexuelle Nötigung (Art. 189).", style={'textAlign': 'left', 'fontStyle': 'italic', 'fontSize': 12, 'color': 'black', 'marginLeft': 20}),
        html.P("Missbrauch einer urteilsunfähigen oder zum Widerstand unfähigen Person (Art. 191)6 war bis 30. Juni 2024 Schändung (Art. 191).", style={'textAlign': 'left', 'fontStyle': 'italic', 'fontSize': 12, 'color': 'black', 'marginLeft': 20}),
        html.P("Ausnützung einer Notlage oder Abhängigkeit (Art. 193) war bis 30. Juni 2024 Ausnützung der Notlage (Art. 193).", style={'textAlign': 'left', 'fontStyle': 'italic', 'fontSize': 12, 'color': 'black', 'marginLeft': 20}),
        html.P("",
               style={'textAlign': 'left', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888', 'marginLeft': 20}),
    ]),

    html.Div([
        html.Hr(),
        html.P(
            "",
            style={'textAlign': 'left', 'fontStyle': 'italic', 'fontSize': 12, 'color': 'black', 'marginLeft': 20}),
        html.P(
            "",
            style={'textAlign': 'left', 'fontStyle': 'italic', 'fontSize': 12, 'color': 'black', 'marginLeft': 20}),
        html.P(
            "",
            style={'textAlign': 'left', 'fontStyle': 'italic', 'fontSize': 12, 'color': 'black', 'marginLeft': 20}),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009–2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888', 'marginLeft': 20}),
    ]),

])


# Hier registrieren wir die Callbacks für diesen Tab
def register_callbacks(app):



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
