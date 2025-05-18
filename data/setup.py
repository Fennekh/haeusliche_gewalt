import os

# Verzeichnisstruktur erstellen
os.makedirs('layouts', exist_ok=True)

# Erstelle eine leere __init__.py-Datei im layouts-Verzeichnis,
# damit Python es als Paket erkennt
with open(os.path.join('layouts', '__init__.py'), 'w') as f:
    pass

print("Verzeichnisstruktur für die Dash-App erfolgreich erstellt!")
print("Bitte speichern Sie nun folgende Dateien:")
print("1. app.py (im Hauptverzeichnis)")
print("2. layouts/tab_zeitliche_entwicklung.py")
print("3. layouts/tab_geschlechterverhaeltnis.py")
print("4. layouts/tab_trend_analyse.py")
print("\nDenken Sie daran, die vollständigen Datensätze in jede Tab-Datei einzufügen!")
