import random
import time
import matplotlib.pyplot as plt

# =============================================
# ALGORITMO 1: CIFRADO CÉSAR TRADICIONAL (FUERZA BRUTA)
# =============================================

def cifrar(palabra):

    #Cifra una palabra usando el cifrado César con desplazamiento aleatorio

    cifrada = []
    salto = random.randint(1, 25)
    palabraMinuscula = palabra.lower()
    
    for letra in palabraMinuscula:
        char = int(ord(letra))
        if (char != 32 ):  # Maneja los espacios (no los cifra)
            if (char == 241 or char == 209 ):  # Maneja las letras 'ñ' y 'Ñ'
                char = definirChar(110 + salto)
            else:
                char = definirChar(char + salto)
        cifrada.append(chr(char))
    
    return "".join(cifrada)

def definirChar(ascii):

    #Ajusta el carácter para que permanezca en el rango de letras minúsculas (a-z)

    if (ascii >= 123): 
        return ascii - 122 + 96
    if (ascii < 97 and ascii != 32):
        return ascii + 26
    return ascii

def cifradoCesar(cifrada):

    #Algoritmo de descifrado por fuerza bruta: prueba TODOS los 25 desplazamientos

    for i in range(1, 26):  # Prueba los 25 desplazamientos posibles
        texto_descifrado = []
        for letra in cifrada:
            char = int(ord(letra))
            if (char != 32 ):  # Los espacios se mantienen
                if (char == 241 or char == 209 ):  # Maneja las 'ñ'
                    char = definirChar(110 - i)
                else:
                    char = definirChar(char - i)
            texto_descifrado.append(chr(char))
        # NO intenta decidir cuál es correcto, solo genera las 25 posibilidades

# =============================================
# ALGORITMO 2: CIFRADO CÉSAR CON DIVIDE Y VENCERÁS
# =============================================

def cifrar_dv(frase_original):

    #Cifra la frase completa usando el método de Divide y Vencerás

    cifrada = []
    salto = random.randint(1, 25)
    fraseMinuscula = frase_original.lower()
    palabra_guia = selectGuia(fraseMinuscula)
    
    for letra in fraseMinuscula:
        char = ord(letra)
        if char != 32:
            if char == 241 or char == 209:
                char = definirChar(110 + salto)
            else:
                char = definirChar(char + salto)
        cifrada.append(chr(char))
    
    frase_cifrada = "".join(cifrada)
    return frase_cifrada, palabra_guia, salto

def selectGuia(frase):

    #Selecciona una palabra guía aleatoria

    lista_palabras = frase.split()
    palabras_validas = [p for p in lista_palabras if len(p) >= 3]
    if palabras_validas:
        return random.choice(palabras_validas)
    else:
        return max(lista_palabras, key=len)

def descifradoCesar(frase_cifrada, palabra_guia):

    #Algoritmo de Divide y Vencerás: Encuentra automáticamente el desplazamiento correcto

    # PASO 1: Buscar palabras candidatas
    wordsWithLen = []
    for palabra in frase_cifrada.split():
        if len(palabra) == len(palabra_guia):
            wordsWithLen.append(palabra)
    
    # PASO 2: Probar desplazamientos en candidatos
    desplazamiento = None
    for palabra in wordsWithLen:
        if not palabra or not palabra_guia:
            continue
        
        salto = ord(palabra[0]) - ord(palabra_guia[0])
        if salto < 0:
            salto += 26
        
        if len(palabra) > 1 and len(palabra_guia) > 1:
            prueba = definirChar(ord(palabra[1]) - salto)
            if chr(prueba) != palabra_guia[1]:
                continue
        
        desplazamiento = salto
        break
    
    # PASO 3: Descifrar con el desplazamiento encontrado
    if desplazamiento is None:
        return None
    
    diccionario = {}
    for i in range(97, 123):
        diccionario[chr(i)] = chr(definirChar(i - desplazamiento))
    
    texto_descifrado = ""
    for letra in frase_cifrada:
        if letra == " ":
            texto_descifrado += " "
        elif letra in diccionario:
            texto_descifrado += diccionario[letra]
        else:
            texto_descifrado += letra
    
    return texto_descifrado

# =============================================
# COMPARACIÓN PURA DE TIEMPOS
# =============================================

