import random
ID = 'U2010050'
size = int(ID[-2:]) % 8 + 7
print("=====================")
print("My student ID is", ID)
print(f"My chessboard size is [{ID[-2:]} mod 8 + 7] => {size}x{size}", )
print("=====================")
POP_SIZE = 100
GENERATIONS = 1000

#FITNESS
def fitness(board):
    conflicts = 0
    for i in range(size):
        for j in range(i+1, size):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                conflicts += 1
    return conflicts

#CROSSOVER
def crossover(parent1, parent2):
    split = random.randint(1, size-1)
    child1 = parent1[:split] + parent2[split:]
    child2 = parent2[:split] + parent1[split:]
    return child1, child2
#MUTATE
def mutate(board):
    index = random.randint(0, size-1)
    value = random.randint(0, size-1)
    board[index] = value
    return board

# INITIAL POPULATION
def initial_population(pop_size):
    population = []
    for i in range(pop_size):
        board = [random.randint(0, size-1) for j in range(size)]
        population.append(board)
    return population
#GENETIC_ALGORITHM
def genetic_algorithm(pop_size, generations):
    population = initial_population(pop_size)
    for i in range(generations):
        population = sorted(population, key=lambda x: fitness(x))
        if fitness(population[0]) == 0:
            return population[0]
        parents = population[:pop_size//2]
        offspring = []
        for j in range(pop_size//2):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            offspring.append(child1)
            offspring.append(child2)
        population = parents + offspring
    return None

solution = genetic_algorithm(POP_SIZE, GENERATIONS)
if solution is not None:
    matrix = [['.' for i in range(size+1)] for j in range(size+1)]
    for i in range(1,size+1):
        matrix[0][i] = chr(ord('a') + i - 1)
        matrix[i][0] = i
    matrix[0][0] = ' ' 
    print("Found solution:", solution)
else:
    print("No solution found.")
