from dataclasses import dataclass
from Producto import Producto


@dataclass
class ProductoFisico(Producto):
    peso: int = 0

    def costo_envio(self)->float:
        return 1500 + 500*self.peso