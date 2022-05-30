from grafo import *
import sys

def main():

    comandos = sys.argv

    if len(comandos) != 2:
        return

    archivo = comandos[1].lower()

    grafo, origen, destino  = obtener_grafo_origen_destino_de(archivo)
    flujo_max = grafo.ford_fulkerson(origen,destino)

    grafo_residual = grafo.get_grafo_residual()
    ciclo_neg, _ = grafo_residual.encontrar_ciclos_negativos(destino)

    while not esta_vacio(ciclo_neg):
        valor_min_arista = calcular_min_arista(ciclo_neg, grafo_residual)
        grafo.actualizar_flujo_en_ciclo(ciclo_neg, valor_min_arista)

        grafo_residual = grafo.get_grafo_residual()
        ciclo_neg, _ = grafo_residual.encontrar_ciclos_negativos(destino)
    
    costo_min = grafo.min_cost()

    print(f"\n>> Costo Mínimo de Viajes: ${costo_min}, Capacidad Máxima de Personas: {flujo_max}\n")

def obtener_grafo_origen_destino_de(archivo):

    lineas = [] 
    grafo = Grafo()
       
    with open(archivo) as aristas:
        lineas = aristas.readlines()
        source = lineas.pop(0).strip()
        target = lineas.pop(0).strip()

        for linea in lineas:
            try:
                origen, dest, costo, capacidad = linea.strip().split(",")
                arista = Arista(origen, dest, int(costo), int(capacidad))

                grafo.guardar_arista(arista)

            except (TypeError, ValueError):
                pass
        
    for n in grafo.nodos:
        if grafo.aristas.get(n) is None:
            grafo.aristas[n] = {}
        if grafo.aristas_residuales.get(n) is None:
            grafo.aristas_residuales[n] = {}

    return grafo, source, target

main()