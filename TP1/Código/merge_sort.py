def mergesort_antennas(lista):
    if len(lista) < 2:
        return lista
    medio = len(lista) // 2
    izq = mergesort_antennas(lista[:medio])
    der = mergesort_antennas(lista[medio:])
    return _merge_antennas(izq, der)
 
def _merge_antennas(lista1, lista2):
    i, j = 0, 0  
    resultado = []
    while(i < len(lista1) and j < len(lista2)):
        if (lista1[i].s_i <= lista2[j].s_i):
            resultado.append(lista1[i])
            i += 1
        else:
            resultado.append(lista2[j])
            j += 1
    # Agregar lo que falta
    resultado += lista1[i:]
    resultado += lista2[j:]
    return resultado