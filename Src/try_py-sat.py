from pysat.solvers import Solver

from Maps import *
from Gen_CNF import *

if __name__ == "__main__":
    board = LoadMap("ex.txt", "Maps")
    display(board, "Input map")

    assign, unassign = get_assigned_unassigned(board)

    clauses = gen_CNF(board, assign, unassign)

    model = None
    with Solver() as solver:
        solver.append_formula(clauses)
        if solver.solve():
            model = solver.get_model()
        else:
            print("No solution")

    if model is not None:
        for i in model:
            if i > 0:
                x, y = unflatten(i, len(board[0]))
                board[x][y] = "T"
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == "_":
                    board[i][j] = "G"

        display(board, "\nOutput map")
