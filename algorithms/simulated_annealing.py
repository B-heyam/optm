"""
algorithms/simulated_annealing.py
───────────────────────────────────
Simulated Annealing (SA)
"""

import random, math
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from problems.knapsack import KnapsackProblem, DEFAULT as K_DEFAULT
from problems.tsp      import TSPProblem,      DEFAULT as T_DEFAULT


def _two_opt_swap(tour, i, k):
    return tour[:i] + tour[i:k + 1][::-1] + tour[k + 1:]


# ── KNAPSACK ──────────────────────────────────────────────────────────────────

def simulated_annealing_knapsack(
    problem: KnapsackProblem,
    T_init=1000.0, T_min=1e-3, cooling=0.995,
    seed=None
):
    if seed is not None:
        random.seed(seed)

    solution = [random.randint(0, 1) for _ in range(problem.n)]
    while not problem.is_feasible(solution):
        solution = [random.randint(0, 1) for _ in range(problem.n)]

    current_val   = problem.fitness(solution)
    best_solution = solution[:]
    best_val      = current_val
    T             = T_init

    while T > T_min:
        i        = random.randint(0, problem.n - 1)
        neighbor = solution[:]
        neighbor[i] = 1 - neighbor[i]

        if not problem.is_feasible(neighbor):
            T *= cooling
            continue

        nval  = problem.fitness(neighbor)
        delta = nval - current_val

        if delta > 0 or random.random() < math.exp(delta / T):
            solution    = neighbor
            current_val = nval
            if current_val > best_val:
                best_val      = current_val
                best_solution = solution[:]
        T *= cooling

    return best_solution


# ── TSP ───────────────────────────────────────────────────────────────────────

def simulated_annealing_tsp(
    problem: TSPProblem,
    T_init=1000.0, T_min=1e-3, cooling=0.995,
    seed=None
):
    if seed is not None:
        random.seed(seed)

    tour         = list(range(problem.n))
    random.shuffle(tour)
    current_dist = problem.tour_distance(tour)
    best_tour    = tour[:]
    best_dist    = current_dist
    T            = T_init

    while T > T_min:
        i        = random.randint(1, problem.n - 2)
        k        = random.randint(i + 1, problem.n - 1)
        neighbor = _two_opt_swap(tour, i, k)
        new_dist = problem.tour_distance(neighbor)
        delta    = new_dist - current_dist

        if delta < 0 or random.random() < math.exp(-delta / T):
            tour         = neighbor
            current_dist = new_dist
            if current_dist < best_dist:
                best_dist = current_dist
                best_tour = tour[:]
        T *= cooling

    return best_tour


# ── Quick test ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sol = simulated_annealing_knapsack(K_DEFAULT, seed=42)
    print("[Knapsack] SA:", K_DEFAULT.summary(sol))

    tour = simulated_annealing_tsp(T_DEFAULT, seed=42)
    print("[TSP]      SA:", T_DEFAULT.summary(tour))
