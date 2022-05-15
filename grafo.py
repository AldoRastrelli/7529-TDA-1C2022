from re import A
from site import addusersitepackages
from tkinter import E
from tokenize import PseudoExtras
from arista import *
import time


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

        for n in self.nodos:
            aristas_de_n = self.aristas[n]
            print(n)
            if len(aristas_de_n) == 0:
                print(" -- None -- ")
            for dest in aristas_de_n:
                arista = aristas_de_n[dest]
                arista.print()

        print("\nAristas Residuales:")

        for n in self.nodos:
            aristas_de_n = self.aristas_residuales.get(n)
            print(n)
            if len(aristas_de_n) == 0:
                print(" -- None -- ")
            for dest,arista in aristas_de_n.items():
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