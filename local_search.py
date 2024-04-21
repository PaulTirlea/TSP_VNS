import random

def read_distance_matrix(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        distance_matrix = [line.strip().split(" | ") for line in file.readlines()]
    return distance_matrix

def print_tour_with_names(tour, distance_matrix):
    city_names = distance_matrix[0][1:]
    tour_names = [city_names[int(city)] for city in tour]
    tour_names.append(tour_names[0])
    print("Tur:", " -> ".join(tour_names))

def calculate_tour_cost(tour, distance_matrix):
    cost = 0
    n = len(tour)
    for i in range(n):
        city1 = tour[i]
        city2 = tour[(i + 1) % n]  # Avem nevoie de o legătură circulară între orașe
        cost += int(distance_matrix[city1 + 1][city2 + 1].strip().split()[0])
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

if __name__ == "__main__":
    file_name = "distance_matrix_top_maramures.txt"
    distance_matrix = read_distance_matrix(file_name)
    n = len(distance_matrix) - 1
    initial_tour = list(range(n))
    best_tour, best_cost = two_opt(initial_tour, distance_matrix)
    best_tour, best_cost = three_opt(best_tour, distance_matrix)
    print("Cel mai bun tur găsit:")
    print_tour_with_names(best_tour, distance_matrix)
    print("Distanța turului optim local:", best_cost)

