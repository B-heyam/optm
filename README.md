# metaheuristic-optimizer

A Python framework for benchmarking classic optimization algorithms across combinatorial problems. Plug in a problem, run all algorithms, and get a side-by-side comparison of solution quality and runtime.

---

## Algorithms

| Algorithm | Variant |
|---|---|
| Greedy | Deterministic, Nondeterministic (GRASP-style) |
| Local Search | First-Improvement, Best-Improvement |
| Simulated Annealing | — |
| Genetic Algorithm | — |

## Problems

- **0/1 Knapsack** — maximize value without exceeding weight capacity
- **Travelling Salesman (TSP)** — minimize total round-trip distance

---

## Project Structure

```
optm/
├── algorithms/
│   ├── genetic.py
│   ├── greedy.py
│   ├── local_search.py
│   └── simulated_annealing.py
├── problems/
│   ├── knapsack.py
│   └── tsp.py
├── results/
│   └── results.txt
├── compare.py        # run all algorithms and print comparison tables
└── plot_results.py   # visualize results
```

---

## Getting Started

**Requirements:** Python 3.10+, no external dependencies for core algorithms.

```bash
git clone https://github.com/YOUR_USERNAME/metaheuristic-optimizer.git
cd metaheuristic-optimizer
python compare.py
```

---

## Sample Results

Results on the default instances (8-item knapsack, 8-city TSP, seed=42):

```
KNAPSACK
Algorithm                               Value   Weight    Time(ms)
Greedy - Deterministic                     16       10       0.012
Greedy - Nondeterministic                  16       10       0.044
Local Search - First Impr.                 14       10       0.067
Local Search - Best Impr.                  14       10       0.059
Simulated Annealing                        16       10      10.165
Genetic Algorithm                          16       10     102.143

TSP
Algorithm                                Distance    Time(ms)
Greedy - Deterministic                        410       0.022
Greedy - Nondeterministic                     320       0.039
Local Search - First Impr.                    320       0.173
Local Search - Best Impr.                     320       0.290
Simulated Annealing                           320       9.108
Genetic Algorithm                             320     162.582
```

**Overall best:** Greedy (Nondeterministic), Simulated Annealing, and Genetic Algorithm all achieve optimal solutions on both problems. Greedy is fastest; GA is most general.

---

## Using Your Own Problem Instance

**Knapsack:**
```python
from problems.knapsack import KnapsackProblem
from algorithms.genetic import genetic_algorithm_knapsack

problem = KnapsackProblem(
    weights=[2, 3, 4, 5],
    values=[3, 4, 5, 8],
    capacity=8
)
solution = genetic_algorithm_knapsack(problem, seed=42)
print(problem.summary(solution))
```

**TSP (from coordinates):**
```python
from problems.tsp import TSPProblem
from algorithms.simulated_annealing import simulated_annealing_tsp

problem = TSPProblem(coords=[(0,0), (1,5), (4,3), (7,1)], name="my_tsp")
tour = simulated_annealing_tsp(problem, seed=42)
print(problem.summary(tour))
```

---
## License

MIT © BEY Heyam 2026
