from itertools import combinations  # Create all possible combinations of n elements

from Src.Maps import Board, flatten


def gen_CNF(board: Board):
    clauses = []
    for pos in board.assign:
        clauses.append([-flatten(pos, board.cols)])  # No trap here

    for pos in board.assign:
        val = int(board.board[pos[0]][pos[1]])
        neighbors = board.get_neighbors(pos)

        if val == 0:
            # No trap around
            for neighbor in neighbors:
                clauses.append([-flatten(neighbor, board.cols)])
        elif len(neighbors) == 0:
            continue
        elif len(neighbors) == val:
            for neighbor in neighbors:
                clauses.append([flatten(neighbor, board.cols)])
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
    return clauses
