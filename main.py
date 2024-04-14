import os
from time import time_ns

from Src.DPLL import dpll_solver
from Src.GA import GeneticAlgorithm
from Src.A_Star import *
from Src.Resolution import *
from Src.Gen_CNF import gen_CNF
from Src.Maps import Board
from Src.Pysat import pysat_solver


# Find all maps in the chosen folder to choose from
def choose_map(folder: str = "Maps"):
    map_list = os.listdir(folder)
    map_list = [
        x for x in map_list if x.endswith(".txt") and not x.endswith("_solution.txt")
    ]

    print("    Available maps")
    for i, m in enumerate(map_list):
        print(f"{i+1}: {m}")
    print(f"{len(map_list) + 1}: Quit")

    inp = int(input("Choose a map: ")) - 1
    print()
    if inp == len(map_list):
        print("Quitting...")
        exit()
    return map_list[inp], folder


# Choose the algorithm to solve the CNF
def choose_algorithm():
    # algo = ["Pysat", "A*", "Brute Force", "Back-tracking"]
    algo = ["Pysat", "CSP", "DPLL"]
    print("Available algorithms to solve CNF")
    for i, a in enumerate(algo, 1):
        print(f"{i}: {a}")
    inp = int(input("Choose an algorithm: ")) - 1
    print()
    return inp


# Re-branching algorithm
def re_branch(inp: int, clauses: list, board: Board) -> tuple[list[int], int]:
    model = None
    start_time = time_ns()
    match inp:
        case 0:
            model = pysat_solver(clauses)
        case 1:
            model = CSP_Backtracking_Solver(board, clauses)
        case 2:
            model = dpll_solver(clauses)
        case 3:
            pass
        case _:
            pass
    return model, (time_ns() - start_time)


def main():
    board = Board(*choose_map())
    # board = Board("map4.txt", "Maps")
    board.display("Input map")

    clauses = gen_CNF(board)
    model, run_time = re_branch(inp = choose_algorithm(), clauses = clauses, board = board)

    if model is not None:
        board.load_solution(model)
        board.display("Solution")
        board.export_solution()
        print(f"Run time: {run_time:_} nano-seconds\n")
    else:
        print("No solution found\n")


if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"An error occurred: {e}")
