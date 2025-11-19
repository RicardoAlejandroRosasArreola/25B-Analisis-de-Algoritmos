import math
import random
import tkinter as tk
from tkinter import messagebox

def eval(A, B):
    x1, y1 = A
    x2, y2 = B
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def encontrar_par_mas_cercano(puntos):
    min_distancia = float('inf')
    par_cercano = None
    
    for i in range(len(puntos)):
        for j in range(i + 1, len(puntos)):
            distancia = eval(puntos[i], puntos[j])
            if distancia < min_distancia:
                min_distancia = distancia
                par_cercano = (puntos[i], puntos[j])
    
    return par_cercano, min_distancia

# ========== MODO CONSOLA ==========
def generar_puntos_aleatorios():
    puntos = []
    for i in range(5):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        puntos.append([x, y])
    return puntos

def mostrar_puntos(puntos):
    print("\nPuntos:")
    print("Punto\tX\tY")
    for i, punto in enumerate(puntos):
        print(f"P{i+1}\t{punto[0]}\t{punto[1]}")

def modo_consola():
    print("=== PAR MAS CERCANO (Modo Consola) ===")
    
    # Generar puntos aleatorios
    puntos = generar_puntos_aleatorios()
    mostrar_puntos(puntos)
    
    # Calcular par más cercano
    par_cercano, distancia = encontrar_par_mas_cercano(puntos)
    
    # Mostrar resultado
    if par_cercano:
        p1, p2 = par_cercano
        print(f"\nEl par mas cercano son los puntos {p1} y {p2}")
        print(f"Distancia: {distancia:.6f}")
    else:
        print("\nNo se encontro ningun par")

# ========== MODO GRÁFICO ==========
class ParMasCercanoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Par mas cercano")
        self.root.geometry("600x550")
        
        self.List1 = []
        self.List2 = []
        self.List3 = []
        self.List4 = []
        self.List5 = []
        self.T = [self.List1, self.List2, self.List3, self.List4, self.List5]
        
        self.par_cercano = None
        self.distancia = 0
        
        self.crear_interfaz()
        self.llenar_random()
    
    def crear_interfaz(self):
        titulo = tk.Label(self.root, text="Par mas cercano", font=("Arial", 16))
        titulo.pack(pady=20)
        
        frame_puntos = tk.Frame(self.root)
        frame_puntos.pack(pady=15)
        
        tk.Label(frame_puntos, text="Punto", font=("Arial", 12)).grid(row=0, column=0, padx=15, pady=10)
        tk.Label(frame_puntos, text="X", font=("Arial", 12)).grid(row=0, column=1, padx=15, pady=10)
        tk.Label(frame_puntos, text="Y", font=("Arial", 12)).grid(row=0, column=2, padx=15, pady=10)
        
        self.entries_x = []
        self.entries_y = []
        
        for i in range(5):
            label_punto = tk.Label(frame_puntos, text=f"P{i+1}", font=("Arial", 10))
            label_punto.grid(row=i+1, column=0, padx=15, pady=8)
            
            entry_x = tk.Entry(frame_puntos, width=10, font=("Arial", 10))
            entry_x.grid(row=i+1, column=1, padx=15, pady=8)
            
            entry_y = tk.Entry(frame_puntos, width=10, font=("Arial", 10))
            entry_y.grid(row=i+1, column=2, padx=15, pady=8)
            
            self.entries_x.append(entry_x)
            self.entries_y.append(entry_y)
        
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=20)
        
        btn_calcular = tk.Button(frame_botones, text="Calcular", command=self.calcular, font=("Arial", 10), width=12, height=1)
        btn_calcular.grid(row=0, column=0, padx=10, pady=10)
        
        btn_aleatorio = tk.Button(frame_botones, text="Llenar random", command=self.llenar_random, font=("Arial", 10), width=12, height=1)
        btn_aleatorio.grid(row=0, column=1, padx=10, pady=10)
        
        btn_limpiar = tk.Button(frame_botones, text="Limpiar", command=self.limpiar, font=("Arial", 10), width=12, height=1)
        btn_limpiar.grid(row=0, column=2, padx=10, pady=10)
        
        self.label_resultado = tk.Label(self.root, text="", font=("Arial", 12), wraplength=500, justify="center")
        self.label_resultado.pack(pady=25)
    
    def actualizar_T_desde_interfaz(self):
        for i in range(5):
            try:
                x = int(self.entries_x[i].get())
                y = int(self.entries_y[i].get())
                self.T[i] = [x, y]
            except ValueError:
                messagebox.showerror("Error", f"Valores numericos invalidos para P{i+1}")
                return False
        return True
    
    def actualizar_interfaz_desde_T(self):
        for i in range(5):
            if len(self.T[i]) == 2:
                self.entries_x[i].delete(0, tk.END)
                self.entries_x[i].insert(0, str(self.T[i][0]))
                self.entries_y[i].delete(0, tk.END)
                self.entries_y[i].insert(0, str(self.T[i][1]))
    
    def llenar_random(self):
        self.List1 = [random.randint(0, 100), random.randint(0, 100)]
        self.List2 = [random.randint(0, 100), random.randint(0, 100)]
        self.List3 = [random.randint(0, 100), random.randint(0, 100)]
        self.List4 = [random.randint(0, 100), random.randint(0, 100)]
        self.List5 = [random.randint(0, 100), random.randint(0, 100)]
        self.T = [self.List1, self.List2, self.List3, self.List4, self.List5]
        
        self.actualizar_interfaz_desde_T()
        self.label_resultado.config(text="")
    
    def limpiar(self):
        self.List1 = [0, 0]
        self.List2 = [0, 0]
        self.List3 = [0, 0]
        self.List4 = [0, 0]
        self.List5 = [0, 0]
        self.T = [self.List1, self.List2, self.List3, self.List4, self.List5]
        
        self.actualizar_interfaz_desde_T()
        self.label_resultado.config(text="")
    
    def calcular(self):
        if not self.actualizar_T_desde_interfaz():
            return
        
        puntos_validos = [p for p in self.T if len(p) == 2]
        if len(puntos_validos) < 2:
            messagebox.showerror("Error", "Puntos insuficientes para calcular")
            return
        
        self.par_cercano, self.distancia = encontrar_par_mas_cercano(self.T)
        
        if self.par_cercano:
            p1, p2 = self.par_cercano
            resultado = f"El par mas cercano son los puntos {p1} y {p2} con una distancia de {self.distancia:.6f}"
            self.label_resultado.config(text=resultado)
        else:
            self.label_resultado.config(text="No se encontro ningun par")

def modo_grafico():
    root = tk.Tk()
    app = ParMasCercanoApp(root)
    root.mainloop()

# ========== PROGRAMA PRINCIPAL ==========
if __name__ == "__main__":
    # Preguntar al usuario qué modo prefiere
    print("Seleccione el modo de ejecucion:")
    print("1. Modo grafico (interfaz de ventanas)")
    print("2. Modo consola (sin interfaz grafica)")
    
    opcion = input("Ingrese su opcion (1 o 2): ")
    
    if opcion == "1":
        modo_grafico()
    elif opcion == "2":
        modo_consola()
    else:
        print("Opcion no valida. Ejecutando modo consola por defecto.")
        modo_consola()