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

# Step 3: Hill Climbing Algorithm
def hill_climbing(cities, max_distance, max_iterations):
    num_cities = len(cities)
    current_solution = list(range(num_cities))
    random.shuffle(current_solution)

    while not is_valid_cycle(current_solution, cities, max_distance):
        random.shuffle(current_solution)
    print(current_solution)
    current_distance = calculate_distance(current_solution, cities)
    print(current_distance)
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
            print(f"Iteration {iteration}: Current Distance = {current_distance}")

    return current_solution, current_distance

# Step 4: Run the algorithm
if __name__ == "__main__":
    start_time = time.time()

    FILE_PATH = "data/data_100.csv"  
    MAX_DISTANCE = 90
    MAX_ITERATIONS = 1000

    cities = read_cities(FILE_PATH)

    best_path, best_distance = hill_climbing(cities, MAX_DISTANCE, MAX_ITERATIONS)
    print("Best Path:", best_path)
    print("Best Distance:", best_distance)
    


    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.4f} seconds")


