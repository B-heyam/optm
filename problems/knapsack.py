
class KnapsackProblem:
    """Holds a 0/1 Knapsack instance."""

    def __init__(self, weights, values, capacity, name="knapsack"):
        assert len(weights) == len(values), "weights and values must be same length"
        self.weights  = weights

        self.values   = values
        self.capacity = capacity
        self.n        = len(weights)

        self.name     = name

    # Evaluation 

    def fitness(self, solution):
        """
        solution: list of 0/1 of length n.
        Returns total value if feasible, else 0 (penalty).
        """
        tw = sum(self.weights[i] for i in range(self.n) if solution[i])
        tv = sum(self.values[i]  for i in range(self.n) if solution[i])
        return tv if tw <= self.capacity else 0

    def total_weight(self, solution):
        return sum(self.weights[i] for i in range(self.n) if solution[i])

    def selected_items(self, solution):
        return [i for i in range(self.n) if solution[i]]

    def is_feasible(self, solution):
        return self.total_weight(solution) <= self.capacity

    #  Display 

    def summary(self, solution):
        items = self.selected_items(solution)
        val   = self.fitness(solution)
        wt    = self.total_weight(solution)
        return f"items={items}  value={val}  weight={wt}/{self.capacity}"

    def __repr__(self):
        return (f"KnapsackProblem(n={self.n}, capacity={self.capacity}, "
                f"values={self.values}, weights={self.weights})")


# Default test instance 

DEFAULT = KnapsackProblem(
    weights  = [2, 3, 4, 5, 1, 6, 3, 2],
    values   = [3, 4, 5, 8, 2, 9, 4, 3],
    capacity = 10,
    name     = "default_8items"
)


if __name__ == "__main__":
    p = DEFAULT
    print(p)
    sol = [1, 1, 0, 0, 1, 1, 0, 0]
    print("Solution summary:", p.summary(sol))
    print("Feasible:", p.is_feasible(sol))
