
class Arista:

    def __init__(self, origen, destino, costo = 0, capacidad = 0 ):
        self.origen = origen
        self.destino = destino
        self.costo = costo
        self.capacidad_total = capacidad
        self.capacidad_ocupada = 0

    def print(self):
        print(f"arista: {self.origen}->{self.destino} | costo: {self.costo} | capacidad: {self.capacidad_ocupada}/{self.capacidad_total}")

    def usar_capacidad(self, adicional):
        if adicional < 0:
            return
        self.capacidad_ocupada += adicional
        resto = self.capacidad_ocupada - self.capacidad_total
        
        if resto > 0:
            self.capacidad_ocupada -= resto
        
        return resto

    def liberar_capacidad(self, liberado):
        if liberado < 0 or (self.capacidad_ocupada - liberado) < 0:
            return
        self.capacidad_ocupada -= liberado

    def tiene_capacidad_completa(self):
        return self.capacidad_ocupada == self.capacidad_total

    def tiene_capacidad_disponible(self):
        return self.capacidad_total > self.capacidad_ocupada

    def get_capacidad_disponible(self):
        return self.capacidad_total - self.capacidad_ocupada