import plotly.express as px
import pandas as pd
from dash import dcc

# Beispiel-Daten
df = pd.DataFrame({
    'Altersgruppe': ['<18', '18-25', '26-35', '36-50', '51+'],
    'Fälle': [50, 120, 180, 140, 60]
})

fig = px.bar(df, x='Fälle', y='Altersgruppe', orientation='h', title='Fälle nach Altersgruppe')

component = dcc.Graph(figure=fig)