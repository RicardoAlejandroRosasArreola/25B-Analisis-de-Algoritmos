from random import sample
import time
import matplotlib.pyplot as plt

# ==================== DEFINICIÓN DE FUNCIONES ==================== #

def generar_lista(n):
    """Genera una lista de n números aleatorios enteros entre 0 and 9999"""
    return sample(list(range(10000)), n)

def bubblesort(vectorbs):
    """Bubble Sort - Versión original"""
    n = 0
    for _ in vectorbs:
        n += 1
    
    for i in range(n-1):
        for j in range(0, n-i-1):
            if vectorbs[j] > vectorbs[j+1]:
                vectorbs[j], vectorbs[j+1] = vectorbs[j+1], vectorbs[j]
    return vectorbs

def mergesort(vectormerge):
    """Merge Sort - Versión original"""
    
    def merge(vectormerge):
        def largo(vec):
            largovec = 0
            for _ in vec:
                largovec += 1
            return largovec
        
        if largo(vectormerge) > 1:
            medio = largo(vectormerge) // 2
            izq = vectormerge[:medio]
            der = vectormerge[medio:]
            
            merge(izq)
            merge(der)
            
            i = j = k = 0
            
            while i < largo(izq) and j < largo(der):
                if izq[i] < der[j]:
                    vectormerge[k] = izq[i]
                    i += 1
                else:
                    vectormerge[k] = der[j]
                    j += 1
                k += 1
            
            while i < largo(izq):
                vectormerge[k] = izq[i]
                i += 1
                k += 1
            
            while j < largo(der):
                vectormerge[k] = der[j]
                j += 1
                k += 1
    
    merge(vectormerge)
    return vectormerge

def quicksort(vectorquick):
    """Quick Sort - Versión adaptada para un solo argumento"""
    
    def quick(vectorquick, start=0, end=None):
        if end is None:
            end = len(vectorquick) - 1
        if start >= end:
            return
        
        def particion(vectorquick, start, end):
            pivot = vectorquick[start]
            menor = start + 1
            mayor = end

            while True:
                while menor <= mayor and vectorquick[mayor] >= pivot:
                    mayor = mayor - 1
                while menor <= mayor and vectorquick[menor] <= pivot:
                    menor = menor + 1
                if menor <= mayor:
                    vectorquick[menor], vectorquick[mayor] = vectorquick[mayor], vectorquick[menor]
                else:
                    break

            vectorquick[start], vectorquick[mayor] = vectorquick[mayor], vectorquick[start]
            return mayor
        
        p = particion(vectorquick, start, end)
        quick(vectorquick, start, p-1)
        quick(vectorquick, p+1, end)
    
    quick(vectorquick)
    return vectorquick

def medir_tiempo(algoritmo, lista):
    """Mide el tiempo de ejecución de un algoritmo"""
    lista_copia = lista.copy()
    inicio = time.perf_counter()
    algoritmo(lista_copia)
    fin = time.perf_counter()
    return (fin - inicio) * 1000  # Convertir a milisegundos


# ==================== CONFIGURACIÓN DEL EXPERIMENTO ==================== #

tamanos = list(range(50, 1001, 50))  # [50, 100, 150, 200, ..., 1000]
algoritmos = {
    'Bubble Sort': bubblesort,
    'Merge Sort': mergesort,
    'Quick Sort': quicksort
}

resultados = {algo: [] for algo in algoritmos}


# ==================== EJECUCIÓN DE EXPERIMENTOS ==================== #

for tamaño in tamanos:
    lista = generar_lista(tamaño)
    
    for nombre, algoritmo in algoritmos.items():
        tiempos = []
        for _ in range(3):
            tiempo = medir_tiempo(algoritmo, lista)
            tiempos.append(tiempo)
        
        tiempo_promedio = sum(tiempos) / len(tiempos)
        resultados[nombre].append(tiempo_promedio)


# ==================== CREACIÓN DE GRÁFICA Y TABLA ==================== #

fig, (ax, ax_table) = plt.subplots(2, 1, figsize=(14, 10), 
                                  gridspec_kw={'height_ratios': [3, 1]})

# -------------------- SUBCONFIGURACIÓN DE GRÁFICA -------------------- #
colors = {'Bubble Sort': 'red', 'Merge Sort': 'blue', 'Quick Sort': 'green'}
markers = {'Bubble Sort': 'o', 'Merge Sort': 's', 'Quick Sort': '^'}

for nombre in algoritmos.keys():
    ax.plot(tamanos, resultados[nombre], 
             label=nombre, 
             color=colors[nombre],
             marker=markers[nombre],
             linewidth=2.5,
             markersize=6)

ax.set_title('COMPARACIÓN DE ALGORITMOS DE ORDENAMIENTO', 
          fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Tamaño de la Lista (n)', fontsize=12, fontweight='bold')
ax.set_ylabel('Tiempo de Ejecución (ms)', fontsize=12, fontweight='bold')
ax.legend(fontsize=11)

ax.set_xticks(tamanos)
ax.set_xticklabels(tamanos, rotation=45, ha='right')

ax.grid(True, alpha=0.3)
ax.set_axisbelow(True)

max_tiempo = max(max(resultados['Bubble Sort']), 
                 max(resultados['Merge Sort']), 
                 max(resultados['Quick Sort']))
ax.set_ylim(0, max_tiempo * 1.1)

# -------------------- SUBCONFIGURACIÓN DE TABLA -------------------- #
table_tamanos = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
table_data = []

for tamaño in table_tamanos:
    if tamaño in tamanos:
        idx = tamanos.index(tamaño)
        row = [f"{tamaño}"]
        for algo in algoritmos.keys():
            row.append(f"{resultados[algo][idx]:.2f}")
        table_data.append(row)

column_labels = ['Tamaño', 'Bubble Sort', 'Merge Sort', 'Quick Sort']
table = ax_table.table(cellText=table_data, colLabels=column_labels, 
                      loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.8)

for i in range(len(column_labels)):
    table[(0, i)].set_facecolor('#DDDDDD')
    table[(0, i)].set_text_props(weight='bold', size=10)

ax_table.axis('off')

# -------------------- SUBTÍTULO DE TABLA -------------------- #
ax_table.text(0.5, 1.7, 'TIEMPOS PROMEDIO DE EJECUCIÓN (ms)', 
              fontsize=11, fontweight='bold', 
              ha='center', va='center', transform=ax_table.transAxes)


# ==================== VISUALIZACIÓN FINAL ==================== #

plt.tight_layout()
plt.subplots_adjust(bottom=0.10)
plt.show()