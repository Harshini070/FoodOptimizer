# optimizer/solver.py

def solve_transportation(supply, demand, cost_matrix):
    import numpy as np

    supply = supply[:]
    demand = demand[:]

    n_rows = len(supply)
    n_cols = len(demand)

    result = [[0] * n_cols for _ in range(n_rows)]
    total_cost = 0

    # Copy of cost matrix for manipulation
    cost = [row[:] for row in cost_matrix]

    while True:
        min_cost = float('inf')
        min_cell = (-1, -1)

        # Find the minimum cost cell
        for i in range(n_rows):
            for j in range(n_cols):
                if supply[i] > 0 and demand[j] > 0 and cost[i][j] < min_cost:
                    min_cost = cost[i][j]
                    min_cell = (i, j)

        if min_cell == (-1, -1):  # No more valid cell
            break

        i, j = min_cell
        quantity = min(supply[i], demand[j])
        result[i][j] = quantity
        total_cost += quantity * cost[i][j]

        supply[i] -= quantity
        demand[j] -= quantity

    return result, total_cost
