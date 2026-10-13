from dataclasses import dataclass

from Producto import Producto


@dataclass
class ProductoDigital(Producto):
    pesoMB: int = 0

    def costo_envio(self) -> int:
        return 0

    def tiene_stock_suficiente(self, cantidad:int)->bool:
        return True