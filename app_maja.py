import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

# Initialisiere die Dash-Anwendung
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']  # Beispiel für eine externe CSS-Datei

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
server = app.server

# Farbschema
MALE_COLOR = "#2D5E89"  # Dunkelblau
FEMALE_COLOR = "#E63946"  # Rot

# Altersklassen in der gewünschten Reihenfolge
age_groups = ["<10", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70+"]

# Winkel für jede Altersklasse (in Grad)
angles_deg = {
    "<10": 0,  # 12 Uhr
    "10-19": 45,  # 1:30 Uhr
    "20-29": 90,  # 3 Uhr
    "30-39": 135,  # 4:30 Uhr
    "40-49": 180,  # 6 Uhr
    "50-59": 225,  # 7:30 Uhr
    "60-69": 270,  # 9 Uhr
    "70+": 315  # 10:30 Uhr
}

# Winkel in Radianten für Plotly
angles_rad = {age: np.radians(angle) for age, angle in angles_deg.items()}

# Daten aus dem HTML-Dokument für alle Jahre
all_data = {
    "2009": {
        "opfer": {
            "männlich": {"<10": 178, "10-19": 276, "20-29": 364, "30-39": 491, "40-49": 555, "50-59": 287, "60-69": 121,
                         "70+": 47},
            "weiblich": {"<10": 205, "10-19": 774, "20-29": 2016, "30-39": 2068, "40-49": 1570, "50-59": 522,
                         "60-69": 178, "70+": 63}
        },
        "taeter": {
            "männlich": {"<10": 0, "10-19": 354, "20-29": 1709, "30-39": 2190, "40-49": 2022, "50-59": 859,
                         "60-69": 254, "70+": 84},
            "weiblich": {"<10": 0, "10-19": 84, "20-29": 424, "30-39": 601, "40-49": 455, "50-59": 137, "60-69": 47,
                         "70+": 22}
        }
    },
    "2010": {
        "opfer": {
            "männlich": {"<10": 185, "10-19": 276, "20-29": 379, "30-39": 496, "40-49": 528, "50-59": 288, "60-69": 119,
                         "70+": 48},
            "weiblich": {"<10": 195, "10-19": 756, "20-29": 1965, "30-39": 2090, "40-49": 1581, "50-59": 534,
                         "60-69": 172, "70+": 68}
        },
        "taeter": {
            "männlich": {"<10": 0, "10-19": 341, "20-29": 1733, "30-39": 2222, "40-49": 1973, "50-59": 853,
                         "60-69": 266, "70+": 84},
            "weiblich": {"<10": 0, "10-19": 97, "20-29": 450, "30-39": 656, "40-49": 488, "50-59": 146, "60-69": 48,
                         "70+": 16}
        }
    },
    "2011": {
        "opfer": {
            "männlich": {"<10": 200, "10-19": 309, "20-29": 404, "30-39": 516, "40-49": 531, "50-59": 292, "60-69": 118,
                         "70+": 51},
            "weiblich": {"<10": 212, "10-19": 759, "20-29": 1978, "30-39": 2095, "40-49": 1571, "50-59": 550,
                         "60-69": 177, "70+": 75}
        },
        "taeter": {
            "männlich": {"<10": 0, "10-19": 306, "20-29": 1695, "30-39": 2289, "40-49": 1975, "50-59": 882,
                         "60-69": 268, "70+": 80},
            "weiblich": {"<10": 0, "10-19": 80, "20-29": 455, "30-39": 643, "40-49": 481, "50-59": 169, "60-69": 52,
                         "70+": 20}
        }
    },
    "2012": {
        "opfer": {
            "männlich": {"<10": 206, "10-19": 298, "20-29": 400, "30-39": 517, "40-49": 529, "50-59": 302, "60-69": 127,
                         "70+": 59},
            "weiblich": {"<10": 221, "10-19": 760, "20-29": 1885, "30-39": 2075, "40-49": 1553, "50-59": 532,
                         "60-69": 173, "70+": 92}
        },
        "taeter": {
            "männlich": {"<10": 0, "10-19": 327, "20-29": 1644, "30-39": 2191, "40-49": 1881, "50-59": 857,
                         "60-69": 290, "70+": 98},
            "weiblich": {"<10": 0, "10-19": 89, "20-29": 447, "30-39": 651, "40-49": 485, "50-59": 177, "60-69": 51,
                         "70+": 20}
        }
    },
    "2013": {
        "opfer": {
            "männlich": {"<10": 198, "10-19": 332, "20-29": 424, "30-39": 534, "40-49": 523, "50-59": 299, "60-69": 126,
                         "70+": 58},
            "weiblich": {"<10": 217, "10-19": 761, "20-29": 1814, "30-39": 2045, "40-49": 1543, "50-59": 561,
                         "60-69": 183, "70+": 104}
        },
        "taeter": {
            "männlich": {"<10": 1, "10-19": 352, "20-29": 1607, "30-39": 2188, "40-49": 1827, "50-59": 836,
                         "60-69": 297, "70+": 103},
            "weiblich": {"<10": 0, "10-19": 103, "20-29": 447, "30-39": 645, "40-49": 514, "50-59": 192, "60-69": 52,
                         "70+": 23}
        }
    },
    "2014": {
        "opfer": {
            "männlich": {"<10": 185, "10-19": 331, "20-29": 427, "30-39": 514, "40-49": 502, "50-59": 303, "60-69": 136,
                         "70+": 65},
            "weiblich": {"<10": 226, "10-19": 753, "20-29": 1793, "30-39": 2022, "40-49": 1506, "50-59": 563,
                         "60-69": 190, "70+": 95}
        },
        "taeter": {
            "männlich": {"<10": 1, "10-19": 354, "20-29": 1558, "30-39": 2140, "40-49": 1788, "50-59": 909,
                         "60-69": 327, "70+": 100},
            "weiblich": {"<10": 0, "10-19": 91, "20-29": 424, "30-39": 622, "40-49": 514, "50-59": 187, "60-69": 53,
                         "70+": 25}
        }
    },
    "2015": {
        "opfer": {
            "männlich": {"<10": 196, "10-19": 327, "20-29": 433, "30-39": 527, "40-49": 496, "50-59": 340, "60-69": 134,
                         "70+": 58},
            "weiblich": {"<10": 240, "10-19": 746, "20-29": 1797, "30-39": 2076, "40-49": 1477, "50-59": 566,
                         "60-69": 166, "70+": 94}
        },
        "taeter": {
            "männlich": {"<10": 1, "10-19": 385, "20-29": 1513, "30-39": 2133, "40-49": 1815, "50-59": 923,
                         "60-69": 311, "70+": 116},
            "weiblich": {"<10": 0, "10-19": 103, "20-29": 447, "30-39": 670, "40-49": 522, "50-59": 187, "60-69": 49,
                         "70+": 18}
        }
    },
    "2016": {
        "opfer": {
            "männlich": {"<10": 261, "10-19": 398, "20-29": 467, "30-39": 647, "40-49": 610, "50-59": 334, "60-69": 155,
                         "70+": 90},
            "weiblich": {"<10": 271, "10-19": 848, "20-29": 1667, "30-39": 2208, "40-49": 1668, "50-59": 667,
                         "60-69": 181, "70+": 129}
        },
        "taeter": {
            "männlich": {"<10": 1, "10-19": 424, "20-29": 1361, "30-39": 2238, "40-49": 1930, "50-59": 947,
                         "60-69": 328, "70+": 122},
            "weiblich": {"<10": 0, "10-19": 126, "20-29": 507, "30-39": 803, "40-49": 651, "50-59": 249, "60-69": 71,
                         "70+": 29}
        }
    },
    "2017": {
        "opfer": {
            "männlich": {"<10": 272, "10-19": 420, "20-29": 466, "30-39": 666, "40-49": 651, "50-59": 342, "60-69": 140,
                         "70+": 90},
            "weiblich": {"<10": 259, "10-19": 860, "20-29": 1613, "30-39": 2264, "40-49": 1719, "50-59": 697,
                         "60-69": 213, "70+": 121}
        },
        "taeter": {
            "männlich": {"<10": 0, "10-19": 383, "20-29": 1296, "30-39": 2259, "40-49": 1943, "50-59": 954,
                         "60-69": 339, "70+": 126},
            "weiblich": {"<10": 0, "10-19": 124, "20-29": 545, "30-39": 904, "40-49": 716, "50-59": 287, "60-69": 96,
                         "70+": 37}
        }
    },
    "2018": {
        "opfer": {
            "männlich": {"<10": 296, "10-19": 459, "20-29": 466, "30-39": 696, "40-49": 628, "50-59": 381, "60-69": 154,
                         "70+": 104},
            "weiblich": {"<10": 291, "10-19": 965, "20-29": 1630, "30-39": 2402, "40-49": 1819, "50-59": 739,
                         "60-69": 205, "70+": 134}
        },
        "taeter": {
            "männlich": {"<10": 0, "10-19": 404, "20-29": 1318, "30-39": 2370, "40-49": 2034, "50-59": 984,
                         "60-69": 349, "70+": 148},
            "weiblich": {"<10": 0, "10-19": 142, "20-29": 602, "30-39": 955, "40-49": 747, "50-59": 324, "60-69": 101,
                         "70+": 48}
        }
    },
    "2019": {
        "opfer": {
            "männlich": {"<10": 316, "10-19": 437, "20-29": 473, "30-39": 731, "40-49": 656, "50-59": 405, "60-69": 151,
                         "70+": 100},
            "weiblich": {"<10": 306, "10-19": 937, "20-29": 1652, "30-39": 2434, "40-49": 1839, "50-59": 790,
                         "60-69": 243, "70+": 150}
        },
        "taeter": {
            "männlich": {"<10": 0, "10-19": 413, "20-29": 1351, "30-39": 2428, "40-49": 2153, "50-59": 1027,
                         "60-69": 368, "70+": 151},
            "weiblich": {"<10": 0, "10-19": 145, "20-29": 596, "30-39": 1020, "40-49": 803, "50-59": 306, "60-69": 98,
                         "70+": 33}
        }
    },
    "2020": {
        "opfer": {
            "männlich": {"<10": 294, "10-19": 458, "20-29": 442, "30-39": 738, "40-49": 630, "50-59": 389, "60-69": 160,
                         "70+": 98},
            "weiblich": {"<10": 280, "10-19": 912, "20-29": 1546, "30-39": 2300, "40-49": 1695, "50-59": 741,
                         "60-69": 204, "70+": 130}
        },
        "taeter": {
            "männlich": {"<10": 0, "10-19": 333, "20-29": 1287, "30-39": 2403, "40-49": 2075, "50-59": 1051,
                         "60-69": 349, "70+": 140},
            "weiblich": {"<10": 0, "10-19": 110, "20-29": 592, "30-39": 946, "40-49": 743, "50-59": 292, "60-69": 96,
                         "70+": 39}
        }
    },
    "2021": {
        "opfer": {
            "männlich": {"<10": 320, "10-19": 454, "20-29": 464, "30-39": 698, "40-49": 664, "50-59": 410, "60-69": 180,
                         "70+": 118},
            "weiblich": {"<10": 317, "10-19": 910, "20-29": 1506, "30-39": 2291, "40-49": 1722, "50-59": 777,
                         "60-69": 224, "70+": 137}
        },
        "taeter": {
            "männlich": {"<10": 0, "10-19": 358, "20-29": 1240, "30-39": 2294, "40-49": 2052, "50-59": 1035,
                         "60-69": 365, "70+": 167},
            "weiblich": {"<10": 0, "10-19": 132, "20-29": 599, "30-39": 968, "40-49": 761, "50-59": 308, "60-69": 96,
                         "70+": 33}
        }
    },
    "2022": {
        "opfer": {
            "männlich": {"<10": 346, "10-19": 434, "20-29": 467, "30-39": 725, "40-49": 672, "50-59": 422, "60-69": 183,
                         "70+": 126},
            "weiblich": {"<10": 329, "10-19": 932, "20-29": 1535, "30-39": 2378, "40-49": 1749, "50-59": 753,
                         "60-69": 213, "70+": 149}
        },
        "taeter": {
            "männlich": {"<10": 0, "10-19": 389, "20-29": 1268, "30-39": 2395, "40-49": 2089, "50-59": 1048,
                         "60-69": 345, "70+": 170},
            "weiblich": {"<10": 0, "10-19": 122, "20-29": 564, "30-39": 1010, "40-49": 762, "50-59": 307, "60-69": 112,
                         "70+": 43}
        }
    },
    "2023": {
        "opfer": {
            "männlich": {"<10": 352, "10-19": 456, "20-29": 428, "30-39": 738, "40-49": 717, "50-59": 427, "60-69": 168,
                         "70+": 111},
            "weiblich": {"<10": 352, "10-19": 940, "20-29": 1560, "30-39": 2371, "40-49": 1763, "50-59": 773,
                         "60-69": 219, "70+": 148}
        },
        "taeter": {
            "männlich": {"<10": 1, "10-19": 397, "20-29": 1258, "30-39": 2437, "40-49": 2179, "50-59": 1022,
                         "60-69": 384, "70+": 188},
            "weiblich": {"<10": 0, "10-19": 114, "20-29": 580, "30-39": 1012, "40-49": 777, "50-59": 295, "60-69": 101,
                         "70+": 40}
        }
    },
    "2024": {
        "opfer": {
            "männlich": {"<10": 355, "10-19": 482, "20-29": 473, "30-39": 799, "40-49": 735, "50-59": 426, "60-69": 187,
                         "70+": 122},
            "weiblich": {"<10": 354, "10-19": 972, "20-29": 1581, "30-39": 2455, "40-49": 1771, "50-59": 757,
                         "60-69": 212, "70+": 164}
        },
        "taeter": {
            "männlich": {"<10": 1, "10-19": 366, "20-29": 1307, "30-39": 2545, "40-49": 2236, "50-59": 1103,
                         "60-69": 386, "70+": 191},
            "weiblich": {"<10": 0, "10-19": 116, "20-29": 529, "30-39": 1024, "40-49": 760, "50-59": 328, "60-69": 103,
                         "70+": 46}
        }
    }
}

# Jahre für den Slider
years = list(all_data.keys())


# Funktion zum Erstellen eines polaren Plots
def create_polar_plot(data, plot_type, max_value=None):
    """
    Erstellt einen polaren Plot für Opfer oder Täter nach Altersklasse und Geschlecht

    Args:
        data: Dictionary mit Daten für männlich und weiblich
        plot_type: String, entweder 'opfer' oder 'taeter'
        max_value: Optional, maximaler Wert für die Radiusachse

    Returns:
        Plotly Figure-Objekt
    """
    if max_value is None:
        # Maximaler Wert für die Radiusachse
        max_value = max([
            max(data["männlich"].values()),
            max(data["weiblich"].values())
        ])

    # Erstelle Figur mit Polar-Subplot
    fig = go.Figure()

    # Für jedes Geschlecht
    for gender, color in [("männlich", MALE_COLOR), ("weiblich", FEMALE_COLOR)]:
        # Sammle Daten pro Altersklasse
        r_values = [data[gender][age] for age in age_groups]
        # Schließe den Kreis, indem wir zum ersten Punkt zurückkehren
        r_values.append(r_values[0])

        # Sammle Winkel in Grad für jede Altersklasse
        theta_values = [angles_deg[age] for age in age_groups]
        # Schließe den Kreis
        theta_values.append(theta_values[0])

        # Füge Trace hinzu
        fig.add_trace(go.Scatterpolar(
            r=r_values,
            theta=theta_values,
            mode='lines+markers',
            name=gender.capitalize(),
            line=dict(color=color, width=2),
            marker=dict(color=color, size=8),
            fill='toself',
            opacity=0.6
        ))

    # Layout anpassen
    title = "Opfer nach Altersklasse und Geschlecht" if plot_type == "opfer" else "Täter:innen nach Altersklasse und Geschlecht"

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_value * 1.1],  # Füge etwas Platz hinzu
                showticklabels=True,
                ticks='outside',
                showline=True,
                linecolor='lightgray',
                gridcolor='lightgray'
            ),
            angularaxis=dict(
                tickvals=list(angles_deg.values()),
                ticktext=list(angles_deg.keys()),
                direction='clockwise',
                showline=True,
                linecolor='lightgray',
                gridcolor='lightgray'
            ),
            bgcolor='white'
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="white",
            bordercolor="lightgray",
            borderwidth=1
        ),
        margin=dict(l=10, r=10, t=50, b=10),  # Minimale Ränder
        height=450,
    )

    return fig


