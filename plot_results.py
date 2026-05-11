

import os, sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time

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

#Problem instances

knapsack = KnapsackProblem(
    weights  = [2, 3, 4, 5, 1, 6, 3, 2],
    values   = [3, 4, 5, 8, 2, 9, 4, 3],
    capacity = 10,
    name     = "8-item knapsack"
)

tsp = TSPProblem.random_instance(n_cities=8, seed=SEED, name="8-city TSP")

# Algorithm labels 

ALGO_LABELS = [
    "Greedy\nDeterministic",
    "Greedy\nNondeterministic",
    "Local Search\nFirst Impr.",
    "Local Search\nBest Impr.",
    "Simulated\nAnnealing",
    "Genetic\nAlgorithm",
]

# Colors: group by algorithm family
COLORS = [
    "#4C9BE8",  
    "#2E6DB4",  
    "#E8834C",  
    "#B45A2E",  
    "#4CBE7A", 
    "#9B59B6",  ]


def run(fn, *args, **kwargs):
    t0     = time.perf_counter()
    result = fn(*args, **kwargs)
    ms     = (time.perf_counter() - t0) * 1000
    return result, ms


#Collect results 

def collect_knapsack():
    fns = [
        (greedy_knapsack_deterministic,    (knapsack,), {}),
        (greedy_knapsack_nondeterministic, (knapsack,), {"alpha": 0.3, "seed": SEED}),
        (local_search_knapsack_first,      (knapsack,), {"seed": SEED}),
        (local_search_knapsack_best,       (knapsack,), {"seed": SEED}),
        (simulated_annealing_knapsack,     (knapsack,), {"seed": SEED}),
        (genetic_algorithm_knapsack,       (knapsack,), {"seed": SEED}),
    ]
    values = []
    times  = []
    for fn, args, kwargs in fns:
        sol, ms = run(fn, *args, **kwargs)
        values.append(knapsack.fitness(sol))
        times.append(ms)
    return values, times


def collect_tsp():
    fns = [
        (greedy_tsp_deterministic,    (tsp,), {}),
        (greedy_tsp_nondeterministic, (tsp,), {"alpha": 0.3, "seed": SEED}),
        (local_search_tsp_first,      (tsp,), {"seed": SEED}),
        (local_search_tsp_best,       (tsp,), {"seed": SEED}),
        (simulated_annealing_tsp,     (tsp,), {"seed": SEED}),
        (genetic_algorithm_tsp,       (tsp,), {"seed": SEED}),
    ]
    distances = []
    times     = []
    for fn, args, kwargs in fns:
        tour, ms = run(fn, *args, **kwargs)
        distances.append(tsp.tour_distance(tour))
        times.append(ms)
    return distances, times


#Plot helpers

def add_value_labels(ax, bars, values, best_val = True):
    """Add value labels on top of each bar, highlight winners in gold."""
    for bar, val in zip(bars, values):
        is_best = (val == best_val)
        color   = "#FFD700" if is_best else "#333333"
        label   = f"{val}\n[BEST]" if is_best else str(val)
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + (max(values) * 0.01),
            label,
            ha="center", va="bottom",
            fontsize=9, fontweight="bold" if is_best else "normal",
            color=color
        )


def style_axis(ax, title, ylabel, xlabel="Algorithm"):
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)


# Plot 1: Knapsack 

def plot_knapsack(values, times, out_dir):
    best_val = max(values)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Knapsack Problem — Algorithm Comparison", fontsize=16, fontweight="bold", y=1.02)

    # Left: value
    bars = ax1.bar(ALGO_LABELS, values, color=COLORS, edgecolor="white", linewidth=1.2, width=0.6)
    add_value_labels(ax1, bars, values, best_val)
    ax1.set_ylim(0, max(values) * 1.2)
    style_axis(ax1, "Total Value (higher is better)", "Value")

    # Right: time
    bars2 = ax2.bar(ALGO_LABELS, times, color=COLORS, edgecolor="white", linewidth=1.2, width=0.6)
    for bar, t in zip(bars2, times):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + max(times) * 0.01,
                 f"{t:.2f}ms", ha="center", va="bottom", fontsize=8, color="#333333")
    ax2.set_ylim(0, max(times) * 1.25)
    style_axis(ax2, "Execution Time (lower is better)", "Time (ms)")

    plt.tight_layout()
    path = os.path.join(out_dir, "plot_knapsack.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f">> Saved: {path}")


# Plot 2: TSP 

def plot_tsp(distances, times, out_dir):
    best_dist = min(distances)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("TSP — Algorithm Comparison", fontsize=16, fontweight="bold", y=1.02)

    # Left: distance
    bars = ax1.bar(ALGO_LABELS, distances, color=COLORS, edgecolor="white", linewidth=1.2, width=0.6)
    for bar, val in zip(bars, distances):
        is_best = (val == best_dist)
        color   = "#FFD700" if is_best else "#333333"
        label   = f"{val}\n[BEST]" if is_best else str(val)
        ax1.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + max(distances) * 0.01,
                 label, ha="center", va="bottom",
                 fontsize=9, fontweight="bold" if is_best else "normal", color=color)
    ax1.set_ylim(0, max(distances) * 1.25)
    style_axis(ax1, "Tour Distance (lower is better)", "Distance")

    # Right: time
    bars2 = ax2.bar(ALGO_LABELS, times, color=COLORS, edgecolor="white", linewidth=1.2, width=0.6)
    for bar, t in zip(bars2, times):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + max(times) * 0.01,
                 f"{t:.2f}ms", ha="center", va="bottom", fontsize=8, color="#333333")
    ax2.set_ylim(0, max(times) * 1.25)
    style_axis(ax2, "Execution Time (lower is better)", "Time (ms)")

    plt.tight_layout()
    path = os.path.join(out_dir, "plot_tsp.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f">> Saved: {path}")





#  Main 

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(out_dir, exist_ok=True)

    print("Running algorithms...")
    k_values,  k_times = collect_knapsack()
    t_dists,   t_times = collect_tsp()

    print("Generating plots...")
    plot_knapsack(k_values, k_times, out_dir)
    plot_tsp(t_dists, t_times, out_dir)

    print("\nAll plots saved to results/")