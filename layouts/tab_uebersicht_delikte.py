import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.validators.scatter.marker import SymbolValidator
from dash import dash_table
import matplotlib.pyplot as plt
import io
import base64
import plotly.io as pio



#------ Variabeln überall gleich

#Variabeln
color_women = "#811616"
color_men = "#0a0a35"
color_all = "black"

# Roboto-Template definieren (bei allen seiten machen?)
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
#------


#------
#Daten laden
opfer = pd.read_csv("data/geschaedigte_tidy.csv")
taeter = pd.read_csv("data/beschuldigte_tidy.csv")

#----Datenvorbereitung für Tabelle
# Liste der Altersgruppen aus den Spaltennamen
altersgruppen = [
    '<10 Jahre', '10 - 19 Jahre', '20 - 29 Jahre', '30 - 39 Jahre',
    '40 - 49 Jahre', '50 - 59 Jahre', '60 - 69 Jahre', '70 Jahre und +'
]

# Daten filtern auf Jahr 2024
opfer_2024 = opfer[opfer["Jahr"] == 2024].copy()
taeter_2024 = taeter[taeter["Jahr"] == 2024].copy()

# Altersgruppen-Spalten in Zahlen umwandeln (für Berechnungen)
for col in altersgruppen:
    opfer_2024[col] = pd.to_numeric(opfer_2024[col], errors="coerce")
    taeter_2024[col] = pd.to_numeric(taeter_2024[col], errors="coerce")

# Zeilenweise: häufigstes Alter und entsprechende Anzahl bestimmen
opfer_2024["Häufigstes Alter (Opfer)"] = opfer_2024[altersgruppen].idxmax(axis=1)
opfer_2024["Anzahl (Opfer)"] = opfer_2024[altersgruppen].max(axis=1)

taeter_2024["Häufigstes Alter (Täter)"] = taeter_2024[altersgruppen].idxmax(axis=1)
taeter_2024["Anzahl (Täter)"] = taeter_2024[altersgruppen].max(axis=1)

# Für jedes Delikt: die Zeile mit der höchsten Altersgruppen-Anzahl behalten
opfer_top_alter = opfer_2024.loc[
    opfer_2024.groupby("Delikt")["Anzahl (Opfer)"].idxmax()
][["Delikt", "Häufigstes Alter (Opfer)", "Anzahl (Opfer)"]]

taeter_top_alter = taeter_2024.loc[
    taeter_2024.groupby("Delikt")["Anzahl (Täter)"].idxmax()
][["Delikt", "Häufigstes Alter (Täter)", "Anzahl (Täter)"]]

# Zusammenführen für Anzeige oder weitere Nutzung
top_alter_pro_delikt = pd.merge(opfer_top_alter, taeter_top_alter, on="Delikt", how="outer")
#---- Datenvorbereitung Alter

# In ein Nachschlage-Dict umwandeln
top_alter_dict = top_alter_pro_delikt.set_index("Delikt").to_dict("index")


#--- Beziehungen
# --- Häufigste Beziehungsart für Opfer und Täter:innen (nach Anzahl) ---

# Daten für 2024 vorbereiten
opfer_2024 = opfer[
    (opfer["Jahr"] == 2024) &
    (opfer["Beziehungsart"] != "Alle")
]
taeter_2024 = taeter[
    (taeter["Jahr"] == 2024) &
    (taeter["Beziehungsart"] != "Alle")
]
# Opfer: häufigste Beziehungsart pro Delikt
opfer_2024_grouped = opfer_2024.groupby(["Delikt", "Beziehungsart"])["Anzahl_geschaedigter_Personen_Total"].sum().reset_index()
opfer_top_beziehung = opfer_2024_grouped.loc[
    opfer_2024_grouped.groupby("Delikt")["Anzahl_geschaedigter_Personen_Total"].idxmax()
].rename(columns={
    "Beziehungsart": "Häufigste Beziehung (Opfer)",
    "Anzahl_geschaedigter_Personen_Total": "Anzahl Beziehung (Opfer)"
})

