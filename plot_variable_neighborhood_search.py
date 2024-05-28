import random
import time
import matplotlib.pyplot as plt

def calculate_tour_cost(tour, distance_matrix):
    return sum(distance_matrix[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour)))

def two_opt(tour, distance_matrix):
    n = len(tour)
    best_cost = calculate_tour_cost(tour, distance_matrix)
    while True:
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n + (i > 0)):  # Ensuring no adjacent edges are swapped
                new_tour = tour[:i] + tour[i:j][::-1] + tour[j:]
                new_cost = calculate_tour_cost(new_tour, distance_matrix)
                if new_cost < best_cost:
                    tour, best_cost = new_tour, new_cost
                    improved = True
        if not improved:
            break
    return tour, best_cost

def three_opt(tour, distance_matrix):
    n = len(tour)
    best_cost = calculate_tour_cost(tour, distance_matrix)
    while True:
        improved = False
        for i in range(n - 2):
            for j in range(i + 2, n - 1):
                for k in range(j + 2, n + (i > 0)):
                    new_tour = tour[:i] + tour[j:k] + tour[i:j] + tour[k:]
                    new_cost = calculate_tour_cost(new_tour, distance_matrix)
                    if new_cost < best_cost:
                        tour, best_cost = new_tour, new_cost
                        improved = True
        if not improved:
            break
    return tour, best_cost

def insertion(tour, distance_matrix):
    n = len(tour)
    best_cost = calculate_tour_cost(tour, distance_matrix)
    for i in range(n):
        for j in range(n):
            if i != j:
                new_tour = tour[:]
                city = new_tour.pop(i)
                new_tour.insert(j, city)
                new_cost = calculate_tour_cost(new_tour, distance_matrix)
                if new_cost < best_cost:
                    tour, best_cost = new_tour, new_cost
    return tour, best_cost

def swap(tour, distance_matrix):
    n = len(tour)
    best_cost = calculate_tour_cost(tour, distance_matrix)
    for i in range(n - 1):
        for j in range(i + 1, n):
            new_tour = tour[:]
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            new_cost = calculate_tour_cost(new_tour, distance_matrix)
            if new_cost < best_cost:
                tour, best_cost = new_tour, new_cost
    return tour, best_cost

def generate_random_tour(n):
    tour = list(range(n))
    random.shuffle(tour)
    return tour

