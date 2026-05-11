

import math
import random


class TSPProblem:

    def __init__(self, dist_matrix=None, coords=None, name="tsp"):
       
        if dist_matrix is not None:
            self.dist_matrix = dist_matrix
            self.n = len(dist_matrix)
            self.coords = coords  # optional, for display
        elif coords is not None:
            self.coords = coords
            self.n = len(coords)
            self.dist_matrix = self._build_dist_matrix(coords)
        else:
            raise ValueError("Provide either dist_matrix or coords")
        self.name = name

    # Build 

    @staticmethod
    def _build_dist_matrix(coords):
        n = len(coords)
        return [
            [int(math.hypot(coords[i][0] - coords[j][0],
                            coords[i][1] - coords[j][1]))
             for j in range(n)]
            for i in range(n)
        ]

    @classmethod
    def random_instance(cls, n_cities, seed=None, name="random_tsp"):
        """Generate a random TSP instance from n cities on a 100×100 grid."""
        if seed is not None:
            random.seed(seed)
        coords = [(random.randint(0, 100), random.randint(0, 100))
                  for _ in range(n_cities)]
        return cls(coords=coords, name=name)

    # ── Evaluation 

    def tour_distance(self, tour):
        """Total round-trip distance of a tour (list of city indices)."""
        n = len(tour)
        return sum(self.dist_matrix[tour[i]][tour[(i + 1) % n]]
                   for i in range(n))

    def is_valid_tour(self, tour):
        return sorted(tour) == list(range(self.n))

    #  Display 

    def summary(self, tour):
        return f"tour={tour}  distance={self.tour_distance(tour)}"

    def __repr__(self):
        return f"TSPProblem(n={self.n}, name='{self.name}')"


#  Default test instance 

DEFAULT = TSPProblem(
    dist_matrix=[
        [0, 10, 15, 20],
        [10,  0, 35, 25],
        [15, 35,  0, 30],
        [20, 25, 30,  0],
    ],
    name="default_4cities"
)


if __name__ == "__main__":
    p = DEFAULT
    print(p)
    tour = [0, 1, 3, 2]
    print("Tour summary:", p.summary(tour))
    print("Valid:", p.is_valid_tour(tour))

    # Random instance example
    rp = TSPProblem.random_instance(n_cities=6, seed=42)
    print("\nRandom instance:", rp)
