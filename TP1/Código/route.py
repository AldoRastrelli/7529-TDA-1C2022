from aux_funcs import *

class Route:

    def __init__(self, antennas, kms):
        """ antennas: Queue_imp, kms: float"""

        self.antennas = antennas
        self.kms = kms
        self.optimal_arrange = self.calculate_optimal_arrange()
    
    def calculate_optimal_arrange(self):

        selected_antennas = {}
        last_selected = self.antennas.get()
        previous = last_selected

        while not self.antennas.is_empty():
            actual = self.antennas.get()

            # Si la antena anterior ya supera la cantidad de kms de la ruta con su cobertura, no es necesario seguir iterando.
            if previous.t_i >= self.kms:
                selected_antennas[previous] = ""
                last_selected = previous
                break

            # Comparación de antenas con igual inicio de cobertura para elegir aquella que tenga más cobertura.
            if last_selected.s_i_is_equal_with(actual):
                last_selected = get_antenna_with_bigger_range(last_selected, actual)
                previous = last_selected
                continue

            # Guarda la última antena elegida como óptima en la lista de selected_antennas
            if selected_antennas.get(last_selected) is None:
                selected_antennas[last_selected] = ""

            # Si la antena actual de la iteración no está dentro de los límites de la ruta
            # o si la última antena analizada llega a cubrir toda la ruta, no es necesario seguir iterando.
            # Las subsiguientes también van a ser innecesarias.
            if not actual.is_inside_relevant_range_of(self.kms) or previous.t_i > self.kms:
                break

            # Si las antenas no tienen superposición, analiza si el conjunto de antenas es contínuo.
            # Si no lo es, lanza un error y termina el programa.
            # Si lo es, significa que las antenas no se superponen y se debe elegir a la anterior.
            if antennas_leave_spaces_inbetween(last_selected, actual):
                if (last_selected.t_i == previous.t_i):
                    lanzar_error_terminal("El conjunto de antenas no es continuo para esta ruta.")
                selected_antennas[previous] = ""
                last_selected = previous
                previous = actual
                continue
            
            # Avanza con el recorrido de antenas
            previous = actual

        # Si al cortar la iteración aún no se terminó de llenar la ruta,
        # termina de llenar la ruta con la última antena analizada.
        if previous_is_needed(previous, last_selected, selected_antennas, self.kms):
            selected_antennas[previous] = ""

        return selected_antennas

    def get_optimal_arrange(self):
        return self.optimal_arrange
