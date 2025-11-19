import tkinter as tk
import random
import time

# Parámetros generales
ANCHO = 800
ALTO = 300
VAL_MIN, VAL_MAX = 5, 100
RETARDO_MS = 30

# Algoritmos de ordenamiento
def selection_sort_steps(data, draw_callback):
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            draw_callback(activos=[i, j, min_idx]); yield
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        draw_callback(activos=[i, min_idx]); yield
    draw_callback(activos=[])

def bubble_sort_steps(data, draw_callback):
    n = len(data)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            draw_callback(activos=[j, j+1]); yield
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                swapped = True
                draw_callback(activos=[j, j+1]); yield
        if not swapped:
            break
    draw_callback(activos=[])

def merge_sort_steps(data, draw_callback):
    def merge_sort(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        yield from merge_sort(lo, mid)
        yield from merge_sort(mid, hi)
        left, right = data[lo:mid], data[mid:hi]
        i = j = 0
        for k in range(lo, hi):
            draw_callback(activos=[k]); yield
            if i < len(left) and (j >= len(right) or left[i] <= right[j]):
                data[k] = left[i]; i += 1
            else:
                data[k] = right[j]; j += 1
            draw_callback(activos=[k]); yield
    yield from merge_sort(0, len(data))
    draw_callback(activos=[])

def quick_sort_steps(data, draw_callback):
    def quick_sort(lo, hi):
        if lo < hi:
            p = yield from partition(lo, hi)
            yield from quick_sort(lo, p)
            yield from quick_sort(p + 1, hi)

    def partition(lo, hi):
        pivot = data[hi - 1]
        i = lo
        for j in range(lo, hi - 1):
            draw_callback(activos=[j, hi - 1]); yield
            if data[j] < pivot:
                data[i], data[j] = data[j], data[i]
                draw_callback(activos=[i, j]); yield
                i += 1
        data[i], data[hi - 1] = data[hi - 1], data[i]
        draw_callback(activos=[i, hi - 1]); yield
        return i

    yield from quick_sort(0, len(data))
    draw_callback(activos=[])

# Colores para los resaltados de cada algoritmo
COLORES_RESALTADO = {
    "Selection Sort": "#f28e2b",
    "Bubble Sort": "#e15759",
    "Merge Sort": "#76b7b2",
    "Quick Sort": "#ff9da7"
}

# Clase principal
class Visualizador:
    def __init__(self, ventana):
        self.root = ventana
        self.root.title("Visualizador de Métodos de Ordenamiento")
        
        # Panel para el tiempo (fuera del canvas)
        self.tiempo_frame = tk.Frame(self.root)
        self.tiempo_frame.pack(pady=5)
        
        self.tiempo_label = tk.Label(self.tiempo_frame, text="Tiempo: -", font=("Arial", 12))
        self.tiempo_label.pack()
        
        # Canvas para las barras
        self.canvas = tk.Canvas(self.root, width=ANCHO, height=ALTO, bg="white")
        self.canvas.pack(padx=10, pady=5)

        self.N_BARRAS = 15
        self.datos = []
        self.algoritmos = {
            "Selection Sort": selection_sort_steps,
            "Bubble Sort": bubble_sort_steps,
            "Merge Sort": merge_sort_steps,
            "Quick Sort": quick_sort_steps
        }
        self.alg_seleccionado = tk.StringVar(value="Selection Sort")
        self.retardo_ms = tk.IntVar(value=RETARDO_MS)
        self.generador = None
        self.ordenando = False
        self.after_id = None
        
        # Variable para tiempo aproximado
        self.tiempo_inicio = 0

        self.crear_panel()
        self.generar()

    def crear_panel(self):
        panel_superior = tk.Frame(self.root)
        panel_superior.pack(pady=6)

        panel_inferior = tk.Frame(self.root)
        panel_inferior.pack(pady=6)

        # Panel superior
        tk.Button(panel_superior, text="Generar", command=self.generar).pack(side="left", padx=5)
        tk.Button(panel_superior, text="Mezclar", command=self.mezclar).pack(side="left", padx=5)
        tk.Button(panel_superior, text="Ordenar", command=self.ordenar).pack(side="left", padx=5)
        tk.Button(panel_superior, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)

        # Panel inferior
        tk.Label(panel_inferior, text="Algoritmo:").pack(side="left", padx=5)
        alg_menu = tk.OptionMenu(panel_inferior, self.alg_seleccionado, *self.algoritmos.keys())
        alg_menu.pack(side="left", padx=5)

        tk.Label(panel_inferior, text="N barras:").pack(side="left", padx=5)
        self.entry_n = tk.Entry(panel_inferior, width=5)
        self.entry_n.insert(0, str(self.N_BARRAS))
        self.entry_n.pack(side="left", padx=5)
        tk.Button(panel_inferior, text="Aplicar N", command=self.aplicar_nuevo_n).pack(side="left", padx=5)

        tk.Label(panel_inferior, text="Velocidad:").pack(side="left", padx=5)
        scale_velocidad = tk.Scale(panel_inferior, from_=0, to=200, orient=tk.HORIZONTAL, 
                                  variable=self.retardo_ms, showvalue=True, length=150)
        scale_velocidad.pack(side="left", padx=5)

    def obtener_color_resaltado(self):
        return COLORES_RESALTADO.get(self.alg_seleccionado.get(), "#f28e2b")

    def dibujar_barras(self, activos=None):
        self.canvas.delete("all")
        if not self.datos: return
        n = len(self.datos)
        margen = 10
        ancho_disp = ANCHO - 2 * margen
        alto_disp = ALTO - 2 * margen
        w = ancho_disp / n
        esc = alto_disp / max(self.datos)
        
        color_base = "#4e79a7"
        color_activo = self.obtener_color_resaltado()
        
        for i, v in enumerate(self.datos):
            x0 = margen + i * w
            x1 = x0 + w * 0.9
            h = v * esc
            y0 = ALTO - margen - h
            y1 = ALTO - margen
            color = color_base
            if activos and i in activos:
                color = color_activo
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        
        # Mostrar información adicional en el canvas
        self.canvas.create_text(6, 6, anchor="nw", text=f"n={len(self.datos)}", fill="#666")
        
        # Actualizar tiempo fuera del canvas
        if self.ordenando:
            tiempo_aproximado = time.time() - self.tiempo_inicio
            self.tiempo_label.config(text=f"Tiempo: ~{tiempo_aproximado:.1f}s")

    def generar(self):
        if self.ordenando:
            self.detener_animacion()
        random.seed(time.time())
        self.datos = [random.randint(VAL_MIN, VAL_MAX) for _ in range(self.N_BARRAS)]
        self.limpiar()

    def mezclar(self):
        if self.ordenando:
            self.detener_animacion()
        random.shuffle(self.datos)
        self.limpiar()

    def limpiar(self):
        self.detener_animacion()
        self.dibujar_barras()
        self.tiempo_label.config(text="Tiempo: -")

    def detener_animacion(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.ordenando = False
        self.generador = None

    def aplicar_nuevo_n(self):
        if self.ordenando:
            self.detener_animacion()
        try:
            nuevo_n = int(self.entry_n.get())
            if nuevo_n > 0:
                self.N_BARRAS = nuevo_n
                self.generar()
        except ValueError:
            pass

    def ordenar(self):
        if self.ordenando:
            return
        if not self.datos: 
            return
            
        algoritmo = self.algoritmos.get(self.alg_seleccionado.get())
        if not algoritmo: 
            return
            
        self.ordenando = True
        self.tiempo_inicio = time.time()
        self.tiempo_label.config(text="Tiempo: ~0.0s")
        self.generador = algoritmo(self.datos, lambda activos=None: self.dibujar_barras(activos))
        
        def paso():
            try:
                next(self.generador)
                self.after_id = self.root.after(self.retardo_ms.get(), paso)
            except StopIteration:
                # Mostrar tiempo final aproximado
                tiempo_final = time.time() - self.tiempo_inicio
                self.tiempo_label.config(text=f"Tiempo final: ~{tiempo_final:.1f}s")
                
                self.ordenando = False
                self.generador = None
                self.after_id = None
                
        self.after_id = self.root.after(self.retardo_ms.get(), paso)

# Ejecutar aplicación
if __name__ == "__main__":
    ventana = tk.Tk()
    app = Visualizador(ventana)
    ventana.mainloop()