from random import choice


# Refs: https://github.com/marcmelis/dpll-sat/blob/master/solvers/original_dpll.py
class DPLL:
    def __init__(self, clauses: list[list[int]]):
        self.cnf = clauses

    def get_model(self):
        solution = self.dpll(self.cnf)
        if solution == 0:
            return None
        return sorted(list(solution), key=abs)

    def get_counter(self, cnf: list[list[int]]):
        counter = set()
        for clause in cnf:
            for literal in clause:
                counter.add(literal)
        return counter

    def constraint_propagation(self, cnf: list[list[int]], unit: int):
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

    def eliminate_pure_literal(self, cnf: list[list[int]]):
        pures = set()
        modified = cnf
        counter = self.get_counter(cnf)

        for literal in counter:
            if -literal not in counter:
                pures.add(literal)

        for pure in pures:
            modified = self.constraint_propagation(modified, pure)
            if modified == 0:
                return 0, {0}

        return modified, pures

    def unit_propagation(self, cnf: list[list[int]]):
        modified = cnf
        unit_clauses = [clause for clause in cnf if len(clause) == 1]
        assignments = set()

        while len(unit_clauses) > 0:
            unit = unit_clauses[0][0]
            # Constrainting down the CNF
            modified = self.constraint_propagation(modified, unit)
            assignments.add(unit)

            if modified == 0:
                return 0, {0}
            # If no clauses left, return the assignments => Solved
            if len(modified) == 0:
                return modified, assignments

            # Recalculate the unit clauses
            unit_clauses = [clause for clause in modified if len(clause) == 1]

        return modified, assignments

    def dpll(self, cnf: list[list[int]], assigned: set = set()):
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


def dpll_solver(clauses: list[list[int]], *args, **kwargs):
    dpll = DPLL(clauses)
    return dpll.get_model()
