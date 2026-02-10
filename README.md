# Tesla Supercharger Network Optimizer — India

Interactive dashboard for the **facility location problem** applied to Tesla's Supercharger network rollout across India. ( If ever Tesla decides to roll-out) 

**Two components **
- **`index.html`** — Browser-based dashboard with a **greedy heuristic** for real-time interactivity
- **`solver/tesla_supercharger_milp.py`** — Exact **MILP solver** using PuLP + CBC that finds provably optimal solutions offline

**[Live Dashboard →](https://ronakvijayvergia.github.io/tesla-supercharger-optimizer/)**

> *This project was built with the assistance of Claude (Anthropic). The concept, problem framing, and direction are mine; the code and content were AI-generated. I do not claim intellectual ownership over the AI-generated portions.*

## How It Works

### Live Dashboard — Greedy Heuristic (`index.html`)

The browser runs a **JavaScript scoring algorithm** for instant feedback as you adjust sliders:
- Cities are scored by demand, grid capacity, type (metro/highway/tourism), and highway proximity
- Highest-scoring cities are selected greedily within the budget constraint
- Coverage, demand satisfaction, and highway connectivity are recomputed in real time

This is a **heuristic** — it finds good solutions fast, but not necessarily the mathematical optimum.

### Python Solver — Exact MILP (`solver/tesla_supercharger_milp.py`)

The Python file formulates and solves the **exact Mixed-Integer Linear Program**:
- **Objective**: Maximize total demand served
- **Decision variables**: 35 binary build decisions + 87 binary assignment variables
- **Constraints**: Budget cap, coverage range, minimum stations, single-assignment per demand point
- **Solver**: PuLP with CBC (open-source, bundled) — also compatible with Gurobi/CPLEX
- Finds the **provably optimal** solution (not an approximation)

```bash
pip install pulp
python solver/tesla_supercharger_milp.py --budget 1500 --range 250 --min-stations 10
```

Sample output:
```
Status: Optimal
Stations built:    21 / 35
Total investment:  ₹1180 Cr
Cities covered:    35 / 35 (100%)
Demand served:     7,380 / 7,380 (100%)
```

## Features

- **India map** with district-level boundaries (D3-geo + GeoJSON, 759 districts, 36 states/UTs)
- **35 candidate cities** with real geographic coordinates, demand estimates, grid capacity, and construction costs
- **7 highway corridors** (Golden Quadrilateral + major national highways)
- **Parameter controls**: budget, coverage range, minimum stations, demand growth multiplier
- **Strategy toggles**: rollout phases (Tier 1/2/3), highway prioritization, solar integration bonus
- **5-tab dashboard**: Network Map, Analysis, Corridors, Projection, MILP Model
- **Hover tooltips** explaining every KPI card and parameter

## Tech Stack

| Component | Technology | Runs Where |
|-----------|-----------|------------|
| Dashboard UI | React 18, Tailwind CSS | Browser (CDN) |
| Map rendering | D3.js (geoMercator projection) | Browser (CDN) |
| Charts | Recharts | Browser (CDN) |
| JSX compilation | Babel standalone | Browser (CDN) |
| Greedy solver | Vanilla JavaScript | Browser |
| MILP solver | PuLP + CBC (Python) | Offline / CLI |

The dashboard is a **single self-contained HTML file** — zero build step, no server required.
The Python solver is a **standalone script** — `pip install pulp` and run.

## Repo Structure

```
├── index.html                          # Interactive dashboard (deploy to GitHub Pages)
├── solver/
│   └── tesla_supercharger_milp.py      # Exact MILP solver (run offline with Python)
└── README.md
```

## Deploy the Dashboard

1. Fork this repo
2. Go to **Settings → Pages → Source → main**
3. Your dashboard is live at `https://your-username.github.io/tesla-supercharger-optimizer/`

## Limitations

- **Scope**: 35 candidate cities — India's vast geography may need 100+ for full rural coverage
- **Data**: Demand estimates and costs are baseline approximations, not sourced from real market data
- **Heuristic vs optimal**: The live dashboard uses a greedy heuristic; the Python solver finds the exact optimum but runs offline
- **Static model**: No stochastic elements (variable EV adoption), multi-period planning (year-over-year expansion), or grid reliability modeling
- **No real-time data**: Doesn't integrate live traffic APIs, grid status feeds, or weather impact

## License

MIT
