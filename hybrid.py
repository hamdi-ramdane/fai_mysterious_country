import random
import math
import time

# Step 1: Read cities from a file
def read_cities(file_path):
    cities = []
    with open(file_path, 'r') as file:
        for line in file:
            city_id, x, y = map(float, line.strip().replace(',', ' ').split())
            cities.append((city_id, (x, y)))
    return cities

# Step 2: Utility functions
def calculate_distance(individual, cities):
    distance = 0
    for i in range(len(individual)):
        city1 = cities[individual[i]][1]
        city2 = cities[individual[(i + 1) % len(individual)]][1]
        distance += math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
    return distance

def is_valid_cycle(individual, cities, max_distance):
    for i in range(len(individual)):
        city1 = cities[individual[i]][1]
        city2 = cities[individual[(i + 1) % len(individual)]][1]
        distance = math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
        if distance > max_distance:
            return False
    return True

# Step 3: Hill Climbing
def hill_climbing(cities, max_distance, max_iterations, initial_solution):
    num_cities = len(cities)
    current_solution = initial_solution[:]
    current_distance = calculate_distance(current_solution, cities)

    for iteration in range(max_iterations):
        next_solution = current_solution[:]
        i, j = random.sample(range(num_cities), 2)
        next_solution[i], next_solution[j] = next_solution[j], next_solution[i]

        if is_valid_cycle(next_solution, cities, max_distance):
            next_distance = calculate_distance(next_solution, cities)
            if next_distance < current_distance:
                current_solution = next_solution
                current_distance = next_distance

        if iteration % 100 == 0:
            print(f"Hill Climbing Iteration {iteration}: Current Distance = {current_distance}")

    return current_solution, current_distance

# Step 4: Genetic Algorithm
def initialize_population(cities, population_size):
    num_cities = len(cities)
    population = []
    for _ in range(population_size):
        individual = list(range(num_cities))
        random.shuffle(individual)
        population.append(individual)
    return population

def selection(population, fitness):
    total_fitness = sum(fitness)
    probabilities = [f / total_fitness for f in fitness]
    selected_index = random.choices(range(len(population)), weights=probabilities, k=1)[0]
    return population[selected_index]

def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[start:end+1] = parent1[start:end+1]

    current_index = (end + 1) % size
    for gene in parent2:
        if gene not in child:
            child[current_index] = gene
            current_index = (current_index + 1) % size
    return child

def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

def genetic_algorithm(cities, max_distance, population_size, generations, mutation_rate, hill_climbing_frequency):
    population = initialize_population(cities, population_size)
    fitness = [
        1 / (calculate_distance(ind, cities) + 1e-6)
        if is_valid_cycle(ind, cities, max_distance) else 0
        for ind in population
    ]

    for generation in range(generations):
        if all(f == 0 for f in fitness):
            population = initialize_population(cities, population_size)
            fitness = [
                1 / (calculate_distance(ind, cities) + 1e-6)
                if is_valid_cycle(ind, cities, max_distance) else 0
                for ind in population
            ]
            continue

        new_population = []
        best_individual = max(population, key=lambda ind: fitness[population.index(ind)])
        new_population.append(best_individual)

        while len(new_population) < population_size:
            parent1 = selection(population, fitness)
            parent2 = selection(population, fitness)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)

            if is_valid_cycle(child, cities, max_distance):
                new_population.append(child)

        population = new_population
        fitness = [
            1 / (calculate_distance(ind, cities) + 1e-6)
            if is_valid_cycle(ind, cities, max_distance) else 0
            for ind in population
        ]

        if generation % hill_climbing_frequency == 0:
            best_individual = max(population, key=lambda ind: fitness[population.index(ind)])
            best_individual, best_distance = hill_climbing(cities, max_distance, 100, best_individual)
            print(f"Generation {generation}: Best Distance = {best_distance}")

    best_individual = max(population, key=lambda ind: fitness[population.index(ind)])
    best_distance = calculate_distance(best_individual, cities)
    return best_individual, best_distance

# Step 5: Run the Hybrid Algorithm
if __name__ == "__main__":
    FILE_PATH = "data_100.csv"
    MAX_DISTANCE = 90
    POPULATION_SIZE = 50
    GENERATIONS = 1000
    MUTATION_RATE = 0.05
    HILL_CLIMBING_FREQUENCY = 10

    cities = read_cities(FILE_PATH)
    best_path, best_distance = genetic_algorithm(
        cities, MAX_DISTANCE, POPULATION_SIZE, GENERATIONS, MUTATION_RATE, HILL_CLIMBING_FREQUENCY
    )
    print("Best Path:", best_path)
    print("Best Distance:", best_distance)

