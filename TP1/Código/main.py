from queue import Queue_imp
import readline
from route import Route
from antenna import Antenna
from merge_sort import mergesort_antennas
import sys
from aux_funcs import *

def main():
    """ Es condición necesaria que, para obtener una respuesta óptima, la base de datos sea continua. Es decir, que la unión de todas las antenas cubran la totalidad de los kilómetros de la ruta."""
    comandos = sys.argv
    if len(sys.argv) < 3:
        mensaje_ayuda()
        return

    file, kilometers = comandos[1].lower(), float(comandos[2])

    sorted_antennas = mergesort_antennas(parse(file))

    # Si las antenas no llegan a cubrir la totalidad de la ruta
    if sorted_antennas[len(sorted_antennas)-1].t_i < kilometers:
        lanzar_error_terminal("Las opciones de antenas no llegan a cubrir la totalidad de los kilómetros de la ruta.")

    antennas = fill_queue(sorted_antennas)
    route = Route(antennas, kilometers)
    print(antennas_dict_to_string(route.get_optimal_arrange()))

def fill_queue(sorted_antennas):
    queue = Queue_imp()
    for antenna in sorted_antennas:
        queue.put(antenna)
    return queue

main()