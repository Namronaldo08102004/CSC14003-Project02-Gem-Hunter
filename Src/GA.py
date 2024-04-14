from random import choices, randint, random

class Node:
    def __init__ (self, state: list[int], clauses: list[list[int]]):
        """
        The state of each node will be a list of integers where:
            + The positive integer denotes there is a trap at the corresponding position
            + The negative integer denotes there is no trap at the corresponding position
            
        The length of each state is the total number of cells in the board
        """
        self.state = state
        self.clauses = clauses
        
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

"""
Genetic algorithm references:
+ https://www.youtube.com/watch?v=uQj5UNhCPuo
+ https://www.youtube.com/watch?v=nhT56blfRpE
"""
def GeneticAlgorithm (stateLength: int, clauses: list[list[int]]) -> list[int]:
    """
    The length of each state will be board.rows * board.cols
    """
    def generatePopulation (state_length: int, population_size: int) -> list[Node]:
        def generateRandomState (state_length: int) ->list[int]:
            newState: list[int] = []
            
            for i in range (1, state_length + 1):
                option = [-i, i]
                newState.append(choices(option)[0])
                
            return newState
        
        newPopulation: list[Node] = [Node(generateRandomState(state_length), clauses) for _ in range (0, population_size)]
        return newPopulation
    
    def fitness (node: Node):
        return len(clauses) - node.heuristicFunction()
    
    def selectionPair (population: list[Node]) -> list[Node]:
        fitness_list = []
        for i in range (0, len(population)):
            fitness_list.append(fitness(population[i]))
        
        #? Choose two arbitrary nodes in the given population
        return choices(population = population, weights = fitness_list, k = 2)
    
    def crossover (nodePair: tuple[Node, Node]) -> tuple[Node, Node]:
        if (len(nodePair[0].state) != len(nodePair[1].state)):
            raise ValueError ("In the crossover function, the lengths of states in two nodes should be equal")
        
        length = len(nodePair[0].state)
        if (length < 2):
            return (nodePair[0], nodePair[1])
        
        cross_position = randint(0, length - 1)
        crossover_1 = Node(nodePair[0].state[:cross_position] + nodePair[1].state[cross_position:], clauses)
        crossover_2 = Node(nodePair[1].state[:cross_position] + nodePair[0].state[cross_position:], clauses)
        return (crossover_1, crossover_2)
    
    def mutation (node: Node, numMutablePositions: int = 1, probability: float = 0.2) -> Node:
        for _ in range (0, numMutablePositions):
            mutable_position = randint(0, len(node.state) - 1)
            if (random() <= probability):
                node.state[mutable_position] = -node.state[mutable_position]
                
        return node
    
    def findGoal (population: list[Node]) -> Node:
        for node in population:
            if (node.checkGoal()):
                return node
        return None
    
    #? Generate the initial state
    initialState = []
    for i in range (1, stateLength + 1):
        initialState.append(-i)
    
    #? Generate population with a specific size
    state_length = stateLength
    population_size = stateLength
    population = generatePopulation(state_length, population_size)
    
    #? Until solution was found, continue to generate new population
    solution = findGoal(population)
    while (solution is None):
        next_population = []
        
        for _ in range (0, int(population_size / 2)):
            #? Choose arbitrary pair of nodes in the old population and cross over
            parents = selectionPair(population)
            offspring_1, offspring_2 = crossover((parents[0], parents[1]))
            
            #? Take mutation with a specific probability (0.03 in default)
            offspring_1 = mutation(offspring_1)
            offspring_2 = mutation(offspring_2)
            
            #? Add offsprings to the next population
            next_population.append(offspring_1)
            next_population.append(offspring_2)
        
        population = next_population
        solution = findGoal(population)
        
    return solution.state