# Bestimme die maximalen Werte für alle Jahre für konsistente Skalierung
max_opfer_value = max([
    max([
        max(all_data[year]["opfer"]["männlich"].values()),
        max(all_data[year]["opfer"]["weiblich"].values())
    ]) for year in years
])

max_taeter_value = max([
    max([
        max(all_data[year]["taeter"]["männlich"].values()),
        max(all_data[year]["taeter"]["weiblich"].values())
    ]) for year in years
])

# CSS für das Layout
external_stylesheets = []
app.css.append_css({
    'external_url': external_stylesheets
})

# App-Layout
app.layout = html.Div(className='container', style={
    'fontFamily': 'Arial, sans-serif',
    'margin': '0',
    'padding': '20px',
    'backgroundColor': '#f5f5f5',
    'color': '#333',
    'maxWidth': '1200px',
    'marginLeft': 'auto',
    'marginRight': 'auto',
}, children=[
    html.H1("Häusliche Gewalt in der Schweiz (2009-2024)", style={
        'textAlign': 'center',
        'marginBottom': '20px',
        'color': '#444'
    }),

    # Jahr-Anzeige
    html.Div(id='year-display', style={
        'fontSize': '24px',
        'fontWeight': 'bold',
        'textAlign': 'center',
        'margin': '15px 0',
        'color': '#333'
    }),

    # Jahr-Slider
    html.Div(className='slider-container', style={
        'width': '90%',
        'margin': '20px auto 40px auto',
        'textAlign': 'center'
    }, children=[
        dcc.Slider(
            id='year-slider',
            min=0,
            max=len(years) - 1,
            value=0,
            marks={i: year for i, year in enumerate(years)},
            step=None,
        ),
    ]),

    # Legende
    html.Div(className='legend', style={
        'display': 'flex',
        'justifyContent': 'center',
        'margin': '15px 0 30px 0'
    }, children=[
        html.Div(className='legend-item', style={
            'display': 'flex',
            'alignItems': 'center',
            'margin': '0 15px',
            'fontSize': '16px'
        }, children=[
            html.Div(className='legend-color', style={
                'width': '20px',
                'height': '20px',
                'marginRight': '8px',
                'borderRadius': '3px',
                'backgroundColor': MALE_COLOR
            }),
            html.Div(className='legend-label', style={
                'fontSize': '16px'
            }, children=["Männlich"])
        ]),
        html.Div(className='legend-item', style={
            'display': 'flex',
            'alignItems': 'center',
            'margin': '0 15px',
            'fontSize': '16px'
        }, children=[
            html.Div(className='legend-color', style={
                'width': '20px',
                'height': '20px',
                'marginRight': '8px',
                'borderRadius': '3px',
                'backgroundColor': FEMALE_COLOR
            }),
            html.Div(className='legend-label', style={
                'fontSize': '16px'
            }, children=["Weiblich"])
        ])
    ]),

    # Gesamtzahlen
    html.Div(className='total-counts', style={
        'display': 'flex',
        'justifyContent': 'space-around',
        'margin': '20px 0 40px 0'
    }, children=[
        html.Div(className='count-box', style={
            'textAlign': 'center',
            'padding': '15px',
            'borderRadius': '5px',
            'backgroundColor': '#f8f8f8',
            'boxShadow': '0 1px 5px rgba(0, 0, 0, 0.1)',
            'width': '250px'
        }, children=[
            html.Div(className='count-label', style={
                'fontSize': '16px',
                'marginBottom': '8px',
                'fontWeight': 'bold'
            }, children=["Gesamt Opfer"]),
            html.Div(id='total-opfer', className='count-value', style={
                'fontSize': '32px',
                'fontWeight': 'bold'
            })
        ]),
        html.Div(className='count-box', style={
            'textAlign': 'center',
            'padding': '15px',
            'borderRadius': '5px',
            'backgroundColor': '#f8f8f8',
            'boxShadow': '0 1px 5px rgba(0, 0, 0, 0.1)',
            'width': '250px'
        }, children=[
            html.Div(className='count-label', style={
                'fontSize': '16px',
                'marginBottom': '8px',
                'fontWeight': 'bold'
            }, children=["Gesamt Täter:innen"]),
            html.Div(id='total-taeter', className='count-value', style={
                'fontSize': '32px',
                'fontWeight': 'bold'
            })
        ])
    ]),

    # Charts Container
    html.Div(className='charts-container', style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'justifyContent': 'space-around',
        'marginBottom': '30px'
    }, children=[
        html.Div(className='chart-wrapper', style={
            'width': '45%',
            'minWidth': '400px',
            'marginBottom': '20px',
            'padding': '15px',
            'position': 'relative'
        }, children=[
            html.Div(className='chart-title', style={
                'textAlign': 'center',
                'marginBottom': '20px',
                'fontSize': '20px',
                'fontWeight': 'bold',
                'color': '#444'
            }, children=["Opfer nach Altersklasse und Geschlecht ", html.Span(id='opfer-year-title')]),
            dcc.Graph(id='opfer-chart')
        ]),
        html.Div(className='chart-wrapper', style={
            'width': '45%',
            'minWidth': '400px',
            'marginBottom': '20px',
            'padding': '15px',
            'position': 'relative'
        }, children=[
            html.Div(className='chart-title', style={
                'textAlign': 'center',
                'marginBottom': '20px',
                'fontSize': '20px',
                'fontWeight': 'bold',
                'color': '#444'
            }, children=["Täter:innen nach Altersklasse und Geschlecht ", html.Span(id='taeter-year-title')]),
            dcc.Graph(id='taeter-chart')
        ]),
    ]),

    # Footer
            html.Footer(style={
                'textAlign': 'center',
                'marginTop': '40px',
                'color': '#777',
                'fontSize': '14px',
                'padding': '10px'
            }, children=[
                "Datenquelle: Strafgesetzbuch (StGB): Straftaten häusliche Gewalt und beschuldigte/geschädigte Personen"
            ])
        ])

             # Callback-Funktionen zum Aktualisieren der Charts und Zahlen