def comparar_tiempos():
    #Compara EXCLUSIVAMENTE los tiempos de ejecución de ambos algoritmos
    print("COMPARACIÓN PURA DE TIEMPOS DE EJECUCIÓN")
    print("=" * 55)
    print("Fuerza Bruta: 25 desplazamientos × todos los caracteres")
    print("Divide y Vencerás: Solo desplazamientos probables")
    print("=" * 55)
    
    # Textos progresivamente más largos
    textos_prueba = [
        "En un luga",
        "En un lugar de la Ma", 
        "En un lugar de la Mancha de cu",
        "En un lugar de la Mancha de cuyo nombre ",
        "En un lugar de la Mancha de cuyo nombre no quiero ",
        "En un lugar de la Mancha de cuyo nombre no quiero acordarme no ha mucho tiempo que vivia un hidalgo de los de lanza en astillero adarga antigua rocin flaco y galgo corredor"
    ]
    
    tiempos_fuerza_bruta = []
    tiempos_divide_venceras = []
    longitudes = []
    
    for texto in textos_prueba:
        print(f"\n--- Texto: {len(texto)} caracteres ---")
        
        # Preparar datos para ambos algoritmos
        texto_cifrado_fb = cifrar(texto)
        frase_cifrada_dv, palabra_guia, salto_real = cifrar_dv(texto)
        
        # Medir TIEMPO de FUERZA BRUTA (25 desplazamientos)
        inicio_fb = time.time()
        for _ in range(50):  # 50 repeticiones para mejor precisión
            cifradoCesar(texto_cifrado_fb)  # Ejecuta los 25 desplazamientos
        tiempo_fb = (time.time() - inicio_fb) / 50
        tiempos_fuerza_bruta.append(tiempo_fb)
        
        # Medir TIEMPO de DIVIDE Y VENCERÁS
        inicio_dv = time.time()
        for _ in range(50):  # 50 repeticiones para mejor precisión
            descifradoCesar(frase_cifrada_dv, palabra_guia)  # Encuentra automáticamente
        tiempo_dv = (time.time() - inicio_dv) / 50
        tiempos_divide_venceras.append(tiempo_dv)
        
        longitudes.append(len(texto))
        
        print(f"Fuerza Bruta: {tiempo_fb:.6f} segundos")
        print(f"Divide y Vencerás: {tiempo_dv:.6f} segundos")
    
    # CREAR GRÁFICA DE COMPARACIÓN
    plt.figure(figsize=(12, 7))
    
    # Graficar tiempos
    plt.plot(longitudes, tiempos_fuerza_bruta, 'ro-', label='Fuerza Bruta (25 desplazamientos)', linewidth=3, markersize=8)
    plt.plot(longitudes, tiempos_divide_venceras, 'bo-', label='Divide y Vencerás', linewidth=3, markersize=8)
    
    # Configurar gráfica
    plt.xlabel('Número de Caracteres en el Texto', fontsize=12)
    plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=12)
    plt.title('COMPARACIÓN DE TIEMPOS: Fuerza Bruta vs Divide y Vencerás\n(Mismos caracteres, diferentes estrategias)', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Mostrar valores en la gráfica
    for i, longitud in enumerate(longitudes):
        plt.annotate(f'FB: {tiempos_fuerza_bruta[i]:.6f}s', 
                    (longitud, tiempos_fuerza_bruta[i]), 
                    textcoords="offset points", xytext=(0,15), ha='center', fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="red", alpha=0.1))
        plt.annotate(f'DV: {tiempos_divide_venceras[i]:.6f}s', 
                    (longitud, tiempos_divide_venceras[i]), 
                    textcoords="offset points", xytext=(0,-20), ha='center', fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="blue", alpha=0.1))
    
    plt.tight_layout()
    
    # Mostrar resultados numéricos
    print("\n" + "="*70)
    print("RESUMEN FINAL - COMPARACIÓN DE TIEMPOS")
    print("="*70)
    for i, longitud in enumerate(longitudes):
        print(f"Texto {longitud:3d} chars: FB={tiempos_fuerza_bruta[i]:.6f}s | DV={tiempos_divide_venceras[i]:.6f}s")
    
    # Mostrar gráfica
    print("\nMostrando gráfica de comparación...")
    plt.show()

# =============================================
# EJECUCIÓN PRINCIPAL
# =============================================

if __name__ == "__main__":
    # Configuración de matplotlib
    plt.rcParams['figure.figsize'] = [10, 6]
    plt.rcParams['font.size'] = 10
    
    # Ejecutar la comparación de tiempos
    comparar_tiempos()