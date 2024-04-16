from Src.Maps import *


def check_model(clauses: list[list[int]], model: list[int]):
    for clause in clauses:
        check = [x in clause for x in model]
        if not any(check):
            return False
    return True


def brute_force(clauses: list[list[int]], board: Board, *args, **kwargs) -> list[int]:
    assigned_flatten_cell = list(
        set([clause[0] for clause in clauses if len(clause) == 1])
    )

    def generate_states(
        listUnassign: list[int],
        nCols: int,
        state: list[int] = [],
        index: int = 0,
    ) -> tuple[bool, list[int]]:
        if index == len(listUnassign):
            model = state.copy()
            model += assigned_flatten_cell
            if check_model(clauses, model):
                return True, model
            return False, None

        literal = listUnassigned[index]
        for option in [-literal, literal]:
            state.append(option)
            check, model = generate_states(listUnassign, nCols, state, index + 1)
            if check:
                return True, model
            state.pop()
        return False, None

    listUnassigned = list(
        set([i for i in range(1, board.rows * board.cols + 1)])
        - set(map(lambda x: abs(x), assigned_flatten_cell))
    )
    check, model = generate_states(listUnassigned, board.cols)
    return model if check else None


def backtracking_solver(clauses: list[list[int]], board: Board):
    assigned_flatten_cell = list(
        set([clause[0] for clause in clauses if len(clause) == 1])
    )
    visited: dict[tuple[int], bool] = dict()

    def backtracking(
        state: list[int],
        clauses: list[list[int]],
    ) -> bool:
        model = state + assigned_flatten_cell
        if check_model(clauses, model):
            return model

        for i in range(len(state)):
            state[i] = -state[i]

            if tuple(state) not in visited:
                visited[tuple(state)] = True
                result = backtracking(state, clauses)
                if result is not None:
                    return result

            state[i] = -state[i]

    initial_state = list(
        set([i for i in range(1, board.rows * board.cols + 1)])
        - set(map(lambda x: abs(x), assigned_flatten_cell))
    )
    return backtracking(initial_state, clauses)
