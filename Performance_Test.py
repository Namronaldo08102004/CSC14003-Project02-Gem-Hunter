import os
from time import time_ns

from Src.BruteForce_BackTrack import backtracking_solver, brute_force
from Src.DPLL import dpll_solver
from Src.GA import GeneticAlgorithm
from Src.Gen_CNF import gen_CNF
from Src.Maps import Board
from Src.Pysat import pysat_solver
from Src.CSP_Backtracking import CSP_Backtracking_Solver


def test_performance():
    time_every_case = 1

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
        "GA": GeneticAlgorithm,
    }
    for i in range(len(map_list)):
        board = Board(map_list[i], "Maps")
        clauses = gen_CNF(board)
        print(f"Testing on {map_list[i]}")

        measure_dict = {}

        for key, func in algo.items():
            try:
                if (map_list[i] == "map10.txt" or map_list[i] == "map15.txt") and (
                    key == "Brute Force" or key == "GA" or key == "Backtracking"
                ):
                    continue

                time_lst = []
                for _ in range(time_every_case):
                    start_time = time_ns()
                    func(clauses, board)
                    time_lst.append(time_ns() - start_time)
                print(
                    f"\tAvg time for {key}: {int(sum(time_lst) / time_every_case):,} ns"
                )
                measure_dict[key] = int(sum(time_lst) / time_every_case)
            except Exception as e:
                print(f"\t{key} failed: {e}")

        with open("Measurement.txt", "a") as f:
            f.write(f"{map_list[i]}\n")
            for key, val in measure_dict.items():
                f.write(f"\t{key}: {val:,} ns\n")
            f.write("\n")

    return measure_dict


if __name__ == "__main__":
    test_performance()
