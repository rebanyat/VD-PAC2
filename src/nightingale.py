"""
Nightingale Rose Chart — Impactes d'aus contra aeronaus per mes (FAA).
Gràfic polar de barres (coxcomb) amb temàtica de cel i aus.

Nota tècnica important:
  En un Nightingale Rose Chart, és l'ÀREA del segment (no el radi)
  la que representa el valor. Com que àrea = π·r²·(θ/2), i tots els
  segments tenen el mateix angle θ, l'àrea és proporcional a r².
  Per tant, per representar fidelment les dades cal aplicar:
      r = √incidents
  Així l'àrea serà proporcional al nombre real d'incidents.
  El valor real s'exposa al tooltip via 'customdata'.
"""

import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os

BASE = os.path.dirname(__file__)
DADES = os.path.join(BASE, "..", "datasets_clean", "bird_strikes_monthly.csv")
DADES_DANYS = os.path.join(BASE, "..", "datasets_clean", "bird_strikes_monthly_damage.csv")
SORTIDA = os.path.join(BASE, "..", "docs", "nightingale.html")

df = pd.read_csv(DADES)
df_danys = pd.read_csv(DADES_DANYS)

# Separar categories de danys
sense_danys = df_danys[df_danys["Damage"] == "No damage"].sort_values("month")
amb_danys = df_danys[df_danys["Damage"] == "Caused damage"].sort_values("month")

# Noms dels mesos en català (per a l'eix angular)
mesos_ca = [
    "Gener", "Febrer", "Març", "Abril", "Maig", "Juny",
    "Juliol", "Agost", "Setembre", "Octubre", "Novembre", "Desembre",
]

# Gradient de colors estacional:
colors_estacionals = [
    "#90caf9",  
    "#80deea",
    "#a5d6a7",
    "#c5e1a5",
    "#e6ee9c",
    "#fff59d", 
    "#ffcc80",  
    "#ffab91",  
    "#ef9a9a", 
    "#ce93d8",  
    "#b39ddb", 
    "#9fa8da",  
]

# Colors foscos per mes per a la capa de danys
colors_danys = [
    "#1565c0",
    "#00838f",
    "#2e7d32",
    "#558b2f",
    "#9e9d24",
    "#f9a825",
    "#ef6c00",
    "#d84315",
    "#c62828",
    "#7b1fa2",
    "#4527a0",
    "#283593",
]

# Transformació de radi: r = √incidents perquè l'ÀREA sigui proporcional al valor
# Sense aquesta transformació, l'àrea creixeria al quadrat i exageraria les diferències
r_sense_danys = np.sqrt(sense_danys["incidents"].values)
r_amb_danys = np.sqrt(amb_danys["incidents"].values)

fig = go.Figure()

# Capa 1: Sense danys 
fig.add_trace(
    go.Barpolar(
        r=r_sense_danys,
        theta=mesos_ca,
        name="Sense danys",
        customdata=sense_danys["incidents"].values,  # valor real per al tooltip
        marker=dict(
            color=colors_estacionals,
            line=dict(color="rgba(255,255,255,0.4)", width=1),
        ),
        opacity=0.9,
        hovertemplate=(
            "<b>%{theta}</b><br>"
            "Incidents sense danys: %{customdata:,.0f}<extra></extra>"
        ),
    )
)

# Capa 2: Amb danys a l'aeronau
fig.add_trace(
    go.Barpolar(
        r=r_amb_danys,
        theta=mesos_ca,
        name="Amb danys a l'aeronau",
        customdata=amb_danys["incidents"].values,  # valor real per al tooltip
        marker=dict(
            color=colors_danys,
            line=dict(color="rgba(255,255,255,0.5)", width=1.5),
        ),
        opacity=0.85,
        hovertemplate=(
            "<b>%{theta}</b><br>"
            "Incidents amb danys: %{customdata:,.0f}<extra></extra>"
        ),
    )
)

fig.update_layout(
    title=dict(
        text=(
            "<b>Impactes d'aus contra aeronaus per mes</b>"
            "<br><span style='font-size:14px;color:#546e7a'>"
            "25.429 incidents registrats per la FAA (2000–2011) · "
            "Patró estacional lligat a la migració d'aus</span>"
        ),
        x=0.5,
        font=dict(size=20, color="#263238", family="Open Sans"),
    ),
    # Fons de cel clar
    paper_bgcolor="#e8eef4",
    font=dict(color="#263238", family="Open Sans"),
    polar=dict(
        bgcolor="rgba(255,255,255,0.3)",
        angularaxis=dict(
            direction="clockwise",
            rotation=90,  # Començar des de dalt
            tickfont=dict(size=13, color="#37474f", family="Open Sans"),
            gridcolor="rgba(0,0,0,0.05)",
            linecolor="rgba(0,0,0,0.1)",
        ),
        radialaxis=dict(
            visible=False,  # Ocultar l'eix radial —
        ),
    ),
    # Llegenda horitzontal sota el gràfic
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.08,
        xanchor="center",
        x=0.5,
        font=dict(size=13),
        bgcolor="rgba(0,0,0,0)",
        itemsizing="constant",
    ),
    margin=dict(t=110, b=160, l=60, r=60),
    width=800,
    height=820,
    annotations=[
        # Anotació del pic màxim
        dict(
            text="<b>Pic: Agost</b><br>3.710 incidents",
            x=0.85,
            y=0.85,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=12, color="#d84315"),
            bgcolor="rgba(216,67,21,0.08)",
            bordercolor="#d84315",
            borderwidth=1,
            borderpad=6,
        ),
        # Anotació del mínim
        dict(
            text="<b>Mínim: Febrer</b><br>772 incidents",
            x=0.15,
            y=0.85,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=12, color="#1565c0"),
            bgcolor="rgba(21,101,192,0.08)",
            bordercolor="#1565c0",
            borderwidth=1,
            borderpad=6,
        ),
        # Nota metodològica 
        dict(
            text="L'àrea de cada segment és proporcional al nombre d'incidents (r = √n)",
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.15,
            xanchor="center",
            showarrow=False,
            font=dict(size=11, color="#546e7a", family="Open Sans"),
        ),
        # Font de dades 
        dict(
            text="Font: FAA Wildlife Strike Database via Kaggle",
            xref="paper",
            yref="paper",
            x=0,
            y=-0.19,
            xanchor="left",
            showarrow=False,
            font=dict(size=10, color="#90a4ae"),
        ),
        # Referència històrica
        dict(
            text="Inspirat en la Rosa de Nightingale (Florence Nightingale, 1858)",
            xref="paper",
            yref="paper",
            x=1,
            y=-0.19,
            xanchor="right",
            showarrow=False,
            font=dict(size=10, color="#90a4ae", family="Open Sans"),
        ),
    ],
)

os.makedirs(os.path.dirname(SORTIDA), exist_ok=True)
fig.write_html(SORTIDA, include_plotlyjs=True)
print(f"✓ Nightingale chart desat a {SORTIDA}")
