# PROBLEMA ACTUAL: Posible falso positivo en desplazamiento

import random

#Variables globales
FRASE = "En un lugar de la Mancha de cuyo nombre no quiero acordarme no ha mucho tiempo que vivia un hidalgo de los de lanza en astillero adarga antigua rocin flaco y galgo corredor"
PALABRA_GUIA = ""
FRASE_CIFRADA = ""

# FUNCIÓN cifrar() - Generar texto cifrado
def cifrar():
    global PALABRA_GUIA, FRASE_CIFRADA 
    cifrada = []
    # Generar salto_aleatorio (desplazamiento de César)
    salto = random.randint(1, 25)
    fraseMinuscula = FRASE.lower()
    # Seleccionar PALABRA_GUIA con selectGuia()
    PALABRA_GUIA = selectGuia(fraseMinuscula)
    
    # Recorrer cada carácter de la frase original
    for letra in fraseMinuscula:
        char = ord(letra)
        if char != 32:  # Para espacios: copiar tal cual
            # Para letras: aplicar desplazamiento salto_aleatorio
            if char == 241 or char == 209:  # Caso especial para 'ñ'
                char = definirChar(110 + salto)
            else:
                char = definirChar(char + salto)
        cifrada.append(chr(char))  # Añadir carácter a lista cifrada
    
    FRASE_CIFRADA = "".join(cifrada)  # Unir lista en FRASE_CIFRADA

# Seleccionar palabra guía (mínimo 3 letras)
def selectGuia(frase):
    palabra = ""
    while len(palabra) < 3:
        lista_palabras = frase.split()
        palabra = random.choice(lista_palabras)
    return palabra

# Función auxiliar para manejo de caracteres
def definirChar(ascii):
    if ascii >= 123:    # Wrap-around si pasa de 'z'
        return ascii - 122 + 96
    if ascii < 97:      # Wrap-around si es menor que 'a'
        return 122 - (96 - ascii)
    return ascii

# FUNCIÓN descifradoCesar() - Recuperar salto y descifrar
def descifradoCesar():
    # Crear lista wordsWithLen (palabras con misma longitud que PALABRA_GUIA)
    wordsWithLen = []
    for palabra in FRASE_CIFRADA.split():
        if len(palabra) == len(PALABRA_GUIA):
            wordsWithLen.append(palabra)
    
    # Inicializar desplazamiento en None
    desplazamiento = None
    
    # Para cada palabra en wordsWithLen:
    for palabra in wordsWithLen:
        if not palabra or not PALABRA_GUIA:
            continue
        
        # Calcular salto (basado en primera letra)
        salto = ord(palabra[0]) - ord(PALABRA_GUIA[0])
        if salto < 0:
            salto += 26
        
        # Verificar con segunda letra (evitar falsos positivos)
        if len(palabra) > 1:
            prueba = definirChar(ord(palabra[1]) - salto)
            if chr(prueba) != PALABRA_GUIA[1]:
                continue
        
        # Salto encontrado, asignar y salir del loop
        desplazamiento = salto
        break
    
    # descifrar_after_loop
    if desplazamiento is None:
        return ""  # No se encontró desplazamiento
    
    # Si desplazamiento es diferente a None: descifrar texto completo
    diccionario = {}
    for i in range(97, 123):  # Crear diccionario de descifrado
        diccionario[chr(i)] = chr(definirChar(i - desplazamiento))
    
    # Aplicar descifrado a toda la frase
    texto_descifrado = ""
    for letra in FRASE_CIFRADA:
        if letra == " ":  # Respetar espacios
            texto_descifrado += " "
        elif letra in diccionario:
            texto_descifrado += diccionario[letra]
        else:
            texto_descifrado += letra
    
    # Mostrar resultados
    print("\nTexto cifrado:", FRASE_CIFRADA)
    print("Palabra guia:", PALABRA_GUIA)
    print("Desplazamiento encontrado:", desplazamiento)
    print("Texto descifrado:", texto_descifrado, "\n")


# FLUJO PRINCIPAL

# INICIO
cifrar()           # Producir FRASE_CIFRADA y PALABRA_GUIA
descifradoCesar()  # Recuperar salto y descifrar
# FIN