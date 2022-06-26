from cmath import inf
ANTERIOR = 0
ULTIMA = 1

def obtener_distancias(grafo, destino):
    nodos = grafo.nodos
    distancia_ant = {}

    for n in nodos:
        if n == destino:
            distancia_ant[n] = 0
        else:
            distancia_ant[n] = inf

    distancia_nueva = {}
    return [distancia_ant, distancia_nueva]

def no_es_ultima_iteración(i,n):
    return i != (n-1)

def costo_aun_no_asignado(costo_vert):
    return costo_vert == inf

def get_diferencias(distancia):
    diferentes = []
    for nodo in distancia[ANTERIOR]:
        if distancia[ANTERIOR][nodo] != distancia[ULTIMA][nodo]:
            diferentes.append(nodo)
    return diferentes

def encontrar_ciclo_en(nodos_cambiados, hash_aristas_min):
    orden = {}
    visitados = []
    nodo = nodos_cambiados[0]
    
    for i in range(len(hash_aristas_min)+1):
        if orden.get(nodo) is None:
            visitados.append(nodo)
            orden[nodo] = i
            nodo = hash_aristas_min[nodo]
            continue
        visitados.append(nodo)
        index = orden[nodo]
        return visitados[index:]
    
    return []

def calcular_costo_para(ciclo_negativo, grafo, arista):
    costo = 0
    primer_nodo = ciclo_negativo[0]
    primero = primer_nodo
    for i in range(1, len(ciclo_negativo)):
        segundo = arista[primero]
        costo += grafo[segundo][primero]
        primero = segundo
    return costo

def esta_vacio(lista):
    return len(lista) == 0

def imprimir_resultado(ciclo_neg, costo):
    if esta_vacio(ciclo_neg):
        print("\nNo existen ciclos negativos en el grafo.\n")
    else:
        print(f"\nExiste al menos un ciclo negativo en el grafo: {imprimir_lista(ciclo_neg)} → costo: {costo}\n")

def imprimir_lista(ciclo):
    return (',').join(ciclo)