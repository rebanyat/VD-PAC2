"""
Script de neteja de dades per a la PAC2 — Visualització de Dades.
Llegeix els CSVs originals i genera datasets nets, preparats per visualitzar.
"""

import pandas as pd
import os

DIR_SORTIDA = os.path.join(os.path.dirname(__file__), "..", "datasets_clean")
os.makedirs(DIR_SORTIDA, exist_ok=True)

# ─────────────────────────────────────────────
# 1. Avistaments d'OVNIs → Pie Chart
# ─────────────────────────────────────────────
print("Netejant avistaments d'OVNIs...")
ovnis = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "..", "Datasets", "OVNIs", "scrubbed.csv"),
    low_memory=False,
)

# Eliminar files sense forma reportada
ovnis = ovnis.dropna(subset=["shape"])

# Comptar per forma
recompte_formes = ovnis["shape"].value_counts().reset_index()
recompte_formes.columns = ["shape", "count"]

# Quedar-se amb les top 10 formes, agrupar la resta com "Altres"
TOP_N = 10
top_formes = recompte_formes.head(TOP_N).copy()
recompte_altres = recompte_formes.iloc[TOP_N:]["count"].sum()
fila_altres = pd.DataFrame([{"shape": "altres", "count": recompte_altres}])
ovnis_net = pd.concat([top_formes, fila_altres], ignore_index=True)

# Capitalitzar noms de formes per a la visualització
ovnis_net["shape"] = ovnis_net["shape"].str.capitalize()

ovnis_net.to_csv(os.path.join(DIR_SORTIDA, "ufo_shapes.csv"), index=False)
print(f"  → Desat ufo_shapes.csv ({len(ovnis_net)} files)")
print(ovnis_net.to_string(index=False))

# ─────────────────────────────────────────────
# 2. Impactes d'aus a avions → Nightingale Rose Chart
# ─────────────────────────────────────────────
print("\nNetejant impactes d'aus...")
aus = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "..", "Datasets", "Bird_strikes.csv"),
    low_memory=False,
)

# Parsejar data i extreure el mes
aus["FlightDate"] = pd.to_datetime(aus["FlightDate"], format="mixed")
aus["month"] = aus["FlightDate"].dt.month

# Comptar incidents per mes
recompte_mensual = aus.groupby("month").size().reset_index(name="incidents")

# Afegir noms dels mesos en català
MESOS_CA = [
    "Gener", "Febrer", "Març", "Abril", "Maig", "Juny",
    "Juliol", "Agost", "Setembre", "Octubre", "Novembre", "Desembre",
]
recompte_mensual["month_name"] = recompte_mensual["month"].map(
    lambda m: MESOS_CA[m - 1]
)

# Desglossament per danys per a una visualització més rica
danys_per_mes = (
    aus.groupby(["month", "Damage"])
    .size()
    .reset_index(name="incidents")
)
danys_per_mes["month_name"] = danys_per_mes["month"].map(
    lambda m: MESOS_CA[m - 1]
)

recompte_mensual.to_csv(os.path.join(DIR_SORTIDA, "bird_strikes_monthly.csv"), index=False)
danys_per_mes.to_csv(os.path.join(DIR_SORTIDA, "bird_strikes_monthly_damage.csv"), index=False)
print(f"  → Desat bird_strikes_monthly.csv ({len(recompte_mensual)} files)")
print(f"  → Desat bird_strikes_monthly_damage.csv ({len(danys_per_mes)} files)")
print(recompte_mensual.to_string(index=False))

# ─────────────────────────────────────────────
# 3. Consum de xocolata → Bump Chart
# ─────────────────────────────────────────────
print("\nNetejant consum de xocolata...")
xoco = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "..", "Datasets", "chocolate",
                 "chocolate-consumption-per-person.csv"),
)

# Reanomenar la columna llarga de consum
xoco = xoco.rename(columns={xoco.columns[-1]: "kg_per_capita"})

# Eliminar regions agregades (grups FAO, continents, etc.)
paraules_agregats = ["(FAO)", "World", "European Union", "income", "Developing",
                     "Importing", "Locked"]
continents = ["Africa", "Asia", "Europe", "Oceania", "South America",
              "Northern America", "Americas"]

mascara = xoco["Entity"].apply(
    lambda x: not any(pw in str(x) for pw in paraules_agregats)
    and x not in continents
)
xoco = xoco[mascara].copy()

# Filtrar 1990-2023 per un bump chart més net
xoco = xoco[(xoco["Year"] >= 1990) & (xoco["Year"] <= 2023)]

# Excloure nacions/territoris petits amb dades per càpita distorsionades
nacions_petites = [
    "Dominica", "Netherlands Antilles", "Bahrain", "Malta", "Bermuda",
    "Antigua and Barbuda", "Saint Lucia", "Grenada", "Barbados",
    "Trinidad and Tobago", "Suriname", "Cabo Verde", "Sao Tome and Principe",
    "Vanuatu", "New Caledonia", "French Polynesia", "Montenegro", "Samoa",
    "Saint Vincent and the Grenadines",
]
xoco = xoco[~xoco["Entity"].isin(nacions_petites)]

# Top 10 països per consum mitjà
consum_mitja = (
    xoco.groupby("Entity")["kg_per_capita"]
    .mean()
    .nlargest(10)
    .index.tolist()
)
print(f"  Top 10 països per consum mitjà: {consum_mitja}")

xoco_top = xoco[xoco["Entity"].isin(consum_mitja)].copy()

# Calcular rànking per any (1 = consum més alt)
xoco_top["rank"] = (
    xoco_top.groupby("Year")["kg_per_capita"]
    .rank(method="min", ascending=False)
    .astype(int)
)

xoco_top = xoco_top.sort_values(["Year", "rank"])

xoco_top.to_csv(os.path.join(DIR_SORTIDA, "chocolate_rankings.csv"), index=False)
print(f"  → Desat chocolate_rankings.csv ({len(xoco_top)} files)")
print(f"\n  Mostra (2023):")
print(xoco_top[xoco_top["Year"] == 2023][["Entity", "kg_per_capita", "rank"]].to_string(index=False))

print("\n✓ Tots els datasets netejats i desats a datasets_clean/")
