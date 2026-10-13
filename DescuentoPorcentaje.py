from dataclasses import dataclass

from Descuento import Descuento


@dataclass
class DescuentoPorcentaje(Descuento):
    porcentaje: float

    def calcular(self, subtotal:float)->float:
        return subtotal * self.porcentaje