# Täter:innen: häufigste Beziehungsart pro Delikt
taeter_2024_grouped = taeter_2024.groupby(["Delikt", "Beziehungsart"])["Anzahl_beschuldigter_Personen_Total"].sum().reset_index()
taeter_top_beziehung = taeter_2024_grouped.loc[
    taeter_2024_grouped.groupby("Delikt")["Anzahl_beschuldigter_Personen_Total"].idxmax()
].rename(columns={
    "Beziehungsart": "Häufigste Beziehung (Täter)",
    "Anzahl_beschuldigter_Personen_Total": "Anzahl Beziehung (Täter)"
})

# Zusammenführen für gemeinsame Nutzung
top_beziehung_pro_delikt = pd.merge(opfer_top_beziehung, taeter_top_beziehung, on="Delikt", how="outer")

# In ein Dictionary für Nachschlagen umwandeln
top_beziehung_dict = top_beziehung_pro_delikt.set_index("Delikt").to_dict("index")




#Datenvorbereitung -- geschlecht
# Nur Beziehungsart = Alle und Geschlecht = Total verwenden
taeter_filtered = taeter[(taeter["Beziehungsart"] == "Alle") & (taeter["Geschlecht"] == "Total")]

# Gruppieren nach Delikt und Jahr
taeter_grouped = taeter_filtered.groupby(['Delikt', 'Jahr'])['Anzahl_beschuldigter_Personen_Total'].sum().reset_index()

# Pivot-Tabelle: Delikt als Zeile, Jahre als Spalten
trend_pivot = taeter_grouped.pivot(index='Delikt', columns='Jahr', values='Anzahl_beschuldigter_Personen_Total')

# Fehlende Werte auffüllen (z. B. Delikte, die in 2009 oder 2024 nicht gemeldet wurden)
trend_pivot = trend_pivot.fillna(0)

# Mini-Trendliste + aktuelle Zahlen + Veränderung
trend_pivot['Anzahl'] = trend_pivot[2024]
trend_pivot['Trend'] = trend_pivot.apply(lambda row: row.loc[2009:2024].tolist(), axis=1)
trend_pivot['Veränderung (%)'] = ((trend_pivot[2024] - trend_pivot[2009]) / trend_pivot[2009].replace(0, 1)) * 100

# Sortieren nach Anzahl (2024)
trend_pivot_sorted = trend_pivot.sort_values(by='Anzahl', ascending=False).reset_index()


# --- Vorbereitung der Mini-Geschlechterbalken ---
opfer_agg = opfer[(opfer["Geschlecht"].isin(["männlich", "weiblich"])) & (opfer["Beziehungsart"] == "Alle")]
opfer_latest = opfer_agg[opfer_agg["Jahr"] == 2024]
geschlecht_pivot = opfer_latest.pivot_table(index="Delikt", columns="Geschlecht", values="Anzahl_geschaedigter_Personen_Total", aggfunc="sum").fillna(0)

geschlecht_balken = {}
for delikt, row in geschlecht_pivot.iterrows():
    fig, ax = plt.subplots(figsize=(2, 0.3))
    total = row["männlich"] + row["weiblich"]
    if total == 0:
        ratio_m = ratio_w = 0.5
    else:
        ratio_m = row["männlich"] / total
        ratio_w = row["weiblich"] / total

    ax.barh([0], [ratio_m], color=color_men)
    ax.barh([0], [ratio_w], left=[ratio_m], color=color_women)
    ax.set_xlim(0, 1)
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    geschlecht_balken[delikt] = f"data:image/png;base64,{img_b64}"


# --- Vorbereitung der Mini-Geschlechterbalken für Täter:innen ---
taeter_agg = taeter[(taeter["Geschlecht"].isin(["männlich", "weiblich"])) & (taeter["Beziehungsart"] == "Alle")]
taeter_latest = taeter_agg[taeter_agg["Jahr"] == 2024]
geschlecht_pivot_taeter = taeter_latest.pivot_table(
    index="Delikt",
    columns="Geschlecht",
    values="Anzahl_beschuldigter_Personen_Total",
    aggfunc="sum"
).fillna(0)

