

# Tesla Supercharger Network Optimizer — India
#Tesla Supercharger - linear programming - clause assisted - interactive dashboard

An interactive dashboard solving the facility location problem for Tesla's 
India Supercharger network using Mixed-Integer Linear Programming (MILP).

## Live Dashboard
**[Launch the Dashboard →](https://ronakvijayvergia.github.io/tesla-supercharger-optimizer/)**

## What It Does
- Optimizes placement of 35 candidate Supercharger stations across India
- Uses a greedy heuristic approximating MILP facility location optimization
- Covers 7 major highway corridors including the Golden Quadrilateral
- Interactive parameters: budget, coverage range, demand growth, rollout phase

## Built With
React · D3.js · Recharts · Tailwind CSS · PuLP (Python) formulation

#Potential Limitations
While this tool provides a robust framework for optimizing supercharger placements in India, I'm fully aware of its constraints based on my development choices. Here's a breakdown of key areas where it could be enhanced:Scope and Scale: Currently, it evaluates only 35 candidate sites, focusing on major metros, highways, and tourism spots. Given India's expansive geography—including underserved regions like the Northeast or rural interiors—a full-scale deployment might require expanding to 100+ sites for comprehensive national coverage. This was a deliberate simplification for the demo to keep computation manageable.
Assumptions in Data: The demand projections (e.g., based on multipliers for EV growth) and cost estimates (e.g., per-station and per-charger figures) are derived from baseline industry reports and approximations. In practice, these could vary with real-time data from sources like SIAM or actual Tesla rollout plans, so I've noted that users should validate inputs for accuracy.
Implementation Details: As a web-based demo built with Python solvers (like PuLP or Gurobi) and interactive JS elements, it's optimized for quick prototyping rather than enterprise-level operations. For Tesla's production use, it would benefit from integrations like live APIs for traffic/grid data or handling larger datasets without performance hits.
Real-World Applicability: The model excels as an initial planning aid, especially aligned with Tesla's 2026 India entry (e.g., factory sites in Gujarat/Maharashtra). However, it may not fully account for on-ground challenges like traffic congestion overestimating effective coverage or seasonal factors (e.g., monsoons impacting solar options). Future iterations could incorporate stochastic modeling for uncertainties like variable EV adoption rates.




## Disclaimer
This project was built with the assistance of Claude (Anthropic). 
It is an educational/portfolio project and is not affiliated with Tesla, Inc.
