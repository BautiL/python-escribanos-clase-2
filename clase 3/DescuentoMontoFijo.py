from dataclasses import dataclass

from Descuento import Descuento

@dataclass
class DescuentoMontoFijo(Descuento):
    monto: float

    def calcular(self, subtotal:float)->float:
        return subtotal - self.monto