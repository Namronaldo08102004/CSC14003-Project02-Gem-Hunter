from Src.Maps import *


def literal_notLiteral_split(
    listKnownLiterals: list[int], clauses: list[list[int]]
) -> tuple[list[list[int]], list[list[int]]]:
    """
    This function is used to split the clauses into two sets: one contains all the literals that are known to be true
    and the other contains the rest of the clauses. The function also checks for conflicts in the clauses.
    """
    # ? Convert the clauses to a set of tuples to remove duplicates
    temp_clauses = set(map(tuple, clauses))

    # ? Loop many times, until there is no more literals can be inferred
    old_lenListLiterals = -1
    listLiterals = [clause[0] for clause in temp_clauses if len(clause) == 1]

    while old_lenListLiterals != len(listLiterals):
        deleted_clauses = set()
        added_clauses = set()

        for clause in temp_clauses:
            if len(clause) == 1:
                continue

            deleted_literals = set()
            beDeletedClause = False

            for literal in clause:
                if -literal in listLiterals:
                    # ? A AND (-A OR B) -> B
                    deleted_literals.add(literal)
                elif literal in listLiterals:
                    # ? A AND (A OR B) -> A
                    beDeletedClause = True
                    deleted_clauses.add(clause)
                    break

            if beDeletedClause:
                continue

            if len(deleted_literals) != 0:
                deleted_clauses.add(clause)
                if len(clause) == len(deleted_literals):
                    return None
                added_clauses.add(
                    tuple(
                        sorted(
                            list(set(clause) - deleted_literals), key=lambda x: abs(x)
                        )
                    )
                )

        temp_clauses = temp_clauses.union(added_clauses)
        temp_clauses = temp_clauses - deleted_clauses

        old_lenListLiterals = len(listLiterals)
        listLiterals = [clause[0] for clause in temp_clauses if len(clause) == 1]

    # ? Add the known literals to the list of literals and remove duplicates, then check for conflicts
    listLiterals = list(set(listKnownLiterals + listLiterals))
    checkConflict = False
    for i in range(len(listLiterals)):
        for j in range(i + 1, len(listLiterals)):
            if -listLiterals[i] == listLiterals[j]:
                checkConflict = True
                break

        if checkConflict:
            break

    # ? If there is a conflict, return None
    if checkConflict:
        return None

    # ? Remove the known literals from the clauses and return the result
    temp_clauses = temp_clauses - set(
        [clause for clause in temp_clauses if len(clause) == 1]
    )
    return (listLiterals, list(map(list, temp_clauses)))


def choose_unknown_literal(unknownLiterals: list[int], clauses: list[list[int]]) -> int:
    """
    Choose the unknown literal that has the negation appears the most in binary clauses
    """
    # ? Count the number of negation of each literal in the binary clauses
    countNegation = dict()

    for literal in unknownLiterals:
        countNegation[literal] = 0
        countNegation[-literal] = 0

    for clause in clauses:
        if len(clause) != 2:
            continue

        for literal in clause:
            if -literal in countNegation:
                countNegation[-literal] += 1

    # ? Choose the unknown literal that has the negation appears the most
    maxNegation = 0
    chosenLiteral = None

    for literal in unknownLiterals:
        if countNegation[literal] > maxNegation:
            maxNegation = countNegation[literal]
            chosenLiteral = literal

    return chosenLiteral


def CSP_Backtracking(board: Board, model, nonLiterals) -> list[int]:
    """
    This function is used to solve the problem using the Backtracking algorithm from CSP
    """
    # ? If the model is consistent, return the model
    if len(model) == board.rows * board.cols:
        return model

    # ? Get the list of unknown literals
    UnknownLiterals = []
    for i in range(1, board.rows * board.cols + 1):
        if i not in model and -i not in model:
            UnknownLiterals.append(i)
            UnknownLiterals.append(-i)

    # ? Choose the unknown literal that has the negation appears the most in binary clauses
    chosenLiteral = choose_unknown_literal(UnknownLiterals, nonLiterals)

    # ? If the chosen literal does not appear in any binary clauses, it means there is no more inference can be made, so return the model after adding the negation of the unknown literals
    if chosenLiteral is None:
        model = model + [literal for literal in UnknownLiterals if literal < 0]
        return model
    # ? Otherwise, solve the problem recursively with each literal having two options
    else:
        for option in [chosenLiteral, -chosenLiteral]:
            temp = literal_notLiteral_split(model, nonLiterals + [[option]])
            if temp is not None:
                temp_literals, temp_nonLiterals = temp
                result = CSP_Backtracking(board, temp_literals, temp_nonLiterals)
                if result is not None:
                    return result


def CSP_Backtracking_Solver(
    clauses: list[list[int]], board: Board, *args, **kwargs
) -> list[int]:
    # ? Sort each clause by the absolute value of the literals
    for i in range(len(clauses)):
        clauses[i] = sorted(clauses[i], key=lambda x: abs(x))

    """
    Split the clauses into two sets: one contains all the literals that are known to be true
    and the other contains the rest of the clauses
    """
    model = []
    literals, nonLiterals = literal_notLiteral_split(model, clauses)
    model = literals

    # ? Solve the problem using the Backtracking algorithm from CSP and return the result
    return CSP_Backtracking(board, model, nonLiterals)
