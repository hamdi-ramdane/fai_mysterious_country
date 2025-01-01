
import random
import math
import time

# Read cities from a file
def read_cities(file_path):
    cities = []
    with open(file_path, 'r') as file:
        for line in file:
            city_id, x, y = map(float, line.strip().replace(',', ' ').split())
            cities.append((city_id, (x, y)))
    return cities

# Calculate distance between cities
def calculate_distance(individual, cities):
    return sum(math.sqrt((cities[individual[i]][1][0] - cities[individual[(i + 1) % len(individual)]][1][0])**2 +
                         (cities[individual[i]][1][1] - cities[individual[(i + 1) % len(individual)]][1][1])**2)
               for i in range(len(individual)))

# Validate if the cycle is valid
def is_valid_cycle(individual, cities, max_distance):
    return all(math.sqrt((cities[individual[i]][1][0] - cities[individual[(i + 1) % len(individual)]][1][0])**2 +
                         (cities[individual[i]][1][1] - cities[individual[(i + 1) % len(individual)]][1][1])**2) <= max_distance
               for i in range(len(individual)))

# Initialize population
def initialize_population(cities, population_size):
    population = []
    num_cities = len(cities)
    for _ in range(population_size):
        individual = list(range(num_cities))
        random.shuffle(individual)
        population.append(individual)
    return population

# Selection, crossover, mutation, and hill climbing combined
def genetic_hill_climbing(cities, max_distance, population_size, generations, mutation_rate):
    population = initialize_population(cities, population_size)
    best_individual = min(population, key=lambda ind: calculate_distance(ind, cities))

    for generation in range(generations):
        # Calculate fitness and handle the case where all fitness values are zero
        fitness = [1 / (calculate_distance(ind, cities) + 1e-6) if is_valid_cycle(ind, cities, max_distance) else 0
                   for ind in population]
        
        # If all individuals are invalid, reinitialize the population
        if sum(fitness) == 0:
            population = initialize_population(cities, population_size)
            continue

        # Proceed with the genetic algorithm process
        new_population = [best_individual]

        while len(new_population) < population_size:
            parent1 = random.choices(population, weights=fitness, k=1)[0]
            parent2 = random.choices(population, weights=fitness, k=1)[0]
            start, end = sorted(random.sample(range(len(cities)), 2))
            child = [-1] * len(cities)
            child[start:end+1] = parent1[start:end+1]
            current_index = (end + 1) % len(cities)
            for gene in parent2:
                if gene not in child:
                    child[current_index] = gene
                    current_index = (current_index + 1) % len(cities)
            if random.random() < mutation_rate:
                i, j = random.sample(range(len(cities)), 2)
                child[i], child[j] = child[j], child[i]

            if is_valid_cycle(child, cities, max_distance):
                new_population.append(child)

        population = new_population
        best_individual = min(population, key=lambda ind: calculate_distance(ind, cities))

        # Hill climbing step: Local optimization for the best individual
        for i in range(100):  # Local search
            next_solution = best_individual[:]
            i, j = random.sample(range(len(cities)), 2)
            next_solution[i], next_solution[j] = next_solution[j], next_solution[i]
            if is_valid_cycle(next_solution, cities, max_distance):
                next_distance = calculate_distance(next_solution, cities)
                if next_distance < calculate_distance(best_individual, cities):
                    best_individual = next_solution

        if generation % 100 == 0:
            print(f"Generation {generation}: Best Distance = {calculate_distance(best_individual, cities)}")

    return best_individual, calculate_distance(best_individual, cities)

# Run the algorithm
if __name__ == "__main__":
    start_time = time.time()

    FILE_PATH = "data/data_100.csv"  
    MAX_DISTANCE = 90
    POPULATION_SIZE = 50
    GENERATIONS = 1000
    MUTATION_RATE = 0.05

    cities = read_cities(FILE_PATH)
    best_path, best_distance = genetic_hill_climbing(cities, MAX_DISTANCE, POPULATION_SIZE, GENERATIONS, MUTATION_RATE)
    
    print("Best Path:", best_path)
    print("Best Distance:", best_distance)

    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.4f} seconds")
