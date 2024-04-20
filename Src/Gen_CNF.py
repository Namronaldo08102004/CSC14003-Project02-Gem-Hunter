from itertools import combinations  # Create all possible combinations of n elements

from Src.Maps import Board, flatten


def gen_CNF(board: Board):
    clauses = []
    # No trap in the assigned cells
    for pos in board.assign:
        clauses.append([-flatten(pos, board.cols)])

    # For each assigned cell, check if there is a trap around
    for pos in board.assign:
        val = int(board.board[pos[0]][pos[1]])
        neighbors = board.get_neighbors(pos) # Get all the unassigned neighbors of the cell

        # No trap around
        if val == 0:
            for neighbor in neighbors:
                clauses.append([-flatten(neighbor, board.cols)])
        # No neighbors
        elif len(neighbors) == 0: 
            continue
        # All neighbors are traps
        elif len(neighbors) == val:
            for neighbor in neighbors:
                clauses.append([flatten(neighbor, board.cols)])
        # Some neighbors are traps
        elif len(neighbors) > val:
            # There is a trap around
            clauses.append([flatten(neighbor, board.cols) for neighbor in neighbors])

            # Or-ing value + 1 is guaranteed to be true (false or false or false)
            # There is n trap, so there must at least 1 safe cell in every n+1 combinations
            com = combinations(neighbors, val + 1)
            for c in com:
                clauses.append([-flatten(literal, board.cols) for literal in c])
            # Or-ing len - value + 1 is guaranteed to be false (true or true or true)
            # There is n trap, so there must be at least 1 trap in every len - n + 1 combinations
            com = combinations(neighbors, len(neighbors) - val + 1)
            for c in com:
                clauses.append([flatten(literal, board.cols) for literal in c])

    # Removing duplicates clauses
    clauses = {frozenset(clause) for clause in clauses}
    clauses = [list(clause) for clause in clauses]
    return clauses
