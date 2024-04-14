from Src.Maps import *
from heapq import heappush, heappop
from itertools import combinations

class Node:
    def __init__ (self, state: list[int], clauses: list[list[int]], board: Board, pathCost: int = 0, successor_level: int = 0):
        """
        The state of each node will be a list of integers where:
            + The positive integer denotes there is a trap at the corresponding position
            + The negative integer denotes there is no trap at the corresponding position
            
        The length of each state is the total number of cells in the board
        """
        self.state = state
        self.clauses = clauses
        self.board = board
        self.listAssignedCells: list[tuple[int, int]] = list(board.assign)
        self.listAssignedCells = sorted(self.listAssignedCells, key = lambda x: (x[0], x[1]))
        print(len(self.listAssignedCells))
        
        self.pathCost = pathCost
        self.heuristic = self.heuristicFunction()
        self.f = self.pathCost + self.heuristic
        
        self.successor_level = successor_level
        
    def __lt__ (self, other) -> bool:
        return self.f < other.f
        
    def heuristicFunction (self) -> int:
        """
        We calculate the heuristic function by counting the number of clauses that conflict with the current state.
        
        We identify "a clause is conflict with the state if and only if every literal in the state is not in the clause"
        Prove: 
            Assume that the state is [A1, A2, ..., An], it means in the new knowledge base will be added n different clauses corresponding 
            n literal(s) A1, A2, ..., An in the state.
            In forward direction, when a conflict occurs, it means there exist a clause [-A_i1, -A_i2, ..., -A_ik] comprising 
            k negated literal(s) in the knowledge base
            (Note: A clause [A,B] in the knowledge base is equivalent to A v B, the operator "-" means negation)
            So, it can be observed that each literal in the state is not in the clause
            
            In backward direction, when every literal in the state is not in the clause:
                Because each literal in each clause of the knowledge base is only one of literals in [A1, A2, ..., An, -A1, -A2, ..., -An]
                So because every literal in the state is not in the clause, it means the clause is [-A_i1, -A_i2, ..., -A_ik] where i1, i2, ..., ik are 
                arbitrary indexes of literals in the state
                
                Because A_i1 AND A_i2 AND ... AND A_ik AND (-A_i1 OR -A_i2 OR ... OR -A_ik) is always false, it means the clause is conflict with the state
            
            Q.E.D
        """
        numConflictClauses: int = 0
        
        for clause in self.clauses:
            conflict: bool = True
            
            for literal in self.state:
                if (literal in clause):
                    conflict = False
                    break
            
            if (conflict):
                numConflictClauses += 1
                
        return numConflictClauses
    
    def checkGoal (self) -> bool:
        """
        The goal state is the state where no clause is conflict with the state
        """
        return self.heuristicFunction() == 0
    
    def expand (self):
        listSuccessors: list[Node] = []
        
        if (self.successor_level == len(self.listAssignedCells)):
            return listSuccessors
        
        assignedCell = self.listAssignedCells[self.successor_level]
        print(assignedCell)
        #? Get the number of mines around the assigned cell
        numMinesAround = int(self.board.board[assignedCell[0]][assignedCell[1]])
        #? Get the neighbors of that assigned cell
        neighbors: list = self.board.get_neighbors(assignedCell)
        neighbors = list(map(lambda x: flatten(x, self.board.cols), neighbors))
        print(neighbors, numMinesAround)
        
        #? Get all sets of numMinesAround elements from the neighbors
        combinationsNeighbors = list(combinations(neighbors, numMinesAround))
        
        for combination in combinationsNeighbors:
            successorState: list[int] = self.state.copy()
            successor: Node = Node(successorState, self.clauses, self.board, self.pathCost, self.successor_level + 1)
            
            #? Update the successor's state
            for i in range (len(self.state)):
                if (-self.state[i] in combination):
                    successor.state[i] = -successor.state[i]
                    
            #? Update the successor's path cost
            successor.pathCost += numMinesAround
            
            print(successor.state, successor.successor_level)
                
            listSuccessors.append(successor)
            
        return listSuccessors
    
def A_Star (board: Board, clauses: list[list[int]]) -> list[int]:
    stateLength = board.rows * board.cols
    
    #? Generate the initial state
    initialState = []
    for i in range (1, stateLength + 1):
        initialState.append(-i)
    
    frontier: list[Node] = []
    reached: dict[tuple[int], Node] = dict()
    heappush(frontier, Node(initialState, clauses, board))
    
    while (frontier):
        node = heappop(frontier)
        reached[tuple(node.state)] = node
        
        if (node.checkGoal()):
            return node.state
        
        listSuccessors: list[Node] = node.expand()
        for successor in listSuccessors:
            curState = tuple(successor.state)
            if (reached.get(curState) is None or (reached.get(curState) is not None and reached[curState].f > successor.f)):
                heappush(frontier, successor)
                reached[curState] = successor
                
    return None