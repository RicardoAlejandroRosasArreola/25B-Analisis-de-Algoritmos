def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]


        merge_sort(left_half)
        merge_sort(right_half)


        merge(arr, left_half, right_half)
    return arr


def merge(arr, left_half, right_half):
    i = j = k = 0


    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k+= 1


    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1
   
    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1




def segundo_merge_sort(lista):
    if len(lista) <= 1:
        return lista
    medio = len(lista) // 2
    izquierda = lista[:medio]
    derecha = lista[medio:]
    izquierda = segundo_merge_sort(izquierda)
    derecha = segundo_merge_sort(derecha)
    return segundo_merge(izquierda, derecha)


def segundo_merge(izquierda, derecha):
    resultado = []
    i, j = 0, 0
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] < derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    resultado += izquierda[i:]
    resultado += derecha[j:]
    return resultado






def quick_sort(arr):
    if len(arr) <= 1:
        return arr
   
    pivot = arr[len(arr) //2]


    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]


    return quick_sort(left) + middle + quick_sort(right)




array = [7, 38, 27, 43, 3, 9, 82, 10]
sorted_quick_arr = quick_sort(array)
sorted_merge_arr = merge_sort(array)
sorted_seg_merge_arr = segundo_merge_sort(array)
print(f"Arreglo ordenado con quick: {sorted_quick_arr} \n Arreglo ordenado con primer merge: {sorted_merge_arr} \n Arreglo ordenado con segundo merge: {sorted_seg_merge_arr}")