"""
algorithms/greedy.py
─────────────────────
Greedy Algorithm — two versions:
  1. Deterministic
  2. Nondeterministic (GRASP-style)
"""

import random
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from problems.knapsack import KnapsackProblem, DEFAULT as K_DEFAULT
from problems.tsp      import TSPProblem,      DEFAULT as T_DEFAULT


# ── KNAPSACK ──────────────────────────────────────────────────────────────────

def greedy_knapsack_deterministic(problem: KnapsackProblem):
    ratios = sorted(range(problem.n),
                    key=lambda i: problem.values[i] / problem.weights[i],
                    reverse=True)
    solution     = [0] * problem.n
    total_weight = 0
    for i in ratios:
        if total_weight + problem.weights[i] <= problem.capacity:
            solution[i] = 1
            total_weight += problem.weights[i]
    return solution


def greedy_knapsack_nondeterministic(problem: KnapsackProblem, alpha=0.3, seed=None):
    if seed is not None:
        random.seed(seed)
    remaining    = list(range(problem.n))
    solution     = [0] * problem.n
    total_weight = 0

    while remaining:
        feasible = [i for i in remaining
                    if total_weight + problem.weights[i] <= problem.capacity]
        if not feasible:
            break
        ratios    = {i: problem.values[i] / problem.weights[i] for i in feasible}
        max_r     = max(ratios.values())
        min_r     = min(ratios.values())
        threshold = max_r - alpha * (max_r - min_r)
        rcl       = [i for i in feasible if ratios[i] >= threshold]
        chosen    = random.choice(rcl)
        solution[chosen] = 1
        total_weight += problem.weights[chosen]
        remaining.remove(chosen)
    return solution


# ── TSP ───────────────────────────────────────────────────────────────────────

def greedy_tsp_deterministic(problem: TSPProblem):
    visited    = [False] * problem.n
    tour       = [0]
    visited[0] = True
    for _ in range(problem.n - 1):
        current   = tour[-1]
        best_next = min((j for j in range(problem.n) if not visited[j]),
                        key=lambda j: problem.dist_matrix[current][j])
        tour.append(best_next)
        visited[best_next] = True
    return tour


def greedy_tsp_nondeterministic(problem: TSPProblem, alpha=0.3, seed=None):
    if seed is not None:
        random.seed(seed)
    start          = random.randint(0, problem.n - 1)
    visited        = [False] * problem.n
    tour           = [start]
    visited[start] = True
    for _ in range(problem.n - 1):
        current   = tour[-1]
        candidates = sorted(
            [(problem.dist_matrix[current][j], j)
             for j in range(problem.n) if not visited[j]]
        )
        min_d, max_d = candidates[0][0], candidates[-1][0]
        threshold    = min_d + alpha * (max_d - min_d)
        rcl          = [j for d, j in candidates if d <= threshold]
        chosen       = random.choice(rcl)
        tour.append(chosen)
        visited[chosen] = True
    return tour


# ── Quick test ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sol = greedy_knapsack_deterministic(K_DEFAULT)
    print("[Knapsack] Deterministic  :", K_DEFAULT.summary(sol))

    sol = greedy_knapsack_nondeterministic(K_DEFAULT, alpha=0.4, seed=42)
    print("[Knapsack] Nondeterministic:", K_DEFAULT.summary(sol))

    tour = greedy_tsp_deterministic(T_DEFAULT)
    print("\n[TSP] Deterministic  :", T_DEFAULT.summary(tour))

    tour = greedy_tsp_nondeterministic(T_DEFAULT, alpha=0.4, seed=42)
    print("[TSP] Nondeterministic:", T_DEFAULT.summary(tour))
