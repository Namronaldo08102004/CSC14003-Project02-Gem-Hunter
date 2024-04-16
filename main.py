import os
from time import time_ns

from Src.BruteForce_BackTrack import brute_force, backtracking_solver
from Src.DPLL import dpll_solver
from Src.Gen_CNF import gen_CNF
from Src.Maps import Board
from Src.Pysat import pysat_solver
from Src.Redundant_source.CSP_Backtracking import CSP_Backtracking_Solver
from Src.Redundant_source.GA import GeneticAlgorithm

def gather_input(src: list[str], msg: str):
    print(msg)
    for i, s in enumerate(src, 1):
        print(f"{i}: {s}")
    inp = int(input("Choose an option: ")) - 1
    print()
    return inp


# Find all maps in the chosen folder to choose from
def choose_map(folder: str = "Maps"):
    map_list = os.listdir(folder)
    map_list = [
        x for x in map_list if x.endswith(".txt") and not x.endswith("_solution.txt")
    ]

    inp = gather_input(map_list + ["Quit"], "Choose a map: ")
    if inp == len(map_list):
        print("Quitting...")
        exit()
    return map_list[inp], folder


def re_branch(clauses: list[list[int]], board: Board) -> tuple[list[int], int]:
    algo: dict[str, callable] = {
        "PySAT": pysat_solver,
        "DPLL": dpll_solver,
        "CSP_Backtracking": CSP_Backtracking_Solver,
        "Brute Force": brute_force,
        "Backtracking": backtracking_solver,
        "Genetic Algorithm": GeneticAlgorithm
    }
    inp = gather_input(key := list(algo.keys()), "Choose an algorithm: ")
    model = None
    start_time = time_ns()

    model = algo[key[inp]](clauses, board)
    return model, (time_ns() - start_time)


def main():
    board = Board(*choose_map())
    # board = Board("map4.txt", "Maps")
    board.display("Input map")

    clauses = gen_CNF(board)
    model, run_time = re_branch(clauses=clauses, board=board)

    if model is not None:
        board.load_solution(model)
        board.display("Solution")
        board.export_solution()
        print(f"Run time: {run_time:,} nano-seconds\n")
    else:
        print("No solution found\n")


if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user, quitting...")
    except Exception as e:
        print(f"An error occurred: {e}")
