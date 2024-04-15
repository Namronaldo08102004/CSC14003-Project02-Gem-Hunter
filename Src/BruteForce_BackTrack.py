from Src.Maps import *

def check_state(clauses: list[list[int]], state: list[int]):
    for clause in clauses:
        check = [x in clause for x in state]
        if not any(check):
            return False
    return True

def brute_force(clauses: list[list[int]], board: Board, *args, **kwargs) -> list[int]:
    assigned_flatten_cell = list(set([clause[0] for clause in clauses if len(clause) == 1]))

    def get_all_possible_states(
        listUnassign: list[int],
        nCols: int,
        state: list[int] = [],
        index: int = 0,
    ) -> tuple[bool, list[int]]:
        if index == len(listUnassign):
            model = state.copy()
            model += assigned_flatten_cell
            if check_state(clauses, model):
                return True, model
            return False, None

        literal = listUnassigned[index]
        for option in [-literal, literal]:
            state.append(option)
            check, model = get_all_possible_states(
                listUnassign, nCols, state, index + 1
            )
            if check:
                return True, model
            state.pop()
        return False, None

    listUnassigned = list(set([i for i in range (1, board.rows * board.cols + 1)]) 
                          - set(map(lambda x: abs(x), assigned_flatten_cell)))
    check, model = get_all_possible_states(listUnassigned, board.cols)
    return model if check else None


