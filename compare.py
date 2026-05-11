

import time, os, sys
sys.path.insert(0, os.path.dirname(__file__))

from problems.knapsack import KnapsackProblem
from problems.tsp      import TSPProblem

from algorithms.greedy              import (greedy_knapsack_deterministic,
                                            greedy_knapsack_nondeterministic,
                                            greedy_tsp_deterministic,
                                            greedy_tsp_nondeterministic)
from algorithms.local_search        import (local_search_knapsack_first,
                                            local_search_knapsack_best,
                                            local_search_tsp_first,
                                            local_search_tsp_best)
from algorithms.simulated_annealing import (simulated_annealing_knapsack,
                                            simulated_annealing_tsp)
from algorithms.genetic             import (genetic_algorithm_knapsack,
                                            genetic_algorithm_tsp)

SEED = 42

# Problem instances 

knapsack = KnapsackProblem(
    weights  = [2, 3, 4, 5, 1, 6, 3, 2],
    values   = [3, 4, 5, 8, 2, 9, 4, 3],
    capacity = 10,
    name     = "8-item knapsack"
)

tsp = TSPProblem.random_instance(n_cities=8, seed=SEED, name="8-city TSP")


# Runner 

def run(fn, *args, **kwargs):
    t0     = time.perf_counter()
    result = fn(*args, **kwargs)
    ms     = (time.perf_counter() - t0) * 1000
    return result, ms


# Comparison tables 

def compare_knapsack():
    rows    = []
    results = []   # (name, value, time_ms)
    W = 38

    runs = [
        ("Greedy - Deterministic",     greedy_knapsack_deterministic,    (knapsack,), {}),
        ("Greedy - Nondeterministic",  greedy_knapsack_nondeterministic, (knapsack,), {"alpha": 0.3, "seed": SEED}),
        ("Local Search - First Impr.", local_search_knapsack_first,      (knapsack,), {"seed": SEED}),
        ("Local Search - Best Impr.",  local_search_knapsack_best,       (knapsack,), {"seed": SEED}),
        ("Simulated Annealing",        simulated_annealing_knapsack,     (knapsack,), {"seed": SEED}),
        ("Genetic Algorithm",          genetic_algorithm_knapsack,       (knapsack,), {"seed": SEED}),
    ]

    header  = f"\n{'='*(W+30)}\n  KNAPSACK -- {knapsack.name}\n{'='*(W+30)}"
    header += f"\n{'Algorithm':<{W}} {'Value':>6}  {'Weight':>7}  {'Time(ms)':>10}"
    header += f"\n{'-'*(W+30)}"
    print(header)
    rows.append(header)

    for name, fn, args, kwargs in runs:
        sol, ms = run(fn, *args, **kwargs)
        val = knapsack.fitness(sol)
        wt  = knapsack.total_weight(sol)
        results.append((name, val, ms))
        line = f"{name:<{W}} {val:>6}  {wt:>7}  {ms:>10.3f}"
        print(line)
        rows.append(line)

    footer = "=" * (W + 30)
    print(footer)
    rows.append(footer)
    return rows, results


def compare_tsp():
    rows    = []
    results = []   
    W = 38

    runs = [
        ("Greedy - Deterministic",     greedy_tsp_deterministic,    (tsp,), {}),
        ("Greedy - Nondeterministic",  greedy_tsp_nondeterministic, (tsp,), {"alpha": 0.3, "seed": SEED}),
        ("Local Search - First Impr.", local_search_tsp_first,      (tsp,), {"seed": SEED}),
        ("Local Search - Best Impr.",  local_search_tsp_best,       (tsp,), {"seed": SEED}),
        ("Simulated Annealing",        simulated_annealing_tsp,     (tsp,), {"seed": SEED}),
        ("Genetic Algorithm",          genetic_algorithm_tsp,       (tsp,), {"seed": SEED}),
    ]

    header  = f"\n{'='*(W+25)}\n  TSP -- {tsp.name}\n{'='*(W+25)}"
    header += f"\n{'Algorithm':<{W}} {'Distance':>10}  {'Time(ms)':>10}"
    header += f"\n{'-'*(W+25)}"
    print(header)
    rows.append(header)

    for name, fn, args, kwargs in runs:
        tour, ms = run(fn, *args, **kwargs)
        dist = tsp.tour_distance(tour)
        results.append((name, dist, ms))
        line = f"{name:<{W}} {dist:>10}  {ms:>10.3f}"
        print(line)
        rows.append(line)

    footer = "=" * (W + 25)
    print(footer)
    rows.append(footer)
    return rows, results


# Winner summary 

def print_winner_summary(k_results, t_results):
    W   = 38
    sep = "=" * (W + 30)

    # Knapsack: higher value = better
    best_k_val    = max(r[1] for r in k_results)
    best_k        = [r for r in k_results if r[1] == best_k_val]
    fastest_k     = min(best_k, key=lambda r: r[2])
    all_k_winners = [r[0] for r in best_k]

    # TSP: lower distance = better
    best_t_dist   = min(r[1] for r in t_results)
    best_t        = [r for r in t_results if r[1] == best_t_dist]
    fastest_t     = min(best_t, key=lambda r: r[2])
    all_t_winners = [r[0] for r in best_t]

    # Overall: wins on both problems
    overall = set(all_k_winners) & set(all_t_winners)

    lines = []
    lines.append(f"\n{sep}")
    lines.append(f"  WINNER SUMMARY")
    lines.append(sep)

    lines.append(f"\n  [KNAPSACK]  Best value = {best_k_val}")
    if len(all_k_winners) == 1:
        lines.append(f"    Winner         : {all_k_winners[0]}")
    else:
        lines.append(f"    Tied for best  : {', '.join(all_k_winners)}")
        lines.append(f"    Fastest winner : {fastest_k[0]}  ({fastest_k[2]:.3f} ms)")

    lines.append(f"\n  [TSP]  Best distance = {best_t_dist}")
    if len(all_t_winners) == 1:
        lines.append(f"    Winner         : {all_t_winners[0]}")
    else:
        lines.append(f"    Tied for best  : {', '.join(all_t_winners)}")
        lines.append(f"    Fastest winner : {fastest_t[0]}  ({fastest_t[2]:.3f} ms)")

    lines.append(f"\n  [OVERALL BEST ALGORITHM]")
    if overall:
        lines.append(f"    {', '.join(sorted(overall))}")
        lines.append(f"    --> Wins on BOTH Knapsack and TSP")
    else:
        lines.append(f"    No single algorithm wins both problems.")
        lines.append(f"    Best for Knapsack : {fastest_k[0]}")
        lines.append(f"    Best for TSP      : {fastest_t[0]}")

    lines.append(f"\n{sep}\n")

    for line in lines:
        print(line)
    return lines


# Save results

def save_results(lines):
    os.makedirs("results", exist_ok=True)
    path = os.path.join("results", "results.txt")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"\n>> Results saved to {path}")


# Main 

if __name__ == "__main__":
    all_lines = []

    k_rows, k_results = compare_knapsack()
    t_rows, t_results = compare_tsp()
    winner_lines      = print_winner_summary(k_results, t_results)

    all_lines += k_rows + t_rows + winner_lines
    save_results(all_lines)