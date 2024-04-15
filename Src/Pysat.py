from pysat.solvers import Solver


def pysat_solver(clauses: list[list[int]], *args, **kwargs) -> list[int]:
    """
    Solve the CNF using pysat
    Args:
        clauses (list): CNF clauses

    Returns:
        list[int]: the model
    """
    model = None
    with Solver() as solver:
        solver.append_formula(clauses)
        if solver.solve():
            model = solver.get_model()
    return model
