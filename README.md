# PAC 2 — Visualització de Dades

Projecte de la PAC 2 de l'assignatura de **Visualització de Dades** de la UOC.

## Visualitzacions

Tres tècniques implementades amb Python + Plotly, publicades a GitHub Pages:

| Tècnica | Dataset | Descripció |
|---|---|---|
| **Pie Chart** | NUFORC | Formes d'OVNIs reportats als EUA (1949–2014) |
| **Nightingale Rose Chart** | FAA | Impactes d'aus contra aeronaus per mes (2000–2011) |
| **Bump Chart** | FAO / Our World in Data | Rànking de consum de xocolata per càpita (1990–2023) |

## Estructura

```
├── src/                  # Scripts Python de neteja i visualització
│   ├── clean_data.py
│   ├── pie_chart.py
│   ├── nightingale.py
│   └── bump_chart.py
├── datasets_clean/       # Datasets nets (CSV)
└── docs/                 # Visualitzacions HTML (GitHub Pages)
    ├── index.html
    ├── pie_chart.html
    ├── nightingale.html
    └── bump_chart.html
```

## Com executar

```bash
pip install plotly pandas numpy
python src/clean_data.py
python src/pie_chart.py
python src/nightingale.py
python src/bump_chart.py
```

## Eines

- Python 3.x · Plotly · Pandas · NumPy
- GitHub Pages per a la publicació
