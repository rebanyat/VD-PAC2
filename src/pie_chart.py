"""
Pie Chart — Formes d'OVNIs reportats al NUFORC.
Gràfic circular amb temàtica còsmica que mostra la distribució de formes d'OVNIs.
Sense forat central (pie chart pur, no donut).
"""

import pandas as pd
import plotly.graph_objects as go
import os

BASE = os.path.dirname(__file__)
DADES = os.path.join(BASE, "..", "datasets_clean", "ufo_shapes.csv")
SORTIDA = os.path.join(BASE, "..", "docs", "pie_chart.html")

df = pd.read_csv(DADES)
total = df["count"].sum()

# Traducció de les formes (originals en anglès al dataset) al català
TRADUCCIONS = {
    "Light": "Llum",
    "Triangle": "Triangle",
    "Circle": "Cercle",
    "Fireball": "Bola de foc",
    "Other": "Indefinit",
    "Unknown": "Desconegut",
    "Sphere": "Esfera",
    "Disk": "Disc",
    "Oval": "Oval",
    "Formation": "Formació",
    "Altres": "Diverses formes",
}
df["shape"] = df["shape"].map(lambda s: TRADUCCIONS.get(s, s))

# Paleta de colors temàtica — cada color evoca la forma que representa
# Colors ben diferenciats entre adjacents per màxima llegibilitat
colors = [
    "#f5e642",  # Light     — groc elèctric, resplendor
    "#00c853",  # Triangle  — verd neó, misteriós
    "#2979ff",  # Circle    — blau intens, cel nocturn
    "#ff3d00",  # Fireball  — vermell foc, explosiu
    "#e91e63",  # Other     — rosa fort, inclassificable
    "#00bcd4",  # Unknown   — cian glacial, incert
    "#9c27b0",  # Sphere    — porpra profund
    "#c6ff00",  # Disk      — verd llima, metàl·lic
    "#ff6f00",  # Oval      — ambre càlid
    "#f48fb1",  # Formation — rosa suau, constel·lació
    "#546e7a",  # Altres    — gris blavós apagat
]

# Ressaltar la forma més freqüent amb un lleuger pull-out
pull = [0.05] + [0] * (len(df) - 1)

fig = go.Figure(
    data=[
        go.Pie(
            labels=df["shape"],
            values=df["count"],
            hole=0,  # Pie chart pur, sense forat
            pull=pull,
            marker=dict(
                colors=colors,
                line=dict(color="#0d1117", width=2),
            ),
            textinfo="label+percent",
            textfont=dict(size=13, color="white"),
            textposition="outside",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Avistaments: %{value:,.0f}<br>"
                "Proporció: %{percent}<extra></extra>"
            ),
            direction="clockwise",
            sort=False,
        )
    ]
)

fig.update_layout(
    title=dict(
        text=(
            "<b>Formes d'OVNIs reportats als Estats Units</b>"
            "<br><span style='font-size:14px;color:#8b949e'>"
            "Distribució de 78.400 avistaments registrats al NUFORC (1949–2014)</span>"
        ),
        x=0.5,
        font=dict(size=22, color="white", family="Open Sans"),
    ),
    paper_bgcolor="#0d1117",
    plot_bgcolor="#0d1117",
    font=dict(color="white", family="Open Sans"),
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        font=dict(size=13),
        bgcolor="rgba(0,0,0,0)",
    ),
    margin=dict(t=100, b=80, l=40, r=160),
    width=900,
    height=650,
    annotations=[
        # Font de dades — a baix a l'esquerra, fora de l'àrea del gràfic
        dict(
            text="Font: NUFORC (National UFO Reporting Center) via Kaggle",
            xref="paper",
            yref="paper",
            x=-0.02,
            y=-0.1,
            xanchor="left",
            showarrow=False,
            font=dict(size=11, color="#8b949e"),
        ),
    ],
)

os.makedirs(os.path.dirname(SORTIDA), exist_ok=True)
fig.write_html(SORTIDA, include_plotlyjs=True)
print(f"✓ Pie chart desat a {SORTIDA}")
