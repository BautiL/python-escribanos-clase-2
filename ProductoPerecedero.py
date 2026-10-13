from dataclasses import dataclass
from datetime import datetime

from ProductoFisico import ProductoFisico


@dataclass
class ProductoPerecedero(ProductoFisico):
    fecha_vencimiento: datetime = datetime.now()

    def costo_envio(self) -> float:
        return super().costo_envio() * 1.2