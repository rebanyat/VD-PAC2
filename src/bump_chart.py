"""
Bump Chart — Top 10 de països per consum de xocolata per càpita (1990–2023).
Gràfic de línies amb eix Y invertit, temàtica xocolata.

Estil inspirat en bump charts clàssics: línies fines i suaus,
etiquetes amb rànking a banda i banda, sense marcadors intermedis.

Interactivitat:
  - Top 3 comencen amb opacitat plena, la resta difuminada.
  - Clic a la llegenda: ressalta el país (mai desapareix).
  - Doble clic: restaura l'estat inicial.
"""

import pandas as pd
import plotly.graph_objects as go
import os

BASE = os.path.dirname(__file__)
DADES = os.path.join(BASE, "..", "datasets_clean", "chocolate_rankings.csv")
SORTIDA = os.path.join(BASE, "..", "docs", "bump_chart.html")

df = pd.read_csv(DADES)

# Ordre fixe dels països (de major a menor consum mitjà)
ORDRE_PAISOS = [
    "Luxembourg", "Iceland", "Estonia", "Cote d'Ivoire",
    "Denmark", "France", "Norway", "Slovenia", "Israel", "United Kingdom",
]

# Top 3 per consum mitjà — comencen destacats
TOP_3 = {"Luxembourg", "Iceland", "Estonia"}

# Opacitats inicials
OPACITAT_DESTACAT = 1.0
OPACITAT_DIFUMINAT = 0.2

# Paleta de colors molt diferenciats — un per rang cromàtic
# Cada país té un to clarament distint dels veïns
COLORS_PAISOS = {
    "Luxembourg":    "#c0392b",  # vermell
    "Iceland":       "#2471a3",  # blau cobalt
    "Estonia":       "#1e8449",  # verd bosc
    "Cote d'Ivoire": "#d4ac0d",  # groc daurat (productor cacau!)
    "Denmark":       "#a04000",  # taronja terra
    "France":        "#7d3c98",  # porpra
    "Norway":        "#117a65",  # verd teal
    "Slovenia":      "#d35400",  # taronja cremat
    "Israel":        "#1a5276",  # blau marí
    "United Kingdom":"#626567",  # gris antracita
}

NOMS_PAISOS = {
    "Luxembourg":    "Luxemburg",
    "Iceland":       "Islàndia",
    "Estonia":       "Estònia",
    "Cote d'Ivoire": "Costa d'Ivori",
    "Denmark":       "Dinamarca",
    "France":        "França",
    "Norway":        "Noruega",
    "Slovenia":      "Eslovènia",
    "Israel":        "Israel",
    "United Kingdom":"Regne Unit",
}

fig = go.Figure()

opacitats_inicials = []

for pais in ORDRE_PAISOS:
    df_pais = df[df["Entity"] == pais].sort_values("Year")
    color = COLORS_PAISOS[pais]
    nom = NOMS_PAISOS[pais]
    es_top3 = pais in TOP_3
    opacitat = OPACITAT_DESTACAT if es_top3 else OPACITAT_DIFUMINAT
    opacitats_inicials.append(opacitat)

    # Mides dels marcadors: grans als extrems (inici/final), invisibles al mig
    n = len(df_pais)
    mides = [9 if (i == 0 or i == n - 1) else 0 for i in range(n)]

    fig.add_trace(
        go.Scatter(
            x=df_pais["Year"],
            y=df_pais["rank"],
            mode="lines+markers",
            name=nom,
            opacity=opacitat,
            line=dict(
                color=color,
                width=3 if es_top3 else 2,
                shape="spline",
                smoothing=1.3,
            ),
            marker=dict(
                size=mides,
                color=color,
                line=dict(color="white", width=2),
            ),
            hovertemplate=(
                f"<b>{nom}</b><br>"
                "Any: %{x}<br>"
                "Posició: #%{y}<br>"
                "Consum: %{customdata:.2f} kg/càpita<extra></extra>"
            ),
            customdata=df_pais["kg_per_capita"],
        )
    )

    # Etiqueta esquerra: "País #N" (rànking inicial)
    primer = df_pais.iloc[0]
    fig.add_annotation(
        x=primer["Year"] - 0.6,
        y=primer["rank"],
        text=f"<b>{nom}</b> #{int(primer['rank'])}",
        showarrow=False,
        font=dict(size=10, color=color, family="Open Sans"),
        xanchor="right",
        opacity=opacitat,
    )

    # Etiqueta dreta: "#N País" (rànking final)
    ultim = df_pais.iloc[-1]
    fig.add_annotation(
        x=ultim["Year"] + 0.6,
        y=ultim["rank"],
        text=f"#{int(ultim['rank'])} <b>{nom}</b>",
        showarrow=False,
        font=dict(size=10, color=color, family="Open Sans"),
        xanchor="left",
        opacity=opacitat,
    )

