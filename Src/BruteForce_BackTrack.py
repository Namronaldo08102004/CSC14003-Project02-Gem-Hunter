from Src.Maps import *


def check_state(clauses: list[list[int]], state: list[int]):
    for clause in clauses:
        check = [x in clause for x in state]
        if not any(check):
            return False
    return True


def brute_force(clauses: list[list[int]], board: Board, *args, **kwargs) -> list[int]:
    assigned_cell = [-flatten(x, board.cols) for x in board.assign]

    def get_all_possible_states(
        listUnassign: list[tuple[int, int]],
        nCols: int,
        state: list[int] = [],
        index: int = 0,
    ) -> tuple[bool, list[int]]:
        if index == len(listUnassign):
            model = state.copy()
            model += assigned_cell
            if check_state(clauses, model):
                return True, model
            return False, []

        literal = flatten(listUnassign[index], nCols)
        for option in [-literal, literal]:
            state.append(option)
            check, model = get_all_possible_states(
                listUnassign, nCols, state, index + 1
            )
            if check:
                return True, model
            state.pop()
        return False, []

    check, model = get_all_possible_states(list(board.unassign), board.cols)
    return model if check else None
