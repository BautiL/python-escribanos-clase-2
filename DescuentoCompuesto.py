from dataclasses import dataclass

from Descuento import Descuento

@dataclass
class DescuentoCompuesto(Descuento):
    descuentos: list[Descuento]

    def calcular(self, subtotal:float)->float:
        for d in self.descuentos:
            subtotal = d.calcular(subtotal)
            return subtotal

        return subtotal