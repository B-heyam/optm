"""
algorithms/local_search.py
───────────────────────────
Local Search — two versions:
  1. First-Improvement  (accept first better neighbor)
  2. Best-Improvement   (accept best neighbor overall)
"""

import random
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from problems.knapsack import KnapsackProblem, DEFAULT as K_DEFAULT
from problems.tsp      import TSPProblem,      DEFAULT as T_DEFAULT


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _bit_flip_neighbors(solution):
    for i in range(len(solution)):
        neighbor    = solution[:]
        neighbor[i] = 1 - neighbor[i]
        yield neighbor


def _two_opt_swap(tour, i, k):
    return tour[:i] + tour[i:k + 1][::-1] + tour[k + 1:]


# ── KNAPSACK ──────────────────────────────────────────────────────────────────

def local_search_knapsack_first(problem: KnapsackProblem, seed=None):
    if seed is not None:
        random.seed(seed)
    solution = [random.randint(0, 1) for _ in range(problem.n)]
    while not problem.is_feasible(solution):
        solution = [random.randint(0, 1) for _ in range(problem.n)]

    current_val = problem.fitness(solution)
    improved    = True

    while improved:
        improved = False
        for neighbor in _bit_flip_neighbors(solution):
            nval = problem.fitness(neighbor)
            if nval > current_val:
                solution    = neighbor
                current_val = nval
                improved    = True
                break   # ← first improvement: stop immediately
    return solution


def local_search_knapsack_best(problem: KnapsackProblem, seed=None):
    if seed is not None:
        random.seed(seed)
    solution = [random.randint(0, 1) for _ in range(problem.n)]
    while not problem.is_feasible(solution):
        solution = [random.randint(0, 1) for _ in range(problem.n)]

    current_val = problem.fitness(solution)
    improved    = True

    while improved:
        improved      = False
        best_neighbor = None
        best_val      = current_val
        for neighbor in _bit_flip_neighbors(solution):
            nval = problem.fitness(neighbor)
            if nval > best_val:
                best_val      = nval
                best_neighbor = neighbor
        if best_neighbor:
            solution    = best_neighbor
            current_val = best_val
            improved    = True
    return solution


# ── TSP ───────────────────────────────────────────────────────────────────────

def local_search_tsp_first(problem: TSPProblem, seed=None):
    if seed is not None:
        random.seed(seed)
    tour         = list(range(problem.n))
    random.shuffle(tour)
    current_dist = problem.tour_distance(tour)
    improved     = True

    while improved:
        improved = False
        for i in range(1, problem.n - 1):
            for k in range(i + 1, problem.n):
                new_tour = _two_opt_swap(tour, i, k)
                new_dist = problem.tour_distance(new_tour)
                if new_dist < current_dist:
                    tour         = new_tour
                    current_dist = new_dist
                    improved     = True
                    break   # ← first improvement
            if improved:
                break
    return tour


def local_search_tsp_best(problem: TSPProblem, seed=None):
    if seed is not None:
        random.seed(seed)
    tour         = list(range(problem.n))
    random.shuffle(tour)
    current_dist = problem.tour_distance(tour)
    improved     = True

    while improved:
        improved  = False
        best_tour = None
        best_dist = current_dist
        for i in range(1, problem.n - 1):
            for k in range(i + 1, problem.n):
                new_tour = _two_opt_swap(tour, i, k)
                new_dist = problem.tour_distance(new_tour)
                if new_dist < best_dist:
                    best_dist = new_dist
                    best_tour = new_tour
        if best_tour:
            tour         = best_tour
            current_dist = best_dist
            improved     = True
    return tour


# ── Quick test ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sol = local_search_knapsack_first(K_DEFAULT, seed=42)
    print("[Knapsack] First-Improvement:", K_DEFAULT.summary(sol))

    sol = local_search_knapsack_best(K_DEFAULT, seed=42)
    print("[Knapsack] Best-Improvement :", K_DEFAULT.summary(sol))

    tour = local_search_tsp_first(T_DEFAULT, seed=42)
    print("\n[TSP] First-Improvement:", T_DEFAULT.summary(tour))

    tour = local_search_tsp_best(T_DEFAULT, seed=42)
    print("[TSP] Best-Improvement :", T_DEFAULT.summary(tour))
