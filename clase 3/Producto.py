from abc import ABC, abstractmethod
from dataclasses import dataclass

from Descuento import Descuento


@dataclass
class Producto(ABC):
    id: int
    nombre: str
    precio: float
    stock: int
    descuento: Descuento

    def tiene_stock_suficiente(self, cantidad:int)->bool:
        return self.stock >= cantidad

    def descontar(self, cantidad:int):
        self.stock -= cantidad

    def reponer(self, cantidad:int):
        self.stock += cantidad

    @abstractmethod
    def costo_envio(self)->float:
        pass

    def aplicar_descuento(self):
        return self.descuento.calcular(self.precio)