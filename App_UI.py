import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from plot_variable_neighborhood_search import read_distance_matrix, read_coordinate_file, generate_random_tour, \
    variable_neighborhood_search, plot_tour_with_coordinates
import io
from PIL import Image, ImageTk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimizare Traseu")

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.file_label = tk.Label(self.frame, text="Alege fișierul de distanțe:")
        self.file_label.grid(row=0, column=0, padx=5, pady=5)

        self.file_entry = tk.Entry(self.frame, width=50)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5)

        self.file_button = tk.Button(self.frame, text="Browse", command=self.browse_file)
        self.file_button.grid(row=0, column=2, padx=5, pady=5)

        self.iter_label = tk.Label(self.frame, text="Număr maxim de iterații:")
        self.iter_label.grid(row=1, column=0, padx=5, pady=5)

        self.iter_entry = tk.Entry(self.frame)
        self.iter_entry.insert(0, "100")
        self.iter_entry.grid(row=1, column=1, padx=5, pady=5)

        self.div_label = tk.Label(self.frame, text="Interval de diversificare:")
        self.div_label.grid(row=2, column=0, padx=5, pady=5)

        self.div_entry = tk.Entry(self.frame)
        self.div_entry.insert(0, "20")
        self.div_entry.grid(row=2, column=1, padx=5, pady=5)

        self.start_button = tk.Button(self.frame, text="Optimizează", command=self.optimize)
        self.start_button.grid(row=3, column=0, columnspan=3, pady=10)

        self.result_label = tk.Label(self.frame, text="Rezultate")
        self.result_label.grid(row=4, column=0, columnspan=3)

        self.result_text = tk.Text(self.frame, height=10, width=50)
        self.result_text.grid(row=5, column=0, columnspan=3, pady=10)

        self.plot_label = tk.Label(self.frame)
        self.plot_label.grid(row=6, column=0, columnspan=3, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.file_entry.insert(0, file_path)

    def optimize(self):
        file_path = self.file_entry.get()
        max_iterations = int(self.iter_entry.get())
        diversification_interval = int(self.div_entry.get())

        try:
            distance_cities, distance_matrix = read_distance_matrix(file_path)
            coord_cities, coordinates, city_index_map = read_coordinate_file("coordinates_top_maramures.txt")

            initial_tour = generate_random_tour(len(distance_matrix))

            best_tour, best_cost = variable_neighborhood_search(
                initial_tour, distance_matrix, distance_cities, coord_cities, coordinates,
                city_index_map, max_iterations, diversification_interval
            )

            self.result_text.insert(tk.END, f"Costul optim: {best_cost}\n")
            self.display_plot(best_tour, distance_cities, coord_cities, coordinates, city_index_map)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_plot(self, best_tour, distance_cities, coord_cities, coordinates, city_index_map):
        plt.figure()
        plot_tour_with_coordinates(best_tour, distance_cities, coord_cities, coordinates, city_index_map, color='green', title='Traseul optim final')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img = Image.open(buf)
        img_tk = ImageTk.PhotoImage(img)

        self.plot_label.configure(image=img_tk)
        self.plot_label.image = img_tk

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
