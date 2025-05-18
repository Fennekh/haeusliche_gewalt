# Gemeinsame Daten für alle Tabs

# Funktion zum Laden der Daten, die in allen drei Tabs verwendet werden können
def load_data():
    # Daten aus der ursprünglichen Datei
    opfer_data = [
        {"year": 2009, "totalMale": 2319, "totalFemale": 7397, "ageGroups": {
            "male": {"<10": 178, "10-19": 276, "20-29": 364, "30-39": 491, "40-49": 555, "50-59": 287, "60-69": 121,
                     "70+": 47},
            "female": {"<10": 205, "10-19": 774, "20-29": 2016, "30-39": 2068, "40-49": 1570, "50-59": 522, "60-69": 178,
                       "70+": 63}}},
        # Alle Datensätze hier einfügen...
    ]

    taeter_data = [
        {"year": 2009, "totalMale": 7476, "totalFemale": 1772, "ageGroups": {
            "male": {"<10": 0, "10-19": 354, "20-29": 1709, "30-39": 2190, "40-49": 2022, "50-59": 859, "60-69": 254,
                     "70+": 84},
            "female": {"<10": 0, "10-19": 84, "20-29": 424, "30-39": 601, "40-49": 455, "50-59": 137, "60-69": 47,
                       "70+": 22}}},
        # Alle Datensätze hier einfügen...
    ]

    import pandas as pd
    
    # Opfer nach Jahr und Geschlecht
    opfer_yearly = pd.DataFrame([(item['year'], item['totalMale'], item['totalFemale'])
                                for item in opfer_data],
                                columns=['Jahr', 'Männliche Opfer', 'Weibliche Opfer'])

    # Täter nach Jahr und Geschlecht
    taeter_yearly = pd.DataFrame([(item['year'], item['totalMale'], item['totalFemale'])
                                for item in taeter_data],
                                columns=['Jahr', 'Männliche Täter', 'Weibliche Täter'])

    # Altersgruppen für alle Jahre
    opfer_age_all_years = []
    taeter_age_all_years = []

    for data in opfer_data:
        year = data['year']
        for gender, gender_label in [('male', 'Männlich'), ('female', 'Weiblich')]:
            for age_group, count in data['ageGroups'][gender].items():
                opfer_age_all_years.append((year, gender_label, age_group, count))

    for data in taeter_data:
        year = data['year']
        for gender, gender_label in [('male', 'Männlich'), ('female', 'Weiblich')]:
            for age_group, count in data['ageGroups'][gender].items():
                taeter_age_all_years.append((year, gender_label, age_group, count))

    opfer_age_df = pd.DataFrame(opfer_age_all_years, columns=['Jahr', 'Geschlecht', 'Altersgruppe', 'Anzahl'])
    taeter_age_df = pd.DataFrame(taeter_age_all_years, columns=['Jahr', 'Geschlecht', 'Altersgruppe', 'Anzahl'])

    # Altersgruppensortierung festlegen
    age_order = ['<10', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70+']
    opfer_age_df['Altersgruppe'] = pd.Categorical(opfer_age_df['Altersgruppe'], categories=age_order, ordered=True)
    taeter_age_df['Altersgruppe'] = pd.Categorical(taeter_age_df['Altersgruppe'], categories=age_order, ordered=True)
    
    return {
        'opfer_data': opfer_data,
        'taeter_data': taeter_data,
        'opfer_yearly': opfer_yearly,
        'taeter_yearly': taeter_yearly,
        'opfer_age_df': opfer_age_df,
        'taeter_age_df': taeter_age_df,
        'age_order': age_order
    }
