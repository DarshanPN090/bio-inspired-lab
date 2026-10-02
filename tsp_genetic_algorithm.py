import random
import math


# --------------------------------------------------
# 1. Calculate distance between two cities
# --------------------------------------------------
def calculate_distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# --------------------------------------------------
# 2. Calculate total distance of a route
# --------------------------------------------------
def total_distance(route, cities):
    distance = 0

    for i in range(len(route)):
        current_city = cities[route[i]]
        next_city = cities[route[(i + 1) % len(route)]]

        distance += calculate_distance(current_city, next_city)

    return distance


# --------------------------------------------------
# 3. Create the initial population
# --------------------------------------------------
def create_population(population_size, number_of_cities):
    population = []

    for _ in range(population_size):
        route = list(range(number_of_cities))
        random.shuffle(route)
        population.append(route)

    return population


# --------------------------------------------------
# 4. Selection
# Select the best routes from the population
# --------------------------------------------------
def selection(population, cities, selection_size):
    ranked_population = sorted(
        population,
        key=lambda route: total_distance(route, cities)
    )

    return ranked_population[:selection_size]


# --------------------------------------------------
# 5. Crossover
# Order Crossover (OX)
# --------------------------------------------------
def crossover(parent1, parent2):
    start, end = sorted(
        random.sample(range(len(parent1)), 2)
    )

    child = [None] * len(parent1)

    # Copy part of parent1
    child[start:end] = parent1[start:end]

    # Fill remaining positions using parent2
    remaining = [
        city for city in parent2
        if city not in child
    ]

    index = 0

    for i in range(len(child)):
        if child[i] is None:
            child[i] = remaining[index]
            index += 1

    return child


# --------------------------------------------------
# 6. Mutation
# Swap two cities in the route
# --------------------------------------------------
def mutation(route, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)

        route[i], route[j] = route[j], route[i]

    return route


# --------------------------------------------------
# 7. Create the next generation
# --------------------------------------------------
def create_next_generation(
    population,
    cities,
    population_size,
    mutation_rate
):

    elite_size = population_size // 5

    # Select best individuals
    elites = selection(
        population,
        cities,
        elite_size
    )

    new_population = elites.copy()

    while len(new_population) < population_size:

        parent1 = random.choice(elites)
        parent2 = random.choice(elites)

        child = crossover(parent1, parent2)

        child = mutation(
            child,
            mutation_rate
        )

        new_population.append(child)

    return new_population


# --------------------------------------------------
# 8. Genetic Algorithm
# --------------------------------------------------
def genetic_algorithm(
    cities,
    population_size=100,
    generations=500,
    mutation_rate=0.02
):

    number_of_cities = len(cities)

    # Create initial population
    population = create_population(
        population_size,
        number_of_cities
    )

    best_route = None
    best_distance = float("inf")

    for generation in range(generations):

        # Find best route in current population
        current_best = min(
            population,
            key=lambda route: total_distance(route, cities)
        )

        current_distance = total_distance(
            current_best,
            cities
        )

        # Update overall best solution
        if current_distance < best_distance:
            best_distance = current_distance
            best_route = current_best.copy()

        # Create next generation
        population = create_next_generation(
            population,
            cities,
            population_size,
            mutation_rate
        )

        # Display progress
        if (generation + 1) % 50 == 0:
            print(
                f"Generation {generation + 1}: "
                f"Best Distance = {best_distance:.2f}"
            )

    return best_route, best_distance


# --------------------------------------------------
# 9. Main Program
# --------------------------------------------------
if __name__ == "__main__":

    # City coordinates
    # A = (2, 3)
    # B = (5, 8)
    # C = (9, 2)
    # D = (12, 7)
    # E = (6, 12)
    # F = (1, 10)

    cities = {
        0: (2, 3),     # A
        1: (5, 8),     # B
        2: (9, 2),     # C
        3: (12, 7),    # D
        4: (6, 12),    # E
        5: (1, 10)     # F
    }

    city_names = ["A", "B", "C", "D", "E", "F"]

    print("=" * 50)
    print("TRAVELLING SALESMAN PROBLEM")
    print("GENETIC ALGORITHM")
    print("=" * 50)

    print("\nCities:")
    for city, coordinate in cities.items():
        print(f"{city_names[city]} -> {coordinate}")

    # Run Genetic Algorithm
    best_route, best_distance = genetic_algorithm(
        cities,
        population_size=100,
        generations=500,
        mutation_rate=0.02
    )

    # Convert route numbers to city names
    route_names = [
        city_names[city]
        for city in best_route
    ]

    # Return to starting city
    route_names.append(route_names[0])

    print("\n" + "=" * 50)
    print("FINAL RESULT")
    print("=" * 50)

    print("Best Route:")
    print(" -> ".join(route_names))

    print(f"\nMinimum Distance: {best_distance:.2f}")
