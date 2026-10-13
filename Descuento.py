from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Descuento(ABC):

    @abstractmethod
    def calcular(self, subtotal:float)->float:
        pass