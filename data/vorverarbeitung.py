import pandas as pd


# Excel-Datei laden
#excel_file = pd.ExcelFile("geschaedigte.xlsx")  # ggf. Pfad anpassen
excel_file = pd.ExcelFile("beschuldigte.xlsx")  # ggf. Pfad anpassen
jahre = [str(j) for j in range(2009, 2025)]
alle_jahre_df = []

# Extraktionsfunktion pro einen Deliktblock um diese später einzeln anprechen zu können
def extract_block(df_block, jahr):
    rows = []

    def add_row(row, delikt, geschlecht, beziehungsart):
        rows.append({
            "Jahr": jahr,
            "Delikt": delikt,
            "Geschlecht": geschlecht,
            "Beziehungsart": beziehungsart,
            "Fälle": row[2] if len(row) > 2 else None,
            "Straftaten_Total": row[3] if len(row) > 3 else None,
            "davon_versucht": row[4] if len(row) > 4 else None,
            "davon_mehrfach": row[5] if len(row) > 5 else None,
            "Anzahl_beschuldigter_Personen_Total": row[6] if len(row) > 6 else None,
            "<10 Jahre": row[7] if len(row) > 7 else None,
            "10 - 14 Jahre": row[8] if len(row) > 8 else None,
            "15 - 17 Jahre": row[9] if len(row) > 9 else None,
            "17 - 19 Jahre": row[10] if len(row) > 10 else None,
            "20 - 24 Jahre": row[11] if len(row) > 11 else None,
            "25 - 29 Jahre": row[12] if len(row) > 12 else None,
            "30 - 34 Jahre": row[13] if len(row) > 13 else None,
            "35 - 39 Jahre": row[14] if len(row) > 14 else None,
            "40 - 49 Jahre": row[15] if len(row) > 15 else None,
            "50 - 59 Jahre": row[16] if len(row) > 16 else None,
            "60 - 69 Jahre": row[17] if len(row) > 17 else None,
            "70 Jahre und +": row[18] if len(row) > 18 else None
        })

    delikt = df_block.iloc[0, 0] if len(df_block) > 0 else "Unbekannt"

    if len(df_block) > 0: add_row(df_block.iloc[0], delikt, "Total", "Alle")
    if len(df_block) > 1: add_row(df_block.iloc[1], delikt, "männlich", "Alle")
    for i in range(2, 6):
        if i >= len(df_block): break
        beziehungsart = df_block.iloc[i, 1] if pd.notna(df_block.iloc[i, 1]) else "Alle"
        add_row(df_block.iloc[i], delikt, "männlich", beziehungsart)
    if len(df_block) > 6: add_row(df_block.iloc[6], delikt, "weiblich", "Alle")
    for i in range(7, 11):
        if i >= len(df_block): break
        beziehungsart = df_block.iloc[i, 1] if pd.notna(df_block.iloc[i, 1]) else "Alle"
        add_row(df_block.iloc[i], delikt, "weiblich", beziehungsart)

    return pd.DataFrame(rows)

# Verarbeite alle Jahre (Aufteilung Jahre
for jahr in jahre:
    df_sheet = excel_file.parse(jahr, header=None)

    # Finde Deliktstartzeilen
    alle_starts = df_sheet[df_sheet[0].astype(str).str.match(r"^\s*(Total Häusliche Gewalt|.*\(.*Art\.)", na=False)].index.tolist()
    letzter_index = df_sheet[df_sheet[0].astype(str).str.contains("Strafbare Vorbereitungshandlungen", na=False)].index.max()
    delikt_start_indices = [idx for idx in alle_starts if idx <= letzter_index]

    # Alle Deliktblöcke extrahieren
    jahr_df = []
    for idx in delikt_start_indices:
        block = df_sheet.iloc[idx:idx + 11]
        jahr_df.append(extract_block(block, jahr=int(jahr)))

    # Zusammenführen
    alle_jahre_df.append(pd.concat(jahr_df, ignore_index=True))

# Alles zusammenfassen
df = pd.concat(alle_jahre_df, ignore_index=True)


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

# "X" durch NaN ersetzen und in numerische Werte umwandeln
df[age_columns_to_convert] = df[age_columns_to_convert].replace("X", pd.NA).apply(pd.to_numeric, errors='coerce')

# Altersgruppen aggregieren
df['10 - 19 Jahre'] = df[['10 - 14 Jahre', '15 - 17 Jahre', '17 - 19 Jahre']].sum(axis=1, skipna=True)
df['20 - 29 Jahre'] = df[['20 - 24 Jahre', '25 - 29 Jahre']].sum(axis=1, skipna=True)
df['30 - 39 Jahre'] = df[['30 - 34 Jahre', '35 - 39 Jahre']].sum(axis=1, skipna=True)


df = df.drop(columns=['10 - 14 Jahre', '15 - 17 Jahre', '17 - 19 Jahre',
    '20 - 24 Jahre', '25 - 29 Jahre',
    '30 - 34 Jahre', '35 - 39 Jahre'])

# Definierte Altersreihenfolge
age_order = ["<10 Jahre", "10 - 19 Jahre", "20 - 29 Jahre", "30 - 39 Jahre",
             "40 - 49 Jahre", "50 - 59 Jahre", "60 - 69 Jahre", "70 Jahre und +"]

# Alle anderen Spalten
meta_columns = [col for col in df.columns if col not in age_order]

# Sortiertes DataFrame
df = df[meta_columns + [col for col in age_order if col in df.columns]]

print(df.iloc[0])

# Speichern geschaedigte
#df.to_csv("geschaedigte_tidy.csv", index=False)
#print("✅ Datei gespeichert als 'geschaedigte_tidy.csv'")


# Speichern beschuldigte
df.to_csv("beschuldigte_tidy.csv", index=False)
print("✅ Datei gespeichert als 'beschuldigte_tidy.csv'")

#Hinweis: Deliktnamen mit Fussnote wurden im nachhnienin direkt in den Tidy Files noch angepasst.
