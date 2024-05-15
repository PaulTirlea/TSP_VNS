import random
import time

def calculate_tour_cost(tour, distance_matrix):
    cost = 0
    n = len(tour)
    for i in range(n):
        city1 = tour[i]
        city2 = tour[(i + 1) % n]  # Tratăm turul ca un ciclu
        cost += distance_matrix[city1][city2]
    return cost

def two_opt(tour, distance_matrix):
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
    return best_tour, best_cost

def three_opt(tour, distance_matrix):
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
    return best_tour, best_cost

def insertion(tour, distance_matrix):
    n = len(tour)
    best_tour = tour[:]
    best_cost = calculate_tour_cost(tour, distance_matrix)
    for i in range(n):
        for j in range(n):
            if i != j:
                new_tour = tour[:]
                city = new_tour.pop(i)
                new_tour.insert(j, city)
                new_cost = calculate_tour_cost(new_tour, distance_matrix)
                if new_cost < best_cost:
                    best_tour = new_tour[:]
                    best_cost = new_cost
    return best_tour, best_cost

def swap(tour, distance_matrix):
    n = len(tour)
    best_tour = tour[:]
    best_cost = calculate_tour_cost(tour, distance_matrix)
    for i in range(n - 1):
        for j in range(i + 1, n):
            new_tour = tour[:]
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            new_cost = calculate_tour_cost(new_tour, distance_matrix)
            if new_cost < best_cost:
                best_tour = new_tour[:]
                best_cost = new_cost
    return best_tour, best_cost

def generate_random_tour(n):
    tour = list(range(n))
    random.shuffle(tour)
    return tour

def generate_perturbed_tour(tour):
    n = len(tour)
    perturbed_tour = tour[:]
    num_changes = random.randint(1, n // 4)  # Controlăm gradul de perturbare
    for _ in range(num_changes):
        i, j = random.sample(range(n), 2)
        perturbed_tour[i], perturbed_tour[j] = perturbed_tour[j], perturbed_tour[i]
    return perturbed_tour

def read_distance_matrix(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        distance_matrix = [list(map(int, line.strip().split())) for line in file.readlines()]
    return distance_matrix

def print_tour(tour):
    tour_string = " -> ".join(str(city + 1) for city in tour)
    print(tour_string)

def variable_neighborhood_search(initial_tour, distance_matrix, max_iterations, diversification_interval):
    current_tour = initial_tour[:]
    current_cost = calculate_tour_cost(current_tour, distance_matrix)
    best_tour = current_tour[:]
    best_cost = current_cost
    print("Distanța inițială:", current_cost)
    iteration = 0
    diversification_counter = 0
    neighborhood_structures = [two_opt, three_opt, insertion, swap]
    explored_solutions = set()

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
                diversification_counter = 0  # Resetăm contorul de diversificare
                improved = True
                break
        if not improved:
            diversification_counter += 1
        iteration += 1

        # Verificăm dacă trebuie să aplicăm mecanismul de diversificare
        if diversification_counter >= diversification_interval:
            print("Aplicăm mecanismul de diversificare...")
            perturbed_tour = generate_perturbed_tour(current_tour)
            perturbed_cost = calculate_tour_cost(perturbed_tour, distance_matrix)
            while tuple(perturbed_tour) in explored_solutions:
                perturbed_tour = generate_perturbed_tour(current_tour)
                perturbed_cost = calculate_tour_cost(perturbed_tour, distance_matrix)
            current_tour = perturbed_tour
            current_cost = perturbed_cost
            diversification_counter = 0

        explored_solutions.add(tuple(current_tour))

    # Afișăm traseul optim găsit
    print("Traseul optim găsit:")
    print_tour(best_tour)

    # Afișăm distanța totală calculată
    print("Distanta totala:", best_cost)

    return best_tour, best_cost

if __name__ == "__main__":
    file_name = "test-dataset.txt"
    distance_matrix = read_distance_matrix(file_name)
    n = len(distance_matrix)
    initial_tour = generate_random_tour(n)  # Generăm un tur inițial aleatoriu
    max_iterations = 100  # Numărul maxim de iterații
    diversification_interval = 20  # Intervalul de diversificare

    start_time = time.time()

    best_tour, best_cost = variable_neighborhood_search(initial_tour, distance_matrix, max_iterations, diversification_interval)

    end_time = time.time()
    execution_time = end_time - start_time

    print("Timpul de execuție:", execution_time, "secunde")
    print("Distanța turului optim local:", best_cost)
