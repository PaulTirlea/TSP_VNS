from geopy.distance import geodesic
from get_input import maramures_communes_data  # Importăm lista de comune din Maramureș

# Sortăm comunele după numărul de locuitori
maramures_communes_data.sort(key=lambda x: x.get("population", 0), reverse=True)

# Luăm doar primele 10 cele mai mari localități
top_10_communes = maramures_communes_data[:100]

# Numele fișierului pentru lista cu cele 10 cele mai mari localități și coordonatele lor
file_name_communes = "coordinates_top_maramures.txt"

# Scriem informațiile în fișierul text pentru localități și coordonatele lor
with open(file_name_communes, "w", encoding="utf-8") as file:
    file.write("Nume localitate | Longitudine | Latitudine\n")
    for commune in top_10_communes:
        name = commune["name"]
        lon = commune["lon"]
        lat = commune["lat"]
        file.write(f"{name} | {lon} | {lat}\n")

print(f"Lista cu cele 10 cele mai mari localități și coordonatele lor a fost salvată în fișierul {file_name_communes}.")

# Creăm o matrice goală pentru a stoca distanțele între cele 10 cele mai mari localități
num_top_communes = len(top_10_communes)
distance_matrix = [["Null" for _ in range(num_top_communes + 1)] for _ in range(num_top_communes + 1)]

# Adăugăm numele localităților în prima linie și prima coloană a matricei de adiacență
for i, commune_info in enumerate(top_10_communes):
    distance_matrix[i + 1][0] = commune_info["name"]
    distance_matrix[0][i + 1] = commune_info["name"]

# Calculăm și adăugăm distanțele în matricea de adiacență
for i, commune1_info in enumerate(top_10_communes):
    for j, commune2_info in enumerate(top_10_communes):
        if i == j:
            distance_matrix[i + 1][j + 1] = "0 km"
        else:
            distance = geodesic((commune1_info["lat"], commune1_info["lon"]), (commune2_info["lat"], commune2_info["lon"])).kilometers
            distance_matrix[i + 1][j + 1] = f"{distance:.0f} km"

# Numele fișierului pentru matricea de adiacență
file_name_matrix = "distance_matrix_top_maramures.txt"

# Scriem matricea de adiacență în fișierul text
with open(file_name_matrix, "w", encoding="utf-8") as file:
    for row in distance_matrix:
        file.write(" | ".join(row) + "\n")

print(f"Matricea de distanțe pentru cele 10 cele mai mari localități a fost salvată în fișierul {file_name_matrix}.")
