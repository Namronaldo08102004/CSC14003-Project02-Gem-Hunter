from itertools import combinations  # Create all possible combinations of n elements
from Utils import *

def gen_CNF(board: list[list[str]], assign, unassign):
    clauses = []
    for pos in assign:
        clauses.append([-flatten(pos, len(board[0]))])  # No trap here

    for pos in assign:
        val = int(board[pos[0]][pos[1]])
        neighbors = get_neighbors(pos, unassign)

        if len(neighbors) == 0:
            continue
        elif len(neighbors) == val:
            for neighbor in neighbors:
                clauses.append([flatten(neighbor, len(board[0]))])
        elif len(neighbors) > val:
            # There is a trap around
            clauses.append([flatten(neighbor, len(board[0])) for neighbor in neighbors])

            # Or-ing value + 1 is guaranteed to be true (false or false or false)
            # There is n trap, so there must at least 1 safe cell in every n+1 combinations
            com = combinations(neighbors, val + 1)
            for c in com:
                clauses.append([-flatten(literal, len(board[0])) for literal in c])
            # Or-ing len - value + 1 is guaranteed to be false (true or true or true)
            # There is n trap, so there must be at least 1 trap in every len - n + 1 combinations
            com = combinations(neighbors, len(neighbors) - val + 1)
            for c in com:
                clauses.append([flatten(literal, len(board[0])) for literal in c])
    return clauses