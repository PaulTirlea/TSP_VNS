import random
import matplotlib.pyplot as plt


def read_distance_matrix(file_name):
    distance_matrix = {}
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
        cities = lines[0].strip().split(" | ")[1:]
        for line in lines[1:]:
            data = line.strip().split(" | ")
            city_name = data[0]
            distances = {cities[i]: int(data[i + 1].split()[0]) for i in range(len(cities))}
            distance_matrix[city_name] = distances
    return distance_matrix


def read_coordinates(file_name):
    coordinates = {}
    with open(file_name, "r", encoding="utf-8") as file:
        next(file)  # Skip header
        for line in file:
            name, longitude, latitude = line.strip().split(" | ")
            coordinates[name] = (float(longitude), float(latitude))
    return coordinates


def print_tour_with_names(tour, coordinates):
    tour_names = tour[:]
    tour_names.append(tour_names[0])
    print("Tur:", " -> ".join(tour_names))


def calculate_tour_cost(tour, distance_matrix):
    cost = 0
    n = len(tour)
    for i in range(n):
        city1 = tour[i]
        city2 = tour[(i + 1) % n]
        cost += distance_matrix[city1][city2]
    return cost


def two_opt(tour, distance_matrix):
    n = len(tour)
    best_tour = tour[:]
    best_cost = calculate_tour_cost(tour, distance_matrix)
    improved = True
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                new_tour = tour[:i] + tour[i:j][::-1] + tour[j:]
                new_cost = calculate_tour_cost(new_tour, distance_matrix)
                if new_cost < best_cost:
                    best_tour = new_tour[:]
                    best_cost = new_cost
                    improved = True
        tour = best_tour[:]
    return best_tour, best_cost


def three_opt(tour, distance_matrix):
    n = len(tour)
    best_tour = tour[:]
    best_cost = calculate_tour_cost(tour, distance_matrix)
    improved = True
    while improved:
        improved = False
        for i in range(1, n - 3):
            for j in range(i + 2, n - 1):
                for k in range(j + 2, n + (i > 0)):
                    new_tour = tour[:i] + tour[j:k] + tour[i:j] + tour[k:]
                    new_cost = calculate_tour_cost(new_tour, distance_matrix)
                    if new_cost < best_cost:
                        best_tour = new_tour[:]
                        best_cost = new_cost
                        improved = True
        tour = best_tour[:]
    return best_tour, best_cost


def plot_tour(tour, coordinates, distance_matrix, title):
    tour_coordinates = [coordinates[city] for city in tour]
    tour_coordinates.append(tour_coordinates[0])  # Connect back to the starting city
    x = [coord[0] for coord in tour_coordinates]
    y = [coord[1] for coord in tour_coordinates]
    plt.plot(x, y, marker='o', markersize=5, linestyle='-', color='b')

    # Adăugăm numele orașelor
    for city, (x, y) in coordinates.items():
        plt.text(x, y, city, fontsize=9, ha='center', va='bottom')

    # Adăugăm distanțele pe harta
    for i in range(len(tour) - 1):
        city1 = tour[i]
        city2 = tour[i + 1]
        distance = distance_matrix[city1][city2]
        plt.text((coordinates[city1][0] + coordinates[city2][0]) / 2,
                 (coordinates[city1][1] + coordinates[city2][1]) / 2,
                 str(distance), fontsize=8, ha='center', va='bottom')

    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    distance_matrix_file = "distance_matrix_top_maramures.txt"
    coordinates_file = "coordinates_top_maramures.txt"

    distance_matrix = read_distance_matrix(distance_matrix_file)
    coordinates = read_coordinates(coordinates_file)

    initial_tour = list(distance_matrix.keys())
    initial_cost = calculate_tour_cost(initial_tour, distance_matrix)

    print("Traseul inițial:")
    print_tour_with_names(initial_tour, coordinates)
    plot_tour(initial_tour, coordinates, distance_matrix, 'Traseul inițial')

    best_tour, best_cost = two_opt(initial_tour, distance_matrix)
    best_tour, best_cost = three_opt(best_tour, distance_matrix)

    print("Cel mai bun tur găsit:")
    print_tour_with_names(best_tour, coordinates)
    print("Distanța turului optim local:", best_cost)
    plot_tour(best_tour, coordinates, distance_matrix, 'Traseul final')