geschlecht_balken_taeter = {}
for delikt, row in geschlecht_pivot_taeter.iterrows():
    fig, ax = plt.subplots(figsize=(2, 0.3))
    total = row["männlich"] + row["weiblich"]
    if total == 0:
        ratio_m = ratio_w = 0.5
    else:
        ratio_m = row["männlich"] / total
        ratio_w = row["weiblich"] / total

    ax.barh([0], [ratio_m], color=color_men)
    ax.barh([0], [ratio_w], left=[ratio_m], color=color_women)
    ax.set_xlim(0, 1)
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('utf-8')
    geschlecht_balken_taeter[delikt] = f"data:image/png;base64,{img_b64}"




#------
# Funktion zur Erstellung von Mini-Trendgrafiken als base64
table_data = []
for _, row in trend_pivot_sorted.iterrows():
    fig, ax = plt.subplots(figsize=(2, 0.5))
    ax.plot(row['Trend'], linewidth=1.5,color=color_all)
    ax.set_axis_off()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    trend_img = f"data:image/png;base64,{img_base64}"
    delikt = row['Delikt']
    top_alter_info = top_alter_dict.get(delikt, {})
    top_beziehung = top_beziehung_dict.get(row['Delikt'], {})


    table_data.append({
        'Delikt': delikt,
        'Anzahl': int(row['Anzahl']),
        'Trend_src': trend_img,
        'Veränderung': f"{row['Veränderung (%)']:.1f} %",
        'Geschlechterverhältnis_src': geschlecht_balken.get(delikt, ""),
        'Geschlechterverhältnis_taeter_src': geschlecht_balken_taeter.get(delikt, ""),
        'Häufigstes_Alter_Opfer': top_alter_info.get("Häufigstes Alter (Opfer)", "–"),
        'Häufigstes_Alter_Taeter': top_alter_info.get("Häufigstes Alter (Täter)", "–"),
        'Häufigste_Beziehungsart_Taeter': top_beziehung.get("Häufigste Beziehung (Täter)", "–"),
        'Häufigste_Beziehungsart_Opfer': top_beziehung.get("Häufigste Beziehung (Opfer)", "–"),

    })


#----

# Layout für den ersten Tab (Zeitliche Entwicklung)
layout = html.Div([
    # Zeitraum-Information
    html.Div(id='zeitraum-info-tab1', style={'textAlign': 'center', 'marginBottom': 20}),





    # Tabelle + weitere Visualisierungen
    dbc.Row([
        dbc.Col([
            html.H4("Übersicht Delikte (Stand 2024)", style={'marginTop': 30, 'marginLeft': 20}),
            html.Table([
                html.Thead(
                    html.Tr([
                        html.Th("Delikt"),
                        html.Th("Straftaten 2024"),
                        html.Th("Trend 2009–2024"),
                        html.Th("Veränderung (%)"),
                        html.Th("Geschlechterverhältnis (Täter:innen)"),
                        html.Th("Geschlechterverhältnis (Opfer)"),
                        html.Th("Häufigste Beziehungsart (Täter:innen)"),
                        html.Th("Häufigste Beziehungsart (Opfer)"),
                        html.Th("Häufigstes Alter (Täter:innen)"),
                        html.Th("Häufigstes Alter (Opfer)"),

                    ])
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(row['Delikt']),
                        html.Td(row['Anzahl']),
                        html.Td(html.Img(src=row['Trend_src'], style={'height': '30px'})),
                        html.Td(row['Veränderung']),
                        html.Td(html.Img(src=row['Geschlechterverhältnis_taeter_src'], style={'height': '20px'})),
                        html.Td(html.Img(src=row['Geschlechterverhältnis_src'], style={'height': '20px'})),
                        html.Td(row['Häufigste_Beziehungsart_Taeter']),
                        html.Td(row['Häufigste_Beziehungsart_Opfer']),
                        html.Td(row['Häufigstes_Alter_Taeter']),
                        html.Td(row['Häufigstes_Alter_Opfer']),



                    ]) for row in table_data
                ])
            ], style={'width': '95%', 'borderCollapse': 'collapse',  'margin': 20})

    ]),

    # Fußnote
    html.Div([
        html.Hr(),
        html.P("Daten basierend auf Statistiken zu häuslicher Gewalt (Schweiz, 2009–2024)",
               style={'textAlign': 'center', 'fontStyle': 'italic', 'fontSize': 12, 'color': '#888'})
    ])
])
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
