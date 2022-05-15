from re import A
from site import addusersitepackages
from tkinter import E
from arista import *
from auxiliares import *
import copy


class Grafo:

    def __init__(self):
        self.aristas = {}
        self.aristas_residuales = {}
        self.nodos = set()

    def guardar_nodo(self, nodo):
        self.nodos.add(nodo)

    def guardar_arista(self, arista):
        origen = arista.origen
        dest = arista.destino
        costo = arista.costo
        capacidad = arista.capacidad_total

        self.guardar_nodo(origen)
        self.guardar_nodo(dest)

        if self.aristas.get(origen) is None:
            self.aristas[origen] = {dest: arista}
        else:
            self.aristas[origen][dest] = arista

        arista_res = Arista(dest, origen, -costo, capacidad)
        self.guardar_arista_residual(arista_res)

    def guardar_arista_residual(self, arista_res):
        origen = arista_res.origen
        dest = arista_res.destino
        arista_res.capacidad_ocupada = arista_res.capacidad_total

        if self.aristas_residuales.get(origen) is None:
            self.aristas_residuales[origen] = {dest: arista_res}
        else:
            self.aristas_residuales[origen][dest] = arista_res
        
        arista = self.aristas_residuales[origen][dest]

    def print(self):
        print(f"Nodos: {list(self.nodos)}\n")

        for nodo, aristas in self.aristas.items():
            print(nodo)
            if len(aristas) == 0:
                print(" -- None -- ")
            for dest, arista in aristas.items():
                arista.print()

        print("\nAristas Residuales:")

        for nodo, aristas in self.aristas.items():
            print(nodo)
            if len(aristas) == 0:
                print(" -- None -- ")
            for dest, arista in aristas.items():
                arista.print()

    def busqueda_BFS(self, s, t, padre):

        visitado = {}
        # inicializamos a todos los nodos en False
        for n in self.nodos:
            visitado[n] = False

        cola = []
        
        cola.append(s)
        visitado[s] = True

        while cola:

            v = cola.pop(0)
            for dest,arista in self.aristas[v].items():
                if visitado[dest] == False and not arista.tiene_capacidad_completa():
                    cola.append(dest)
                    visitado[dest] = True
                    padre[dest] = v

                    if dest == t:
                        return True

        return False

    def ford_fulkerson(self, source, target):
        padre = {}
        # inicializamos a todos los nodos en None
        for n in self.nodos:
            padre[n] = None

        flujo_max = 0

        while self.busqueda_BFS(source, target, padre):
            min_flujo_en_camino = float("Inf")
            s = target
            while (s != source):
                arista = self.aristas[padre[s]][s]
                min_flujo_en_camino = min(min_flujo_en_camino,
                                          arista.get_capacidad_disponible())
                s = padre[s]

            flujo_max += min_flujo_en_camino

            # Actualización de las capacidades residuales de las aristas y las aristas inversas a lo largo del camino
            v = target
            while (v != source):
                
                u = padre[v]
                arista = self.aristas[u][v]
                arista_residual = self.aristas_residuales[v][u]

                arista.usar_capacidad(min_flujo_en_camino)
                arista_residual.liberar_capacidad(min_flujo_en_camino)
                v = padre[v]

        return flujo_max

    def get_grafo_residual(self):
        grafo_nuevo = Grafo()
        grafo_nuevo.nodos = self.nodos

        for origen, aristas_nodo in self.aristas.items():
            for destino, arista in aristas_nodo.items():
                print(f"{origen} -> {destino}")
                self.aristas[origen][destino].print()
                self.aristas_residuales[destino][origen].print()
                if arista.tiene_capacidad_disponible():
                    print("tiene capacidad disponible-> guardar arista")
                    grafo_nuevo.guardar_arista(self.aristas[origen][destino])
                    #grafo_nuevo.aristas[origen][destino].print()
                if self.aristas_residuales[destino][origen].tiene_capacidad_disponible():
                    print("tiene capacidad_disponible -> guardar arista residual")
                    grafo_nuevo.guardar_arista(self.aristas_residuales[destino][origen])

        return grafo_nuevo

    def encontrar_ciclos_negativos(self, destino):
        cant_nodos = len(self.nodos)
        hash_aristas_min = {}
        distancias = obtener_distancias(self,destino)

        for i in range(cant_nodos):
            if no_es_ultima_iteración(i,cant_nodos):
                iteracion = ANTERIOR
            else:
                iteracion = ULTIMA
                distancias[iteracion] = copy.copy(distancias[ANTERIOR])

            for v in self.nodos:
                costo_vert = distancias[iteracion][v]
                if costo_aun_no_asignado(costo_vert):
                    continue

                for arista in self.aristas[v]:
                    peso = self.aristas[v][arista].costo
                    costo_min_anterior = distancias[iteracion][arista]
                    costo_nuevo = costo_vert + peso

                    if costo_min_anterior > costo_nuevo:
                        distancias[iteracion][arista] = costo_nuevo
                        hash_aristas_min[arista] = v

        nodos_cambiados = get_diferencias(distancias)
        if esta_vacio(nodos_cambiados):
            return [], None
        ciclo_negativo = encontrar_ciclo_en(nodos_cambiados, hash_aristas_min)

        costo = calcular_costo_para(ciclo_negativo, self.aristas, hash_aristas_min)
        ciclo_negativo.reverse()
        return ciclo_negativo, costo