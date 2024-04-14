from Src.Maps import *

def literal_notLiteral_split (listKnownLiterals: list[int], clauses: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
    """
    The resolution algorithm to solve the SAT problem
    """
    for i in range (len(clauses)):
        clauses[i] = sorted(clauses[i], key = lambda x: abs(x))
    
    temp_clauses = set(map(tuple, clauses))    
    
    old_lenListLiterals = -1
    listLiterals = [clause[0] for clause in temp_clauses if len(clause) == 1]
    
    while (old_lenListLiterals != len(listLiterals)):
        deleted_clauses = set()
        added_clauses = set()
        
        for clause in temp_clauses:
            if (len(clause) == 1):
                continue
            
            deleted_literals = set()
            
            for literal in clause:
                if (-literal in listLiterals):
                    deleted_literals.add(literal)
                    
            if (len(deleted_literals) != 0):
                deleted_clauses.add(clause)
                added_clauses.add(tuple(sorted(list(set(clause) - deleted_literals), key = lambda x: abs(x))))
                
        temp_clauses = temp_clauses.union(added_clauses)
        temp_clauses = temp_clauses - deleted_clauses
            
        old_lenListLiterals = len(listLiterals)
        listLiterals = [clause[0] for clause in temp_clauses if len(clause) == 1]
    
    listLiterals = list(set(listKnownLiterals + listLiterals))
    checkConflict = False
    for i in range (len(listLiterals)):
        for j in range (i + 1, len(listLiterals)):
            if (-listLiterals[i] == listLiterals[j]):
                checkConflict = True
                break
            
        if (checkConflict):
            break
        
    if (checkConflict):
        return None
    
    temp_clauses = temp_clauses - set([clause for clause in temp_clauses if len(clause) == 1])  
    return (listLiterals, list(map(list, temp_clauses)))

def choose_unknown_literal (unknownLiterals: list[int], clauses: list[list[int]]) -> int:
    """
    Choose the unknown literal that has the negation appears the most in binary clauses
    """
    countNegation = dict()
    
    for literal in unknownLiterals:
        countNegation[literal] = 0
        countNegation[-literal] = 0
        
    for clause in clauses:
        if (len(clause) != 2):
            continue
        
        for literal in clause:
            if (-literal in countNegation):
                countNegation[-literal] += 1
                
    maxNegation = -1
    chosenLiteral = None
    
    for literal in unknownLiterals:
        if (countNegation[literal] > maxNegation):
            maxNegation = countNegation[literal]
            chosenLiteral = literal
            
    return chosenLiteral

def check_solution (board: Board):
    """
    Check if the solution is correct
    """
    for i in range (board.rows):
        for j in range (board.cols):
            if (board.board[i][j] == "T" or board.board[i][j] == "G"):
                continue
            
            count = 0
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                if (0 <= i + dx < board.rows and 0 <= j + dy < board.cols and board.board[i + dx][j + dy] == "T"):
                    count += 1
                    
            if (count != int(board.board[i][j])):
                return False
            
    return True

def return_original_board (board: Board):
    """
    Return the original board
    """
    for i in range (board.rows):
        for j in range (board.cols):
            if (board.board[i][j] == "T" or board.board[i][j] == "G"):
                board.board[i][j] = "_"
                
    return board

def CSP_Backtracking (board: Board, model, nonLiterals) -> list[int]:
    if (len(model) == board.rows * board.cols):
        board.load_solution(model)
        if (check_solution(board)):
            return_original_board(board)
            return model
        else:
            return_original_board(board)
            return None
    
    UnknownLiterals = []
    for i in range (1, board.rows * board.cols + 1):
        if (i not in model and -i not in model):
            UnknownLiterals.append(i)
            UnknownLiterals.append(-i)
            
    chosenLiteral = choose_unknown_literal(UnknownLiterals, nonLiterals)
    for option in [chosenLiteral, -chosenLiteral]:
        temp = literal_notLiteral_split(model, nonLiterals + [[option]])
        if (temp is not None):
            temp_literals, temp_nonLiterals = temp
            result = CSP_Backtracking(board, temp_literals, temp_nonLiterals)
            if (result is not None):
                return result

def CSP_Backtracking_Solver (board: Board, clauses: list[list[int]]) -> list[int]:
    model = []
    literals, nonLiterals = literal_notLiteral_split(model, clauses)
    model = literals
    
    return CSP_Backtracking(board, model, nonLiterals)