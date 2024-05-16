import random
import time
import matplotlib.pyplot as plt

def calculate_tour_cost(tour, distance_matrix):
    cost = 0
    n = len(tour)
    for i in range(n):
        city1 = tour[i]
        city2 = tour[(i + 1) % n]  # Tratăm turul ca un ciclu
        cost += distance_matrix[city1][city2]
    return cost

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

def two_opt(tour, distance_matrix, distance_cities, coord_cities, coordinates, city_index_map):
    n = len(tour)
    best_tour = tour[:]
    best_cost = calculate_tour_cost(tour, distance_matrix)
    improved = True
    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 1, n):
                new_tour = tour[:i] + tour[i:j][::-1] + tour[j:]
                new_cost = calculate_tour_cost(new_tour, distance_matrix)
                if new_cost < best_cost:
                    best_tour = new_tour[:]
                    best_cost = new_cost
                    improved = True
                    tour = new_tour  # Actualizăm turul pentru a evita copiile inutile
                    plot_tour_with_coordinates(tour, distance_cities, coord_cities, coordinates, city_index_map, color='blue', title='Traseul în timpul 2-opt')
    return best_tour, best_cost

def three_opt(tour, distance_matrix, distance_cities, coord_cities, coordinates, city_index_map):
    n = len(tour)
    best_tour = tour[:]
    best_cost = calculate_tour_cost(tour, distance_matrix)
    improved = True
    while improved:
        improved = False
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    new_tour = tour[:i] + tour[j:k] + tour[i:j] + tour[k:]
                    new_cost = calculate_tour_cost(new_tour, distance_matrix)
                    if new_cost < best_cost:
                        best_tour = new_tour[:]
                        best_cost = new_cost
                        improved = True
                        tour = new_tour  # Actualizăm turul pentru a evita copiile inutile
                        plot_tour_with_coordinates(tour, distance_cities, coord_cities, coordinates, city_index_map, color='green', title='Traseul în timpul 3-opt')
    return best_tour, best_cost

def generate_random_tour(n):
    tour = list(range(n))
    random.shuffle(tour)
    return tour

def read_distance_matrix(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
        cities = []
        distance_matrix = []
        for line in lines:
            parts = line.strip().split("|")
            if not cities:  # Dacă lista orașelor este goală, adăugăm numele orașelor
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
    city_index_map = {}  # Mapare între numele orașului și indexul său în listă
    with open(file_name, "r", encoding="utf-8") as file:
        next(file)  # Skip header
        for index, line in enumerate(file):
            parts = line.strip().split(",")
            city_name = parts[0].strip()  # Eliminăm spațiile în exces
            longitude = float(parts[1].strip())
            latitude = float(parts[2].strip())
            cities.append(city_name)
            coordinates.append((longitude, latitude))
            city_index_map[city_name] = index  # Adăugăm maparea pentru fiecare oraș
    return cities, coordinates, city_index_map

def local_search_with_plot(initial_tour, distance_matrix, cities, coord_cities, coordinates, city_index_map, max_iterations):
    current_tour = initial_tour[:]
    current_cost = calculate_tour_cost(current_tour, distance_matrix)
    best_tour = current_tour[:]
    best_cost = current_cost
    print("Distanța inițială:", current_cost)
    iteration = 0
    neighborhood_structures = [two_opt, three_opt]

    plt.ion()  # Activăm modul interactiv

    # Afișăm traseul inițial
    plot_tour_with_coordinates(initial_tour, cities, coord_cities, coordinates, city_index_map, color='gray', title='Traseul inițial')

    while iteration < max_iterations:
        improved = False
        for neighborhood in neighborhood_structures:
            new_tour, new_cost = neighborhood(current_tour, distance_matrix, cities, coord_cities, coordinates, city_index_map)
            if new_cost < best_cost:
                best_tour = new_tour[:]
                best_cost = new_cost
                current_tour = new_tour[:]
                current_cost = new_cost
                print("Iterația {}: Distanța optimă locală găsită: {}".format(iteration + 1, current_cost))
                improved = True
                break
        if not improved:
            break
        iteration += 1

    # Afișăm traseul final optim
    plot_tour_with_coordinates(best_tour, cities, coord_cities, coordinates, city_index_map, color='red', title='Traseul optim final')

    plt.ioff()  # Dezactivăm modul interactiv
    plt.show()  # Afișăm graficul final

    # Afișăm traseul optim găsit
    print("Traseul optim găsit:")
    print_tour(best_tour, cities)

    # Afișăm distanța totală calculată
    print("Distanta totala:", best_cost)

    return best_tour, best_cost

if __name__ == "__main__":
    file_name = "distance_matrix_top_maramures.txt"
    distance_cities, distance_matrix = read_distance_matrix(file_name)
    n = len(distance_matrix)
    initial_tour = generate_random_tour(n)
    max_iterations = 100

    file_name = "coordinates_top_maramures.txt"
    coord_cities, coordinates, city_index_map = read_coordinate_file(file_name)

    start_time = time.time()

    best_tour, best_cost = local_search_with_plot(initial_tour, distance_matrix, distance_cities, coord_cities, coordinates, city_index_map, max_iterations)

    end_time = time.time()
    execution_time = end_time - start_time

    print("Timpul de execuție:", execution_time, "secunde")
    print("Distanța turului optim local:", best_cost)