@app.callback(
    [
        Output('year-display', 'children'),
        Output('opfer-year-title', 'children'),
        Output('taeter-year-title', 'children'),
        Output('total-opfer', 'children'),
        Output('total-taeter', 'children'),
        Output('opfer-chart', 'figure'),
        Output('taeter-chart', 'figure')
    ],
    [Input('year-slider', 'value')]
)


def update_charts(year_index):
    year = years[year_index]
    data = all_data[year]

    # Berechne Gesamtzahlen
    total_opfer = sum([
        sum(data["opfer"]["männlich"].values()),
        sum(data["opfer"]["weiblich"].values())
    ])

    total_taeter = sum([
        sum(data["taeter"]["männlich"].values()),
        sum(data["taeter"]["weiblich"].values())
    ])

    # Formatiere Zahlen im Schweizer Format
    total_opfer_formatted = format(total_opfer, ",").replace(",", "'")
    total_taeter_formatted = format(total_taeter, ",").replace(",", "'")

    # Erstelle die Charts
    opfer_fig = create_polar_plot(data["opfer"], "opfer", max_opfer_value)
    taeter_fig = create_polar_plot(data["taeter"], "taeter", max_taeter_value)

    return (
        year,  # Jahr-Anzeige
        f"({year})",  # Opfer-Chart-Titel Jahr
        f"({year})",  # Täter-Chart-Titel Jahr
        total_opfer_formatted,  # Gesamtzahl Opfer
        total_taeter_formatted,  # Gesamtzahl Täter
        opfer_fig,  # Opfer-Chart
        taeter_fig  # Täter-Chart
    )


# Main
if __name__ == '__main__':
    app.run(debug=True)