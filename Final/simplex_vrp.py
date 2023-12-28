from pulp import *
import numpy as np
import time
import pandas as pd

def fill_results_vrp(dic, nodes, time_taken, min_cost):
    dic["Nodes"].append(nodes)
    dic["Time"].append(time_taken)
    dic["Min_Cost"].append(min_cost)

def solve_vrp(w, k):
    n = len(w)
    prob = LpProblem("Vehicle_Routing_Problem", LpMinimize)

    x = [[LpVariable(f'x_{i}_{j}', 0, 1, LpBinary) for j in range(n)] for i in range(n)]

    prob += lpSum(w[i][j] * x[i][j] for i in range(n) for j in range(n))

    for i in range(1, n):
        prob += lpSum(x[i][j] for j in range(n) if j != i) == 1

    for j in range(1, n):
        prob += lpSum(x[i][j] for i in range(n) if i != j) == 1

    prob += lpSum(x[0][j] for j in range(1, n)) == k
    prob += lpSum(x[j][0] for j in range(1, n)) == k

    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                prob += x[i][j] + x[j][i] <= 1

    start_time = time.time()
    prob.solve()

    print("Status:", LpStatus[prob.status])

    X = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                X[i][j] = x[i][j].varValue

    end_time = time.time()
    elapsed_time = end_time - start_time

    min_cost = np.sum(X * w)

    solution_dict = {
        "Algorithm": ["Simplex-Integer"],
        "Nodes": [n],
        "Time": [elapsed_time],
        "Min_Cost": [min_cost]
    }
    df_results = pd.DataFrame(solution_dict)

    return X, df_results

print("Simplex Integer - Vehicle Routing Problem")
W = np.array([[0, 1, 2, 3, 4],
              [1, 0, 5, 6, 7],
              [2, 5, 0, 8, 9],
              [3, 6, 8, 0, 10],
              [4, 7, 9, 10, 0]])

X, df_results = solve_vrp(W, 2)
print("Solution Matrix:")
print(X)
print("\nResults:")
print(df_results)

