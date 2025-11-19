import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter
import heapq

# Nodo del árbol de Huffman
class Nodo:
    def __init__(self, caracter=None, frecuencia=0):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

# Construir tabla de frecuencias
def construir_tabla_frecuencias(texto):
    return Counter(texto)

# Construir árbol de Huffman
def construir_arbol_huffman(tabla_frecuencias):
    monticulo = [Nodo(caracter, freq) for caracter, freq in tabla_frecuencias.items()]
    heapq.heapify(monticulo)

    while len(monticulo) > 1:
        izq = heapq.heappop(monticulo)
        der = heapq.heappop(monticulo)
        combinado = Nodo(frecuencia=izq.frecuencia + der.frecuencia)
        combinado.izquierda = izq
        combinado.derecha = der
        heapq.heappush(monticulo, combinado)

    return monticulo[0]

# Generar códigos binarios
def generar_codigos(nodo, prefijo="", mapa_codigos=None):
    if mapa_codigos is None:
        mapa_codigos = {}
    if nodo.caracter is not None:
        mapa_codigos[nodo.caracter] = prefijo
    else:
        generar_codigos(nodo.izquierda, prefijo + "0", mapa_codigos)
        generar_codigos(nodo.derecha, prefijo + "1", mapa_codigos)
    return mapa_codigos

# Codificar texto
def codificar_texto(texto, mapa_codigos):
    return ''.join(mapa_codigos[caracter] for caracter in texto)

# Decodificar texto
def decodificar_texto(texto_codificado, arbol):
    resultado = []
    nodo = arbol
    for bit in texto_codificado:
        nodo = nodo.izquierda if bit == '0' else nodo.derecha
        if nodo.caracter:
            resultado.append(nodo.caracter)
            nodo = arbol
    return ''.join(resultado)

# Interfaz gráfica
class AplicacionHuffman:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Compresor Huffman")
        self.texto_original = ""
        self.texto_codificado = ""
        self.mapa_codigos = {}
        self.arbol_huffman = None

        tk.Button(ventana, text="📂 Cargar archivo", command=self.cargar_archivo).pack(pady=5)
        tk.Button(ventana, text="🔐 Codificar", command=self.codificar).pack(pady=5)
        tk.Button(ventana, text="🔓 Decodificar", command=self.decodificar).pack(pady=5)
        self.salida = tk.Text(ventana, height=20, width=80)
        self.salida.pack()

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if ruta:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                self.texto_original = archivo.read()
            self.salida.insert(tk.END, f"✅ Archivo cargado: {ruta}\n")

    def codificar(self):
        if not self.texto_original:
            messagebox.showerror("Error", "No se ha cargado ningún archivo.")
            return
        tabla = construir_tabla_frecuencias(self.texto_original)
        self.arbol_huffman = construir_arbol_huffman(tabla)
        self.mapa_codigos = generar_codigos(self.arbol_huffman)
        self.texto_codificado = codificar_texto(self.texto_original, self.mapa_codigos)

        tamaño_original = len(self.texto_original.encode('utf-8')) * 8
        tamaño_codificado = len(self.texto_codificado)
        compresion = 100 - (tamaño_codificado / tamaño_original * 100)

        self.salida.insert(tk.END, f"🔐 Texto codificado.\n")
        self.salida.insert(tk.END, f"Tamaño original: {tamaño_original} bits\n")
        self.salida.insert(tk.END, f"Tamaño codificado: {tamaño_codificado} bits\n")
        self.salida.insert(tk.END, f"Compresión lograda: {compresion:.2f}%\n")

    def decodificar(self):
        if not self.texto_codificado or not self.arbol_huffman:
            messagebox.showerror("Error", "No hay texto codificado.")
            return
        texto_decodificado = decodificar_texto(self.texto_codificado, self.arbol_huffman)
        self.salida.insert(tk.END, f"🔓 Texto decodificado (primeros 500 caracteres):\n{texto_decodificado[:500]}...\n")

# Ejecutar aplicación
if __name__ == "__main__":
    ventana = tk.Tk()
    app = AplicacionHuffman(ventana)
    ventana.mainloop()