fig.update_layout(
    title=dict(
        text=(
            "<b>Rànking de consum de xocolata per càpita</b>"
            "<br><span style='font-size:14px;color:#6d4c41'>"
            "Evolució dels 10 principals països consumidors de cacau (1990–2023) · "
            "kg per persona/any</span>"
        ),
        x=0.5,
        font=dict(size=20, color="#3e2723", family="Open Sans"),
    ),
    xaxis=dict(
        side="top",  # anys a dalt, com a la referència
        tickfont=dict(size=13, color="#5d4037", family="Open Sans"),
        gridcolor="rgba(78,52,46,0.06)",
        dtick=2,
        range=[1985, 2028],
        zeroline=False,
        showline=False,
    ),
    yaxis=dict(
        autorange="reversed",
        tickvals=list(range(1, 11)),
        ticktext=[f"#{i}" for i in range(1, 11)],
        tickfont=dict(size=11, color="#a1887f"),
        gridcolor="rgba(78,52,46,0.06)",
        range=[0.3, 10.7],
        zeroline=False,
        showline=False,
        title="",
    ),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="#3e2723", family="Open Sans"),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.12,
        xanchor="center",
        x=0.5,
        font=dict(size=11),
        bgcolor="rgba(0,0,0,0)",
        # El comportament per defecte es prevé des del JS (return false)
        itemclick="toggle",
        itemdoubleclick="toggleothers",
    ),
    margin=dict(t=130, b=130, l=130, r=140),
    width=1100,
    height=650,
    hovermode="x unified",
    annotations=[
        dict(
            text="Clic a la llegenda per ressaltar · Doble clic per restaurar",
            xref="paper", yref="paper",
            x=1, y=-0.22, xanchor="right",
            showarrow=False,
            font=dict(size=10, color="#a1887f", family="Open Sans"),
        ),
        dict(
            text="Font: FAO via Our World in Data",
            xref="paper", yref="paper",
            x=0, y=-0.22, xanchor="left",
            showarrow=False,
            font=dict(size=10, color="#a1887f"),
        ),
    ],
)

# ─────────────────────────────────────────────────────────────
# JavaScript personalitzat per a la interactivitat d'opacitat
# ─────────────────────────────────────────────────────────────
JS_PERSONALITZAT = f"""
<script>
(function() {{
    var interval = setInterval(function() {{
        var gd = document.querySelector('.plotly-graph-div');
        if (!gd || !gd._fullData) return;
        clearInterval(interval);

        var numTraces = {len(ORDRE_PAISOS)};
        var opInicial = {opacitats_inicials};
        var opAlta    = {OPACITAT_DESTACAT};
        var opMinima  = 0.08;
        var seleccionats = new Set();

        function aplicarOpacitats() {{
            var novaOpacitat = [];
            for (var i = 0; i < numTraces; i++) {{
                if (seleccionats.size === 0) {{
                    novaOpacitat.push(opInicial[i]);
                }} else if (seleccionats.has(i)) {{
                    novaOpacitat.push(opAlta);
                }} else {{
                    novaOpacitat.push(opMinima);
                }}
            }}
            Plotly.restyle(gd, {{ opacity: novaOpacitat }}, [...Array(numTraces).keys()]);
        }}

        gd.on('plotly_legendclick', function(eventData) {{
            var idx = eventData.curveNumber;
            if (seleccionats.has(idx)) {{
                seleccionats.delete(idx);
            }} else {{
                seleccionats.add(idx);
            }}
            aplicarOpacitats();
            return false;
        }});

        gd.on('plotly_legenddoubleclick', function(eventData) {{
            seleccionats.clear();
            aplicarOpacitats();
            return false;
        }});

        // Hover: ressaltar la línia sobre la qual passa el cursor
        gd.on('plotly_hover', function(eventData) {{
            var idx = eventData.points[0].curveNumber;
            var amplades = [];
            for (var i = 0; i < numTraces; i++) {{
                amplades.push(i === idx ? 5 : gd.data[i].line.width);
            }}
            Plotly.restyle(gd, {{'line.width': amplades}}, [...Array(numTraces).keys()]);
        }});

        gd.on('plotly_unhover', function() {{
            var amplades = [];
            for (var i = 0; i < numTraces; i++) {{
                amplades.push(gd.data[i].line.width);
            }}
            // Restaurar amplades originals (3 per top3, 2 per resta)
            var ampladesOriginals = {[3 if p in TOP_3 else 2 for p in ORDRE_PAISOS]};
            Plotly.restyle(gd, {{'line.width': ampladesOriginals}}, [...Array(numTraces).keys()]);
        }});
    }}, 100);
}})();
</script>
"""

os.makedirs(os.path.dirname(SORTIDA), exist_ok=True)
html_brut = fig.to_html(include_plotlyjs=True, full_html=True)
html_final = html_brut.replace("</body>", JS_PERSONALITZAT + "\n</body>")

with open(SORTIDA, "w", encoding="utf-8") as f:
    f.write(html_final)

print(f"✓ Bump chart desat a {SORTIDA}")
