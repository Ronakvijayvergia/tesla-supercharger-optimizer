"""
Tesla Supercharger Network Optimizer — India
MILP (Mixed-Integer Linear Programming) Facility Location Solver

This is the exact mathematical formulation that the interactive dashboard
(index.html) approximates with a greedy heuristic. Run this offline to
get provably optimal solutions using the CBC solver (bundled with PuLP)
or commercial solvers like Gurobi/CPLEX.

Usage:
    pip install pulp
    python tesla_supercharger_milp.py

Optional arguments:
    python tesla_supercharger_milp.py --budget 2000 --range 300 --min-stations 15
"""

from pulp import *
from math import radians, sin, cos, sqrt, atan2
import argparse
import json

# ─── City Data (same 35 candidates as the dashboard) ────────────────────────────

CITIES = [
    {"id": 0,  "name": "Delhi",              "lat": 28.61, "lng": 77.21, "state": "Delhi",           "type": "metro",   "cost": 95,  "demand": 480, "grid": 800, "tier": 1},
    {"id": 1,  "name": "Mumbai",             "lat": 19.08, "lng": 72.88, "state": "Maharashtra",     "type": "metro",   "cost": 110, "demand": 520, "grid": 900, "tier": 1},
    {"id": 2,  "name": "Bangalore",          "lat": 12.97, "lng": 77.59, "state": "Karnataka",       "type": "metro",   "cost": 85,  "demand": 450, "grid": 750, "tier": 1},
    {"id": 3,  "name": "Chennai",            "lat": 13.08, "lng": 80.27, "state": "Tamil Nadu",      "type": "metro",   "cost": 80,  "demand": 380, "grid": 700, "tier": 1},
    {"id": 4,  "name": "Hyderabad",          "lat": 17.39, "lng": 78.49, "state": "Telangana",       "type": "metro",   "cost": 78,  "demand": 400, "grid": 650, "tier": 1},
    {"id": 5,  "name": "Kolkata",            "lat": 22.57, "lng": 88.36, "state": "West Bengal",     "type": "metro",   "cost": 72,  "demand": 320, "grid": 600, "tier": 1},
    {"id": 6,  "name": "Pune",               "lat": 18.52, "lng": 73.86, "state": "Maharashtra",     "type": "city",    "cost": 70,  "demand": 350, "grid": 550, "tier": 1},
    {"id": 7,  "name": "Ahmedabad",          "lat": 23.02, "lng": 72.57, "state": "Gujarat",         "type": "city",    "cost": 68,  "demand": 310, "grid": 600, "tier": 1},
    {"id": 8,  "name": "Jaipur",             "lat": 26.91, "lng": 75.79, "state": "Rajasthan",       "type": "city",    "cost": 58,  "demand": 220, "grid": 450, "tier": 2},
    {"id": 9,  "name": "Lucknow",            "lat": 26.85, "lng": 80.95, "state": "Uttar Pradesh",   "type": "city",    "cost": 55,  "demand": 200, "grid": 400, "tier": 2},
    {"id": 10, "name": "Chandigarh",         "lat": 30.73, "lng": 76.78, "state": "Chandigarh",      "type": "city",    "cost": 60,  "demand": 180, "grid": 500, "tier": 2},
    {"id": 11, "name": "Kochi",              "lat": 9.93,  "lng": 76.27, "state": "Kerala",          "type": "city",    "cost": 62,  "demand": 250, "grid": 500, "tier": 2},
    {"id": 12, "name": "Nagpur",             "lat": 21.15, "lng": 79.09, "state": "Maharashtra",     "type": "highway", "cost": 52,  "demand": 170, "grid": 400, "tier": 2},
    {"id": 13, "name": "Indore",             "lat": 22.72, "lng": 75.86, "state": "Madhya Pradesh",  "type": "city",    "cost": 50,  "demand": 160, "grid": 380, "tier": 2},
    {"id": 14, "name": "Surat",              "lat": 21.17, "lng": 72.83, "state": "Gujarat",         "type": "city",    "cost": 65,  "demand": 280, "grid": 550, "tier": 2},
    {"id": 15, "name": "Vadodara",           "lat": 22.31, "lng": 73.19, "state": "Gujarat",         "type": "highway", "cost": 48,  "demand": 150, "grid": 450, "tier": 2},
    {"id": 16, "name": "Coimbatore",         "lat": 11.02, "lng": 76.96, "state": "Tamil Nadu",      "type": "city",    "cost": 52,  "demand": 190, "grid": 420, "tier": 2},
    {"id": 17, "name": "Vizag",              "lat": 17.69, "lng": 83.22, "state": "Andhra Pradesh",  "type": "city",    "cost": 50,  "demand": 150, "grid": 380, "tier": 2},
    {"id": 18, "name": "Goa",                "lat": 15.30, "lng": 74.00, "state": "Goa",             "type": "tourism", "cost": 58,  "demand": 200, "grid": 350, "tier": 2},
    {"id": 19, "name": "Bhopal",             "lat": 23.26, "lng": 77.41, "state": "Madhya Pradesh",  "type": "city",    "cost": 48,  "demand": 140, "grid": 380, "tier": 3},
    {"id": 20, "name": "Udaipur",            "lat": 24.59, "lng": 73.71, "state": "Rajasthan",       "type": "tourism", "cost": 55,  "demand": 130, "grid": 300, "tier": 3},
    {"id": 21, "name": "Mysore",             "lat": 12.30, "lng": 76.66, "state": "Karnataka",       "type": "tourism", "cost": 48,  "demand": 140, "grid": 380, "tier": 3},
    {"id": 22, "name": "Amritsar",           "lat": 31.63, "lng": 74.87, "state": "Punjab",          "type": "tourism", "cost": 52,  "demand": 130, "grid": 400, "tier": 3},
    {"id": 23, "name": "Varanasi",           "lat": 25.32, "lng": 83.01, "state": "Uttar Pradesh",   "type": "tourism", "cost": 48,  "demand": 120, "grid": 350, "tier": 3},
    {"id": 24, "name": "Agra",               "lat": 27.18, "lng": 78.02, "state": "Uttar Pradesh",   "type": "tourism", "cost": 50,  "demand": 160, "grid": 400, "tier": 2},
    {"id": 25, "name": "Dehradun",           "lat": 30.32, "lng": 78.03, "state": "Uttarakhand",     "type": "city",    "cost": 55,  "demand": 110, "grid": 350, "tier": 3},
    {"id": 26, "name": "Patna",              "lat": 25.61, "lng": 85.14, "state": "Bihar",           "type": "city",    "cost": 45,  "demand": 130, "grid": 300, "tier": 3},
    {"id": 27, "name": "Ranchi",             "lat": 23.36, "lng": 85.33, "state": "Jharkhand",       "type": "city",    "cost": 42,  "demand": 90,  "grid": 280, "tier": 3},
    {"id": 28, "name": "Bhubaneswar",        "lat": 20.30, "lng": 85.82, "state": "Odisha",          "type": "city",    "cost": 48,  "demand": 120, "grid": 350, "tier": 3},
    {"id": 29, "name": "Thiruvananthapuram", "lat": 8.52,  "lng": 76.94, "state": "Kerala",          "type": "city",    "cost": 55,  "demand": 160, "grid": 420, "tier": 2},
    {"id": 30, "name": "Guwahati",           "lat": 26.14, "lng": 91.74, "state": "Assam",           "type": "city",    "cost": 50,  "demand": 80,  "grid": 250, "tier": 3},
    {"id": 31, "name": "Raipur",             "lat": 21.25, "lng": 81.63, "state": "Chhattisgarh",    "type": "city",    "cost": 44,  "demand": 100, "grid": 320, "tier": 3},
    {"id": 32, "name": "Mangalore",          "lat": 12.87, "lng": 74.84, "state": "Karnataka",       "type": "city",    "cost": 50,  "demand": 120, "grid": 380, "tier": 3},
    {"id": 33, "name": "Nashik",             "lat": 19.99, "lng": 73.79, "state": "Maharashtra",     "type": "highway", "cost": 48,  "demand": 140, "grid": 400, "tier": 3},
    {"id": 34, "name": "Kanpur",             "lat": 26.45, "lng": 80.35, "state": "Uttar Pradesh",   "type": "city",    "cost": 48,  "demand": 150, "grid": 380, "tier": 3},
]

