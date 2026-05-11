"""
algorithms/genetic.py
──────────────────────
Genetic Algorithm (GA)
"""

import random
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from problems.knapsack import KnapsackProblem, DEFAULT as K_DEFAULT
from problems.tsp      import TSPProblem,      DEFAULT as T_DEFAULT


# ── SHARED SELECTION 

def _tournament(population, fitnesses, k=3):
    competitors = random.sample(range(len(population)), k)
    winner      = max(competitors, key=lambda idx: fitnesses[idx])
    return population[winner][:]


# ── KNAPSACK GA ──────

def genetic_algorithm_knapsack(
    problem: KnapsackProblem,
    pop_size=50, generations=200,
    crossover_rate=0.8, mutation_rate=0.05,
    seed=None
):
    if seed is not None:
        random.seed(seed)

    population = [[random.randint(0, 1) for _ in range(problem.n)]
                  for _ in range(pop_size)]
    best_chr = None
    best_val = -1

    for _ in range(generations):
        fitnesses = [problem.fitness(ind) for ind in population]
        best_idx  = max(range(pop_size), key=lambda i: fitnesses[i])
        if fitnesses[best_idx] > best_val:
            best_val = fitnesses[best_idx]
            best_chr = population[best_idx][:]

        new_pop = [best_chr[:]]   # elitism
        while len(new_pop) < pop_size:
            p1, p2 = _tournament(population, fitnesses), _tournament(population, fitnesses)
            if random.random() < crossover_rate:
                pt = random.randint(1, problem.n - 1)
                c1, c2 = p1[:pt] + p2[pt:], p2[:pt] + p1[pt:]
            else:
                c1, c2 = p1[:], p2[:]
            for c in (c1, c2):
                mutated = [1 - g if random.random() < mutation_rate else g for g in c]
                new_pop.append(mutated)
                if len(new_pop) >= pop_size:
                    break
        population = new_pop

    return best_chr


# ── TSP GA ───────────

def _order_crossover(p1, p2):
    n           = len(p1)
    start, end  = sorted(random.sample(range(n), 2))
    child       = [None] * n
    child[start:end + 1] = p1[start:end + 1]
    segment     = set(p1[start:end + 1])
    fill        = [g for g in p2 if g not in segment]
    idx = 0
    for i in range(n):
        if child[i] is None:
            child[i] = fill[idx]
            idx += 1
    return child


def genetic_algorithm_tsp(
    problem: TSPProblem,
    pop_size=50, generations=300,
    crossover_rate=0.8, mutation_rate=0.1,
    seed=None
):
    if seed is not None:
        random.seed(seed)

    population = [random.sample(range(problem.n), problem.n)
                  for _ in range(pop_size)]
    best_tour = None
    best_dist = float('inf')

    for _ in range(generations):
        distances = [problem.tour_distance(t) for t in population]
        fitnesses = [1.0 / d for d in distances]
        best_idx  = min(range(pop_size), key=lambda i: distances[i])
        if distances[best_idx] < best_dist:
            best_dist = distances[best_idx]
            best_tour = population[best_idx][:]

        new_pop = [best_tour[:]]   # elitism
        while len(new_pop) < pop_size:
            p1  = _tournament(population, fitnesses)
            p2  = _tournament(population, fitnesses)
            c   = _order_crossover(p1, p2) if random.random() < crossover_rate else p1[:]
            if random.random() < mutation_rate:
                i, j   = random.sample(range(problem.n), 2)
                c[i], c[j] = c[j], c[i]
            new_pop.append(c)
        population = new_pop

    return best_tour


# ── Quick test ───────

if __name__ == "__main__":
    sol = genetic_algorithm_knapsack(K_DEFAULT, seed=42)
    print("[Knapsack] GA:", K_DEFAULT.summary(sol))

    tour = genetic_algorithm_tsp(T_DEFAULT, seed=42)
    print("[TSP]      GA:", T_DEFAULT.summary(tour))
