import tkinter as tk
from tkinter import ttk
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

###############################################################################
# FUNCIONES FIBONACCI
###############################################################################

def fibonacci(n: int):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

def fibonacci_dp(n: int, memo: dict = None):

    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n == 0:
        return 0
    if n == 1:
        return 1
    memo[n] = fibonacci_dp(n-1, memo) + fibonacci_dp(n-2, memo)
    return memo[n]

###############################################################################
# CLASE PRINCIPAL - ANALIZADOR FIBONACCI
###############################################################################

class AutoFibonacciAnalyzer:

    def __init__(self):
        self.windows = []  # Almacena referencias a las ventanas
        self.show_graphs()
    
    ###########################################################################
    # GENERACIÓN DE DATOS
    ###########################################################################
    
    def generate_time_data(self):

        n_values = list(range(0, 31, 2))
        times_normal = []
        times_dp = []
        
        for n in n_values:
            # Tiempo sin programación dinámica
            start_time = time.time()
            fibonacci(n)
            end_time = time.time()
            times_normal.append(end_time - start_time)
            
            # Tiempo con programación dinámica
            start_time = time.time()
            fibonacci_dp(n, {})
            end_time = time.time()
            times_dp.append(end_time - start_time)
        
        return n_values, times_normal, times_dp
    
    def generate_space_data(self):

        n_values = list(range(0, 51, 2))
        
        # Sin PD: complejidad O(n) por profundidad de recursión
        space_normal = [n for n in n_values]
        
        # Con PD: complejidad O(n) por diccionario de memoización
        space_dp = [n for n in n_values]
        
        return n_values, space_normal, space_dp
    
    ###########################################################################
    # CREACIÓN DE GRÁFICAS
    ###########################################################################
    
    def create_time_graph(self):

        n_values, times_normal, times_dp = self.generate_time_data()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Líneas de la gráfica
        ax.plot(n_values, times_normal, 'ro-', linewidth=2, markersize=6, 
                label='Sin Programación Dinámica')
        ax.plot(n_values, times_dp, 'bo-', linewidth=2, markersize=6, 
                label='Con Programación Dinámica')
        
        # Configuración de ejes y título
        ax.set_xlabel('n (tamaño de entrada)', fontsize=12)
        ax.set_ylabel('Tiempo de ejecución (segundos)', fontsize=12)
        ax.set_title('COMPLEJIDAD TEMPORAL - Fibonacci', fontsize=14, fontweight='bold')
        
        # Elementos de la gráfica
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_space_graph(self):

        n_values, space_normal, space_dp = self.generate_space_data()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Líneas de la gráfica
        ax.plot(n_values, space_normal, 'ro-', linewidth=2, markersize=6, 
                label='Sin Programación Dinámica')
        ax.plot(n_values, space_dp, 'bo-', linewidth=2, markersize=6, 
                label='Con Programación Dinámica')
        
        # Configuración de ejes y título
        ax.set_xlabel('n (tamaño de entrada)', fontsize=12)
        ax.set_ylabel('Espacio utilizado', fontsize=12)
        ax.set_title('COMPLEJIDAD ESPACIAL - Fibonacci', fontsize=14, fontweight='bold')
        
        # Elementos de la gráfica
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    ###########################################################################
    # MANEJO DE VENTANAS Y CERRADO
    ###########################################################################
    
    def exit_program(self):

        for window in self.windows:
            try:
                window.destroy()
            except:
                pass
        sys.exit()
    
    def on_window_close(self, window):

        self.windows.remove(window)
        window.destroy()
        if not self.windows:
            sys.exit()
    
    ###########################################################################
    # INTERFAZ GRÁFICA
    ###########################################################################
    
    def show_graphs(self):

        # VENTANA 1 - Gráfica Temporal
        time_window = tk.Tk()
        time_window.title("Complejidad Temporal - Fibonacci")
        time_window.geometry("800x600")
        time_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(time_window))
        self.windows.append(time_window)
        
        # Crear y empaquetar gráfica temporal
        fig_time = self.create_time_graph()
        canvas_time = FigureCanvasTkAgg(fig_time, time_window)
        canvas_time.draw()
        canvas_time.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame y botón para salir
        button_frame = ttk.Frame(time_window)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="Salir del Programa", 
                  command=self.exit_program).pack(side=tk.LEFT, padx=5)
        
        # VENTANA 2 - Gráfica Espacial
        space_window = tk.Tk()
        space_window.title("Complejidad Espacial - Fibonacci")
        space_window.geometry("800x600")
        space_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(space_window))
        self.windows.append(space_window)
        
        # Crear y empaquetar gráfica espacial
        fig_space = self.create_space_graph()
        canvas_space = FigureCanvasTkAgg(fig_space, space_window)
        canvas_space.draw()
        canvas_space.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame y botón para salir
        button_frame2 = ttk.Frame(space_window)
        button_frame2.pack(pady=5)
        ttk.Button(button_frame2, text="Salir del Programa", 
                  command=self.exit_program).pack(side=tk.LEFT, padx=5)
        
        # POSICIONAMIENTO DE VENTANAS
        time_window.geometry("+100+100")   # Ventana izquierda
        space_window.geometry("+900+100")  # Ventana derecha
        
        # INICIAR LOOP PRINCIPAL
        time_window.mainloop()

###############################################################################
# EJECUCIÓN PRINCIPAL
###############################################################################

def main():

    app = AutoFibonacciAnalyzer()

if __name__ == '__main__':
    main()