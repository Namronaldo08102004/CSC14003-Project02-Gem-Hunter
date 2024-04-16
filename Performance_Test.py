import os
from time import time_ns

from Src.BruteForce_BackTrack import backtracking_solver, brute_force
from Src.DPLL import dpll_solver
from Src.Gen_CNF import gen_CNF
from Src.Maps import Board
from Src.Pysat import pysat_solver
from Src.Redundant_source.CSP_Backtracking import CSP_Backtracking_Solver


def test_performance():
    time_every_case = 5

    measure_dict = {}

    map_list = os.listdir("Maps")
    map_list = [
        x for x in map_list if x.endswith(".txt") and not x.endswith("_solution.txt")
    ]
    algo: dict[str, callable] = {
        "PySAT": pysat_solver,
        "DPLL": dpll_solver,
        "CSP_Backtracking": CSP_Backtracking_Solver,
        "Brute Force": brute_force,
        "Backtracking": backtracking_solver,
    }
    for i in range(len(map_list)):
        board = Board(map_list[i], "Maps")
        clauses = gen_CNF(board)
        print(f"Testing on {map_list[i]}")
        for key, func in algo.items():
            measure_dict[map_list[i]] = {}
            if (map_list[i] == "map10.txt" or map_list[i] == "map15.txt") and (
                key == "Brute Force" or key == "Backtracking"
            ):
                continue

            time_lst = []
            for _ in range(time_every_case):
                start_time = time_ns()
                func(clauses, board)
                time_lst.append(time_ns() - start_time)
            print(f"\tAvg time for {key}: {sum(time_lst) / time_every_case:,} ns")
            measure_dict[map_list[i]][key] = sum(time_lst) / time_every_case

    return measure_dict


if __name__ == "__main__":
    measurement = test_performance()

    with open("Measurement.txt", "w") as f:
        for key, val in measurement.items():
            f.write(f"{key}\n")
            for k, v in val.items():
                f.write(f"\t{k}: {v:,} ns\n")
            f.write("\n")
