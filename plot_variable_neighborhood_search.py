import random
import matplotlib.pyplot as plt


def read_distance_matrix(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        distance_matrix = [line.strip().split(" | ") for line in file.readlines()]
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
    city_names = list(coordinates.keys())  # Get the list of city names
    tour_names = [city_names[city] for city in tour]
    tour_names.append(tour_names[0])  # Add the first city at the end to complete the loop
    print("Tour:", " -> ".join(tour_names))


def calculate_tour_cost(tour, distance_matrix):
    cost = 0
    n = len(tour)
    for i in range(n):
        city1 = tour[i]
        city2 = tour[(i + 1) % n]  # We need a circular linkage between cities
        cost += int(distance_matrix[city1 + 1][city2 + 1].strip().split()[0])
    return cost


def plot_tour(tour, coordinates, title):
    city_names = list(coordinates.keys())  # Get the list of city names
    tour_coordinates = [coordinates[city_names[city - 1]] for city in tour]  # Adjust index by subtracting 1
    tour_coordinates.append(tour_coordinates[0])  # Connect back to the starting city
    x = [coord[0] for coord in tour_coordinates]
    y = [coord[1] for coord in tour_coordinates]
    plt.plot(x, y, marker='o', markersize=5, linestyle='-', color='b')

    # Add city names
    for city, (x, y) in zip(tour, tour_coordinates):
        plt.text(x, y, city_names[city - 1], fontsize=9, ha='center', va='bottom')

    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.show()


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


def insertion(tour, distance_matrix):
    n = len(tour)
    best_tour = tour[:]
    best_cost = calculate_tour_cost(tour, distance_matrix)
    for i in range(1, n):
        for j in range(n):
            if i != j:
                new_tour = tour[:i] + [tour[j]] + tour[i:j] + tour[j + 1:]
                new_cost = calculate_tour_cost(new_tour, distance_matrix)
                if new_cost < best_cost:
                    best_tour = new_tour[:]
                    best_cost = new_cost
    return best_tour, best_cost


def swap(tour, distance_matrix):
    n = len(tour)
    best_tour = tour[:]
    best_cost = calculate_tour_cost(tour, distance_matrix)
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            new_tour = tour[:]
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            new_cost = calculate_tour_cost(new_tour, distance_matrix)
            if new_cost < best_cost:
                best_tour = new_tour[:]
                best_cost = new_cost
    return best_tour, best_cost


def variable_neighborhood_search(initial_tour, distance_matrix, max_iterations):
    current_tour = initial_tour[:]
    current_cost = calculate_tour_cost(current_tour, distance_matrix)
    best_tour = current_tour[:]
    best_cost = current_cost

    # Plot the initial tour
    print("\nInitial Tour:")
    plot_tour(current_tour, coordinates, 'Initial Tour')

    print("Initial Distance:", current_cost)
    iteration = 0
    while iteration < max_iterations:
        neighborhood_structures = [two_opt, three_opt, insertion, swap]
        for neighborhood in neighborhood_structures:
            new_tour, new_cost = neighborhood(current_tour, distance_matrix)
            if new_cost < best_cost:
                best_tour = new_tour[:]
                best_cost = new_cost
                current_tour = new_tour[:]  # Set current tour to the best tour found in this neighborhood
                current_cost = new_cost
                print("Iteration {}: Found better local optimum: {}".format(iteration + 1, current_cost))

                # Plot the current tour after each improvement
                plot_tour(current_tour, coordinates, 'Intermediate Tour - Cost: {}'.format(current_cost))

        print("Iteration {}: Distance: {}".format(iteration + 1, current_cost))  # Afișează distanța la fiecare iterație
        iteration += 1

    # Plot the final tour
    print("\nFinal Tour:")
    plot_tour(best_tour, coordinates, 'Final Tour')

    return best_tour, best_cost



if __name__ == "__main__":
    file_name = "distance_matrix_top_maramures.txt"
    coordinates_file = "coordinates_top_maramures.txt"

    distance_matrix = read_distance_matrix(file_name)
    coordinates = read_coordinates(coordinates_file)
    n = len(distance_matrix) - 1

    initial_tour = list(range(n))
    max_iterations = 10  # Maximum number of iterations

    best_tour, best_cost = variable_neighborhood_search(initial_tour, distance_matrix, max_iterations)
    print("\nBest Tour:", best_tour)
    print("Best Distance:", best_cost)
    print_tour_with_names(best_tour, coordinates)