def generate_perturbed_tour(tour):
    n = len(tour)
    num_changes = random.randint(1, n // 4)
    for _ in range(num_changes):
        i, j = random.sample(range(n), 2)
        tour[i], tour[j] = tour[j], tour[i]
    return tour

def read_distance_matrix(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
        cities = []
        distance_matrix = []
        for line in lines:
            parts = line.strip().split("|")
            if not cities:
                cities = [part.strip() for part in parts[1:]]
            else:
                distances = [int(d) for d in parts[1:]]
                distance_matrix.append(distances)
    return cities, distance_matrix

def print_tour(tour, cities):
    tour_names = [cities[city] for city in tour]
    tour_string = " -> ".join(tour_names)
    print(tour_string)

def read_coordinate_file(file_name):
    cities = []
    coordinates = []
    city_index_map = {}
    with open(file_name, "r", encoding="utf-8") as file:
        next(file)
        for index, line in enumerate(file):
            parts = line.strip().split(",")
            city_name = parts[0].strip()
            longitude = float(parts[1].strip())
            latitude = float(parts[2].strip())
            cities.append(city_name)
            coordinates.append((longitude, latitude))
            city_index_map[city_name] = index
    return cities, coordinates, city_index_map

def plot_tour_with_coordinates(tour, distance_cities, coord_cities, coordinates, city_index_map, color='gray', title=''):
    city_coordinates = []
    missing_cities = []

    for city_index in tour:
        city_name = distance_cities[city_index]
        if city_name in city_index_map:
            city_coordinates.append(coordinates[city_index_map[city_name]])
        else:
            missing_cities.append(city_name)

    if missing_cities:
        print("Următoarele orașe nu au fost găsite în city_index_map:")
        for city in missing_cities:
            print(city)
        return

    city_names = [distance_cities[city_index] for city_index in tour]

    x = [coord[0] for coord in city_coordinates]
    y = [coord[1] for coord in city_coordinates]

    plt.scatter(x, y, c='red', zorder=2)

    for i in range(len(tour) - 1):
        city1 = city_coordinates[i]
        city2 = city_coordinates[i + 1]
        plt.plot([city1[0], city2[0]], [city1[1], city2[1]], color, zorder=1)

    city1 = city_coordinates[-1]
    city2 = city_coordinates[0]
    plt.plot([city1[0], city2[0]], [city1[1], city2[1]], color, zorder=1)

    for i, name in enumerate(city_names):
        plt.text(x[i], y[i], '  ' + name, fontsize=8)

    plt.title(title)
    plt.xlabel('Longitudine')
    plt.ylabel('Latitudine')
    plt.grid(True)
    plt.draw()
    plt.pause(0.1)
    plt.clf()

def variable_neighborhood_search(initial_tour, distance_matrix, distance_cities, coord_cities, coordinates, city_index_map, max_iterations, diversification_interval):
    current_tour = initial_tour[:]
    current_cost = calculate_tour_cost(current_tour, distance_matrix)
    best_tour = current_tour[:]
    best_cost = current_cost
    print("Distanța inițială:", current_cost)
    iteration = 0
    diversification_counter = 0
    neighborhood_structures = [two_opt, three_opt, insertion, swap]
    explored_solutions = set()

    plt.ion()

    plot_tour_with_coordinates(initial_tour, distance_cities, coord_cities, coordinates, city_index_map, color='gray', title='Traseul inițial')

    while iteration < max_iterations:
        improved = False
        for neighborhood in neighborhood_structures:
            new_tour, new_cost = neighborhood(current_tour, distance_matrix)
            if new_cost < best_cost:
                best_tour = new_tour[:]
                best_cost = new_cost
                current_tour = new_tour[:]
                current_cost = new_cost
                print("Iterația {}: Distanța optimă locală găsită: {}".format(iteration + 1, current_cost))
                diversification_counter = 0
                improved = True
                plot_tour_with_coordinates(current_tour, distance_cities, coord_cities, coordinates, city_index_map, color='blue', title=f'Iterația {iteration + 1}')
                break
        if not improved:
            diversification_counter += 1
        iteration += 1

        if diversification_counter >= diversification_interval:
            print("Aplicăm mecanismul de diversificare...")
            perturbed_tour = generate_perturbed_tour(current_tour)
            perturbed_cost = calculate_tour_cost(perturbed_tour, distance_matrix)
            if perturbed_cost < best_cost:
                current_tour = perturbed_tour
                current_cost = perturbed_cost
                best_tour = perturbed_tour[:]
                best_cost = perturbed_cost
                diversification_counter = 0
                print("Diversificarea a condus la o îmbunătățire: {}".format(current_cost))

        explored_solutions.add(tuple(current_tour))

    plt.ioff()

    print("Traseul optim găsit:")
    print_tour(best_tour, distance_cities)

    print("Distanta totala:", best_cost)

    plot_tour_with_coordinates(best_tour, distance_cities, coord_cities, coordinates, city_index_map, color='green', title='Traseul optim final')

    return best_tour, best_cost

if __name__ == "__main__":
    distance_file_name = "distance_matrix_top_maramures.txt"
    coord_file_name = "coordinates_top_maramures.txt"

    distance_cities, distance_matrix = read_distance_matrix(distance_file_name)
    n = len(distance_matrix)

    coord_cities, coordinates, city_index_map = read_coordinate_file(coord_file_name)

    initial_tour = generate_random_tour(n)
    max_iterations = 100
    diversification_interval = 20

    start_time = time.time()

    best_tour, best_cost = variable_neighborhood_search(initial_tour, distance_matrix, distance_cities, coord_cities,
                                                        coordinates, city_index_map, max_iterations,
                                                        diversification_interval)

    end_time = time.time()
    execution_time = end_time - start_time

    print("Timpul de execuție:", execution_time, "secunde")
    print("Distanța turului optim local:", best_cost)
