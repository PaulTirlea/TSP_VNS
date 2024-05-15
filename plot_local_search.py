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
            row_data = [part.strip() for part in parts[1:]]  # Ignorăm primul element (indexul orașului)
            if not cities:  # Dacă lista orașelor este goală, adăugăm numele orașelor
                cities = row_data
            else:
                distances = [int(d) for d in row_data]  # Convertim distanțele în numere întregi
                distance_matrix.append(distances)
    return cities, distance_matrix


def print_tour(tour, cities):
    tour_names = [cities[city] for city in tour]
    tour_string = " -> ".join(tour_names)
    print(tour_string)


def local_search(initial_tour, distance_matrix, cities, max_iterations):
    current_tour = initial_tour[:]
    current_cost = calculate_tour_cost(current_tour, distance_matrix)
    best_tour = current_tour[:]
    best_cost = current_cost
    print("Distanța inițială:", current_cost)
    iteration = 0
    neighborhood_structures = [two_opt, three_opt]

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
                improved = True
                break
        if not improved:
            break
        iteration += 1

    # Afișăm traseul optim găsit
    print("Traseul optim găsit:")
    print_tour(best_tour, cities)

    # Afișăm distanța totală calculată
    print("Distanta totala:", best_cost)

    return best_tour, best_cost


def plot_tour(tour, cities, distance_matrix):
    # Extragem coordonatele fiecărui oraș din matricea de distanțe
    city_coordinates = [(distance_matrix[city][0], distance_matrix[city][1]) for city in tour]
    city_names = [cities[city] for city in tour]

    # Extragem coordonatele fiecărui oraș în parte
    x = [city[0] for city in city_coordinates]
    y = [city[1] for city in city_coordinates]

    # Plasăm fiecare nod (oraș) pe grafic
    plt.scatter(x, y, c='red', zorder=2)

    # Desenăm linii între noduri pentru a reprezenta traseul optim
    for i in range(len(tour) - 1):
        city1 = tour[i]
        city2 = tour[i + 1]
        plt.plot([distance_matrix[city1][0], distance_matrix[city2][0]],
                 [distance_matrix[city1][1], distance_matrix[city2][1]], 'b-', zorder=1)

    # Conectăm ultimul oraș cu primul pentru a închide traseul
    city1 = tour[-1]
    city2 = tour[0]
    plt.plot([distance_matrix[city1][0], distance_matrix[city2][0]],
             [distance_matrix[city1][1], distance_matrix[city2][1]], 'b-', zorder=1)

    # Adăugăm numele orașelor lângă noduri
    for i, name in enumerate(city_names):
        plt.text(x[i], y[i], '  ' + name, fontsize=8)

    plt.title('Traseul optim găsit')
    plt.xlabel('Coordonata X')
    plt.ylabel('Coordonata Y')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    file_name = "distance_matrix_top_maramures.txt"
    cities, distance_matrix = read_distance_matrix(file_name)
    n = len(distance_matrix)
    initial_tour = generate_random_tour(n)  # Generăm un tur inițial aleatoriu
    max_iterations = 100  # Numărul maxim de iterații

    start_time = time.time()

    best_tour, best_cost = local_search(initial_tour, distance_matrix, cities, max_iterations)

    # Afișăm traseul optim folosind funcția plot_tour
    plot_tour(best_tour, cities, distance_matrix)

    end_time = time.time()
    execution_time = end_time - start_time

    print("Timpul de execuție:", execution_time, "secunde")
    print("Distanța turului optim local:", best_cost)