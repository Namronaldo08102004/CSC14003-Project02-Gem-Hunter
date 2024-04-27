from random import choice


# Refs: https://github.com/marcmelis/dpll-sat/blob/master/solvers/original_dpll.py
class DPLL:
    def __init__(self, clauses: list[list[int]]):
        self.cnf = clauses

    def get_model(self):
        """
        Get the model of the CNF formula if it exists and sort it
        """
        solution = self.dpll(self.cnf)
        if solution == 0:
            return None
        return sorted(list(solution), key=abs)

    def get_counter(self, cnf: list[list[int]]):
        """
        Count all of the different literals in the current CNF formula
        """
        counter = set()
        for clause in cnf:
            for literal in clause:
                counter.add(literal)
        return counter

    def constraint_propagation(self, cnf: list[list[int]], unit: int) -> list[list[int]] | int:
        """
        Remove all clauses that contain the unit literal
        Args:
            cnf (list[list[int]]): The current CNF formula
            unit (int): The unit literal to remove from the CNF formula

        Returns:
            list[list[int]] | int: The modified CNF formula or 0 if the formula is unsatisfiable
        """
        modified = []
        for clause in cnf:
            # If the clause is already satisfied, ignore it
            if unit in clause:
                continue
            # If the negation of literal is in the clause, remove it
            if -unit in clause:
                tmp_clause = [x for x in clause if x != -unit]
                # If the clause is empty, it is unsatisfiable - conflict
                if len(tmp_clause) == 0:
                    return 0  # UNSAT
                modified.append(tmp_clause)
            # If the literal is not in the clause, keep it
            else:
                modified.append(clause)

        return modified

    def eliminate_pure_literal(self, cnf: list[list[int]]) -> tuple[list[list[int]] | int, set[int]]:
        """
        Eliminate pure literals from the CNF formula
        Args:
            cnf (list[list[int]]): The current CNF formula

        Returns:
            tuple[list[list[int]] | int, set[int]]: The modified CNF formula and the set of pure literals
        """
        pures = set()
        modified = cnf
        counter = self.get_counter(cnf)

        # Find all pure literals
        for literal in counter:
            if -literal not in counter:
                pures.add(literal)

        # Apply constraint propagation to the CNF formula for each pure literal
        for pure in pures:
            modified = self.constraint_propagation(modified, pure)
            if modified == 0: # UNSAT
                return 0, {0}

        return modified, pures

    def unit_propagation(self, cnf: list[list[int]]) -> tuple[list[list[int]] | int, set[int]]:
        """
        Simplify the CNF formula by propagating unit clauses
        Args:
            cnf (list[list[int]]): The current CNF formula

        Returns:
            tuple[list[list[int]] | int, set[int]]: The modified CNF formula and the set of assigned literals
        """
        modified = cnf
        # Find all unit clauses
        unit_clauses = [clause for clause in cnf if len(clause) == 1]
        assignments = set()

        # Keep simplifying the CNF formula until there are no more unit clauses
        while len(unit_clauses) > 0:
            unit = unit_clauses[0][0]
            # Constrainting down the CNF
            modified = self.constraint_propagation(modified, unit)
            assignments.add(unit)

            if modified == 0: # UNSAT
                return 0, {0}
            # If no clauses left, return the assignments => Solved
            if len(modified) == 0:
                return modified, assignments

            # Recalculate the unit clauses
            unit_clauses = [clause for clause in modified if len(clause) == 1]

        return modified, assignments

    def dpll(self, cnf: list[list[int]], assigned: set = set()) -> set[int] | int:
        """
        Run the DPLL algorithm to solve the CNF formula
        Args:
            cnf (list[list[int]]): The given CNF formula
            assigned (set, optional): The set of assigned literals. Defaults to set().

        Returns:
            set[int] | int: The set of assigned literals or 0 if the formula is unsatisfiable
        """
        modified, pures = self.eliminate_pure_literal(cnf)
        modified, assignments = self.unit_propagation(modified)
        assigned = assigned | pures | assignments

        # UNSAT
        if modified == 0:
            return 0

        if len(modified) == 0:
            return assigned

        # Choose a literal to randomly assign True
        literal = choice(choice(modified))

        # Recursively call DPLL with the chosen literal
        tmp_cnf = self.constraint_propagation(modified, literal)
        solution = self.dpll(tmp_cnf, assigned | {literal})

        # If the chosen literal is False, try again with the negation
        if solution == 0:
            tmp_cnf = self.constraint_propagation(modified, -literal)
            solution = self.dpll(tmp_cnf, assigned | {-literal})

        return solution


def dpll_solver(clauses: list[list[int]], *args, **kwargs) -> list[int] | None:
    """
    Wrapper function for the DPLL algorithm
    """
    dpll = DPLL(clauses)
    return dpll.get_model()
