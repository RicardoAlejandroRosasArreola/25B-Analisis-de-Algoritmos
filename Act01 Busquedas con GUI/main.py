import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class AplicacionBusqueda:
    def __init__(self, master):
        self.master = master
        self.master.title("Comparador de Búsquedas")
        self.master.geometry("900x700")
        
        self.lista_actual = None
        self.tamano_actual = 0
        self.resultados = []
        self.tiempos_lineal = {}
        self.tiempos_binaria = {}
        
        self.canvas = None
        self.fig, self.ax = plt.subplots(figsize=(7, 4))
        
        self.configurar_interfaz()
        
        # Manejo de cierre
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
    
    def configurar_interfaz(self):
        frame_superior = tk.Frame(self.master)
        frame_superior.pack(pady=10)

        tk.Label(frame_superior, text="Tamaño de lista:").grid(row=0, column=0)
        self.entry_tamano = tk.Entry(frame_superior, width=10)
        self.entry_tamano.grid(row=0, column=1)
        self.entry_tamano.insert(0, "1000")
        
        self.btn_generar = tk.Button(frame_superior, text="Generar Datos", command=self.generar_datos)
        self.btn_generar.grid(row=0, column=2, padx=5)
        
        self.btn_ver_lista = tk.Button(frame_superior, text="Ver Lista", command=self.mostrar_lista, state=tk.DISABLED)
        self.btn_ver_lista.grid(row=0, column=3)
        
        tk.Label(frame_superior, text="Valor a buscar:").grid(row=1, column=0)
        self.entry_busqueda = tk.Entry(frame_superior, width=10)
        self.entry_busqueda.grid(row=1, column=1)
        
        self.btn_lineal = tk.Button(frame_superior, text="Búsqueda Lineal", command=lambda: self.buscar("lineal"), state=tk.DISABLED)
        self.btn_lineal.grid(row=1, column=2, padx=5)
        
        self.btn_binaria = tk.Button(frame_superior, text="Búsqueda Binaria", command=lambda: self.buscar("binaria"), state=tk.DISABLED)
        self.btn_binaria.grid(row=1, column=3)

        frame_resultados = tk.Frame(self.master)
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.texto_resultados = scrolledtext.ScrolledText(frame_resultados, height=10)
        self.texto_resultados.pack(fill=tk.BOTH, expand=True)
        self.texto_resultados.config(state=tk.DISABLED)

        self.frame_grafico = tk.Frame(self.master)
        self.frame_grafico.pack(fill=tk.BOTH, expand=True)
        
        self.mostrar_grafico_inicial()
    
    def mostrar_grafico_inicial(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        self.ax.clear()
        self.ax.set_title('Esperando datos...')
        self.ax.set_ylabel('Tiempo (ms)')
        self.ax.set_xlabel('Tamaño de lista')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def generar_datos(self):
        try:
            tamano = int(self.entry_tamano.get())
            if tamano <= 0:
                messagebox.showerror("Error", "El tamaño debe ser positivo")
                return
                
            self.lista_actual = sorted([random.randint(0, tamano*10) for _ in range(tamano)])
            self.tamano_actual = tamano
            
            self.agregar_resultado(f"Lista de {tamano} elementos generada y ordenada")
            
            self.btn_lineal.config(state=tk.NORMAL)
            self.btn_binaria.config(state=tk.NORMAL)
            self.btn_ver_lista.config(state=tk.NORMAL)
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido")
    
    def mostrar_lista(self):
        if not self.lista_actual:
            messagebox.showerror("Error", "No hay datos generados")
            return
            
        ventana_lista = tk.Toplevel(self.master)
        ventana_lista.title(f"Lista generada ({self.tamano_actual} elementos)")
        ventana_lista.geometry("600x400")
        
        texto_lista = scrolledtext.ScrolledText(ventana_lista, width=60, height=20)
        texto_lista.pack(fill=tk.BOTH, expand=True)
        
        if len(self.lista_actual) > 200:
            texto_lista.insert(tk.END, "Primeros 100 elementos:\n")
            texto_lista.insert(tk.END, ", ".join(map(str, self.lista_actual[:100])))
                
            texto_lista.insert(tk.END, "\n\n...\n\nÚltimos 100 elementos:\n")
            texto_lista.insert(tk.END, ", ".join(map(str, self.lista_actual[-100:])))
        else:
            texto_lista.insert(tk.END, ", ".join(map(str, self.lista_actual)))
        
        texto_lista.config(state=tk.DISABLED)
    
    def buscar(self, tipo):
        if not self.lista_actual:
            messagebox.showerror("Error", "Primero genere los datos")
            return
            
        try:
            valor = int(self.entry_busqueda.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido")
            return
            
        tiempos = []
        resultado = None
        
        for _ in range(5):
            inicio = time.perf_counter()
            
            if tipo == "lineal":
                resultado = self.busqueda_lineal(self.lista_actual, valor)
            else:
                resultado = self.busqueda_binaria(self.lista_actual, valor)
                
            fin = time.perf_counter()
            tiempos.append((fin - inicio) * 1000)
            
        tiempo_promedio = sum(tiempos) / len(tiempos)
        
        if tipo == "lineal":
            if self.tamano_actual not in self.tiempos_lineal:
                self.tiempos_lineal[self.tamano_actual] = []
            self.tiempos_lineal[self.tamano_actual].append(tiempo_promedio)
        else:
            if self.tamano_actual not in self.tiempos_binaria:
                self.tiempos_binaria[self.tamano_actual] = []
            self.tiempos_binaria[self.tamano_actual].append(tiempo_promedio)
        
        mensaje = f"Búsqueda {tipo.capitalize()}: "
        mensaje += f"Encontrado en posición {resultado} " if resultado != -1 else "No encontrado "
        mensaje += f"(Tiempo promedio: {tiempo_promedio:.4f} ms)"
        
        self.agregar_resultado(mensaje)
        self.actualizar_grafico()
    
    def busqueda_lineal(self, lista, valor):
        for i in range(len(lista)):
            if lista[i] == valor:
                return i
        return -1
    
    def busqueda_binaria(self, lista, valor):
        izquierda = 0
        derecha = len(lista) - 1
        
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            if lista[medio] < valor:
                izquierda = medio + 1
            elif lista[medio] > valor:
                derecha = medio - 1
            else:
                return medio
        return -1
    
    def agregar_resultado(self, mensaje):
        self.texto_resultados.config(state=tk.NORMAL)
        self.texto_resultados.insert(tk.END, mensaje + "\n")
        self.texto_resultados.see(tk.END)
        self.texto_resultados.config(state=tk.DISABLED)
    
    def actualizar_grafico(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        self.ax.clear()
        
        tamanos = sorted(set(list(self.tiempos_lineal.keys()) + list(self.tiempos_binaria.keys())))
        
        if not tamanos:
            self.mostrar_grafico_inicial()
            return
            

        promedios_lineal = [np.mean(self.tiempos_lineal.get(tam, [0])) for tam in tamanos]
        promedios_binaria = [np.mean(self.tiempos_binaria.get(tam, [0])) for tam in tamanos]
        
        x = np.arange(len(tamanos))
        ancho = 0.35
        
        self.ax.bar(x - ancho/2, promedios_lineal, ancho, label='Lineal')
        self.ax.bar(x + ancho/2, promedios_binaria, ancho, label='Binaria')
        
        self.ax.set_ylabel('Tiempo (ms)')
        self.ax.set_xlabel('Tamaño de lista')
        self.ax.set_title('Comparación de tiempos de búsqueda')
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(tamanos)
        self.ax.legend()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def cerrar_aplicacion(self):
        plt.close('all')
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.master.destroy()

def main():
    root = tk.Tk()
    app = AplicacionBusqueda(root)
    root.mainloop()

if __name__ == "__main__":
    main()