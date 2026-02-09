# Tesla Supercharger Network Optimizer — India

Interactive dashboard for the **facility location problem** applied to Tesla's Supercharger network rollout across India.

The live dashboard runs a **greedy heuristic** for real-time interactivity. A formal **MILP (Mixed-Integer Linear Programming)** formulation with PuLP (Python) code is included as a reference for offline exact solving with production-grade solvers.

**[Live Demo →](https://ronakvijayvergia.github.io/tesla-supercharger-optimizer/)**

> *This project was built with the assistance of Claude (Anthropic). The concept, problem framing, and direction are mine; the code and content were AI-generated. I do not claim intellectual ownership over the AI-generated portions.*

## Features

- **Accurate India map** with district-level boundaries using D3-geo + GeoJSON (759 districts, 36 states/UTs)
- **Real-time greedy solver** — scores and ranks 35 candidate cities by demand, grid capacity, highway connectivity, and more
- **Parameter controls**: budget, coverage range, minimum stations, demand growth
- **Strategy toggles**: rollout phases, highway prioritization, solar integration
- **5-tab dashboard**: Network Map, Analysis, Corridors, Projection, MILP Model
- **Hover tooltips** explaining every KPI and parameter
- **MILP reference formulation** — formal mathematical model with PuLP (Python) code you can copy and run offline

## How It Works

### Live Dashboard (Greedy Heuristic)
The browser-based solver uses a **greedy scoring algorithm** for instant interactivity:
- Cities are scored by demand, grid capacity, type (metro/highway/tourism), and highway corridor proximity
- The solver selects the highest-scoring cities within the budget constraint
- Coverage, demand satisfaction, and highway connectivity are computed in real time

### MILP Reference (Exact Solver)
The **MILP Model tab** provides the formal optimization formulation:
- **Objective**: Minimize total cost (fixed site costs + variable charger costs)
- **Constraints**: Budget cap, coverage range, minimum station count, capacity limits
- **Implementation**: PuLP (Python) code ready to run with CBC, Gurobi, or CPLEX for provably optimal solutions
- The heuristic approximates this model; the MILP finds the exact optimum

## Tech Stack

Single self-contained HTML file — zero build step:

- React 18 (CDN)
- D3.js (CDN) — geographic projection + GeoJSON rendering
- Recharts (CDN) — data visualizations
- Tailwind CSS (CDN)
- Babel standalone (CDN)

## Deploy

1. Fork this repo
2. Go to **Settings → Pages → Source → main**
3. Your dashboard is live at `https://your-username.github.io/tesla-supercharger-optimizer/`

## Limitations

- **Scope**: Limited to 35 candidate cities — India's vast size may need 100+ for full coverage
- **Data**: Demand estimates and costs are baseline approximations, not sourced from real market data
- **Solver**: The live dashboard uses a heuristic, not an exact MILP solver — results are good approximations but not provably optimal
- **Dynamic factors**: Doesn't model grid reliability, monsoon impact on solar, or multi-period year-over-year expansion

## License

MIT