HIGHWAYS = [
    {"name": "NH-44 (Delhi-Mumbai)",     "cities": [0, 8, 24, 9, 34, 13, 15, 7, 14, 1]},
    {"name": "NH-48 (Delhi-Mumbai)",     "cities": [0, 8, 20, 7, 15, 14, 1]},
    {"name": "NH-44 South (Delhi-Chennai)", "cities": [0, 24, 8, 13, 4, 2, 3]},
    {"name": "NH-16 (Chennai-Kolkata)",  "cities": [3, 17, 28, 5]},
    {"name": "NH-6 (Kolkata-Mumbai)",    "cities": [5, 27, 12, 1]},
    {"name": "NH-44 North (Delhi-Amritsar)", "cities": [0, 10, 22]},
    {"name": "NH-66 (Mumbai-Kochi)",     "cities": [1, 18, 32, 11, 29]},
]


# ─── Haversine Distance ─────────────────────────────────────────────────────────

def haversine(lat1, lon1, lat2, lon2):
    """Great-circle distance in km between two lat/lng points."""
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


# ─── Distance Matrix ────────────────────────────────────────────────────────────

def build_distance_matrix(cities):
    """Pre-compute all pairwise distances between candidate sites."""
    n = len(cities)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = haversine(cities[i]["lat"], cities[i]["lng"],
                          cities[j]["lat"], cities[j]["lng"])
            dist[i][j] = d
            dist[j][i] = d
    return dist


