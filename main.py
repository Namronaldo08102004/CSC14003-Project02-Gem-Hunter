import os

from Src.Algorithm import *
from Src.Gen_CNF import gen_CNF
from Src.Maps import Board

# Find all maps in the chosen folder to choose from
def choose_map(folder: str = "Maps"):
    map_list = os.listdir(folder)
    map_list = [x for x in map_list if x.endswith(".txt")]

    print("Available maps")
    for i, m in enumerate(map_list):
        print(f"{i+1}: {m}")
    inp = int(input("Choose a map: ")) - 1
    print()
    return map_list[inp], folder

# Choose the algorithm to solve the CNF
def choose_algorithm():
    # algo = ["Pysat", "A*", "Brute Force", "Back-tracking"]
    algo = ["Pysat"]
    print("Available algorithms to solve CNF")
    for i, a in enumerate(algo, 1):
        print(f"{i}: {a}")
    inp = int(input("Choose an algorithm: ")) - 1
    print()
    return inp

# Re-branching algorithm
def re_branch(inp: int, clauses: list) -> list[int]:
    model = None
    match inp:
        case 0:
            model = pysat_solver(clauses)
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case _:
            pass
    return model


if __name__ == "__main__":
    board = Board(*choose_map())
    board.display("Input map")

    clauses = gen_CNF(board)
    model = re_branch(inp=choose_algorithm(), clauses=clauses)

    if model is not None:
        board.load_solution(model)
        board.display("Solution")
        board.export_solution()
    else:
        print("No solution found")
