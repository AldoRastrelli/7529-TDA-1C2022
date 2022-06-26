from antenna import *

def lanzar_error_terminal(e):
    print("\nERROR: No existe solución con este conjunto de datos.")
    print("Detalle: " + e + "\n")
    exit()

def mensaje_ayuda():
    print("\n\n>> WARNING: La ejecución requiere ingresar dos argumentos junto con la llamada al programa.\n")
    print("\t - El primer argumento debe ser el nombre del archivo, que debe estar guardado en la misma carpeta que el código. Ejemplo: 'contratos.txt'\n")
    print("\t - El segundo argumento debe ser un número: la cantidad de kilómetros que tiene la ruta. Ejemplo: 450\n")
    print("Ejemplo:\n \tpython3 main.py 'contratos.txt' 450\n")

def antennas_dict_to_string(list):
    string = ""
    for l in list:
        string += str(l.id) + " "
    return string

def parse(file):
    """ Returns a stack of elements of class Antennas. """
    antennas = []

    with open(file) as open_file: 
        
        for antenna in open_file:
            data = antenna.split(",")
            id = int(data[0])
            location = float(data[1])
            radius = float(data[2])
            antennas.append(Antenna(id, location, radius))
    
    return antennas

def get_antenna_with_bigger_range(antenna_1, antenna_2):
    if (antenna_1.radius >= antenna_2.radius):
        return antenna_1
    return antenna_2

def antennas_leave_spaces_inbetween(antenna_1, antenna_2):
    return antenna_1.get_superposition_with(antenna_2) < 0

def previous_is_needed(previous, last_selected, selected_antennas, kms):
    return not (last_selected.t_i >= kms or previous in selected_antennas)