# ─── MILP Solver ─────────────────────────────────────────────────────────────────

def solve_milp(budget=1500, coverage_range=250, min_stations=10, demand_multiplier=1.0):
    """
    Solve the facility location problem as a Mixed-Integer Linear Program.

    Sets:
        I = candidate locations (35 cities)
        J = demand points (same 35 cities — each city is both a candidate and a demand point)

    Decision Variables:
        x[i] ∈ {0, 1}   — whether to build a station at location i
        z[i][j] ∈ {0, 1} — whether station i serves demand point j

    Objective:
        Maximize  Σ_j (demand_j × Σ_i z[i][j])
        (maximize total demand served)

    Subject to:
        Σ_i (cost_i × x[i]) ≤ B                          (budget constraint)
        Σ_i x[i] ≥ M                                      (minimum stations)
        z[i][j] ≤ x[i]               ∀ i, j               (can only assign if built)
        z[i][j] = 0  if dist[i][j] > R   ∀ i, j           (coverage range)
        Σ_i z[i][j] ≤ 1              ∀ j                   (each demand point assigned to at most one station)

    Returns:
        dict with selected stations, total cost, coverage stats, etc.
    """
    n = len(CITIES)
    I = range(n)  # Candidate locations
    J = range(n)  # Demand points

    # Scale demand by multiplier
    demand = [round(CITIES[j]["demand"] * demand_multiplier) for j in J]
    cost = [CITIES[i]["cost"] for i in I]

    # Distance matrix
    dist = build_distance_matrix(CITIES)

    # Eligible assignments (within coverage range)
    eligible = {(i, j) for i in I for j in J if dist[i][j] <= coverage_range}

    # ─── Model ───────────────────────────────────────────────────────────────────
    model = LpProblem("Tesla_Supercharger_India", LpMaximize)

    # Decision variables
    x = LpVariable.dicts("build", I, cat="Binary")
    z = LpVariable.dicts("assign", eligible, cat="Binary")

    # Objective: maximize total demand served
    model += lpSum(demand[j] * z[(i, j)] for (i, j) in eligible), "MaxDemandServed"

    # Budget constraint
    model += lpSum(cost[i] * x[i] for i in I) <= budget, "BudgetCap"

    # Minimum stations constraint
    model += lpSum(x[i] for i in I) >= min_stations, "MinStations"

    # Linking: can only assign to a built station
    for (i, j) in eligible:
        model += z[(i, j)] <= x[i], f"Link_{i}_{j}"

    # Each demand point served by at most one station
    for j in J:
        eligible_for_j = [(i, j) for i in I if (i, j) in eligible]
        if eligible_for_j:
            model += lpSum(z[pair] for pair in eligible_for_j) <= 1, f"SingleAssign_{j}"

    # ─── Solve ───────────────────────────────────────────────────────────────────
    print("=" * 60)
    print("  Tesla Supercharger Network Optimizer — India")
    print("  MILP Facility Location Solver (PuLP + CBC)")
    print("=" * 60)
    print(f"\n  Budget:         ₹{budget} Cr")
    print(f"  Coverage range: {coverage_range} km")
    print(f"  Min stations:   {min_stations}")
    print(f"  Demand mult:    {demand_multiplier}x")
    print(f"  Candidates:     {n} cities")
    print(f"  Variables:      {n} binary (build) + {len(eligible)} binary (assign)")
    print(f"\n  Solving...\n")

    solver = PULP_CBC_CMD(msg=1, timeLimit=60)
    model.solve(solver)

    # ─── Results ─────────────────────────────────────────────────────────────────
    status = LpStatus[model.status]
    print(f"\n{'=' * 60}")
    print(f"  Status: {status}")

    if status != "Optimal":
        print(f"  Solver did not find an optimal solution.")
        print(f"  Try increasing the budget or reducing min_stations.")
        return None

    # Extract selected stations
    selected = [i for i in I if value(x[i]) > 0.5]
    total_cost = sum(cost[i] for i in selected)
    total_demand = sum(demand)

    # Compute demand served
    demand_served = 0
    assignments = {}
    for (i, j) in eligible:
        if value(z[(i, j)]) > 0.5:
            demand_served += demand[j]
            assignments[j] = i

    # Coverage stats
    covered_cities = set(assignments.keys())
    uncovered = [j for j in J if j not in covered_cities]

    # Highway coverage
    highway_results = []
    for hw in HIGHWAYS:
        segments = len(hw["cities"]) - 1
        covered_segs = 0
        for k in range(segments):
            c1, c2 = hw["cities"][k], hw["cities"][k + 1]
            mid_lat = (CITIES[c1]["lat"] + CITIES[c2]["lat"]) / 2
            mid_lng = (CITIES[c1]["lng"] + CITIES[c2]["lng"]) / 2
            if any(haversine(mid_lat, mid_lng, CITIES[s]["lat"], CITIES[s]["lng"]) <= coverage_range for s in selected):
                covered_segs += 1
        hw_pct = round(100 * covered_segs / segments) if segments > 0 else 0
        highway_results.append({"name": hw["name"], "coverage": hw_pct})

    # ─── Print Results ───────────────────────────────────────────────────────────
    print(f"  Objective:      {value(model.objective):,.0f} (demand units served)")
    print(f"{'=' * 60}\n")

    print(f"  SELECTED STATIONS ({len(selected)}):")
    print(f"  {'#':<4} {'City':<22} {'State':<20} {'Type':<10} {'Cost':>6} {'Demand':>7}")
    print(f"  {'-'*4} {'-'*22} {'-'*20} {'-'*10} {'-'*6} {'-'*7}")
    for rank, i in enumerate(selected, 1):
        c = CITIES[i]
        print(f"  {rank:<4} {c['name']:<22} {c['state']:<20} {c['type']:<10} ₹{c['cost']:>4}  {demand[i]:>5}/day")

    print(f"\n  SUMMARY:")
    print(f"  ├── Stations built:    {len(selected)} / {n}")
    print(f"  ├── Total investment:  ₹{total_cost} Cr")
    print(f"  ├── Budget remaining:  ₹{budget - total_cost} Cr")
    print(f"  ├── Cities covered:    {len(covered_cities)} / {n} ({round(100 * len(covered_cities) / n)}%)")
    print(f"  ├── Demand served:     {demand_served:,} / {total_demand:,} ({round(100 * demand_served / total_demand)}%)")
    print(f"  └── Uncovered cities:  {', '.join(CITIES[j]['name'] for j in uncovered) or 'None'}")

    print(f"\n  HIGHWAY CORRIDOR COVERAGE:")
    for hw in highway_results:
        bar = "█" * (hw["coverage"] // 5) + "░" * (20 - hw["coverage"] // 5)
        print(f"  ├── {hw['name']:<35} {bar} {hw['coverage']}%")

    print(f"\n{'=' * 60}")

    # Return structured results
    return {
        "status": status,
        "selected_stations": [CITIES[i]["name"] for i in selected],
        "selected_ids": selected,
        "total_cost": total_cost,
        "budget_remaining": budget - total_cost,
        "cities_covered": len(covered_cities),
        "coverage_pct": round(100 * len(covered_cities) / n),
        "demand_served": demand_served,
        "demand_pct": round(100 * demand_served / total_demand),
        "highway_coverage": highway_results,
    }


# ─── CLI ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tesla Supercharger Network Optimizer — India (MILP Solver)"
    )
    parser.add_argument("--budget", type=int, default=1500,
                        help="Total budget in ₹ Crore (default: 1500)")
    parser.add_argument("--range", type=int, default=250,
                        help="Coverage range in km (default: 250)")
    parser.add_argument("--min-stations", type=int, default=10,
                        help="Minimum number of stations (default: 10)")
    parser.add_argument("--demand-multiplier", type=float, default=1.0,
                        help="Demand growth multiplier (default: 1.0)")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON")

    args = parser.parse_args()

    result = solve_milp(
        budget=args.budget,
        coverage_range=args.range,
        min_stations=args.min_stations,
        demand_multiplier=args.demand_multiplier,
    )

    if args.json and result:
        print("\n" + json.dumps(result, indent=2))
