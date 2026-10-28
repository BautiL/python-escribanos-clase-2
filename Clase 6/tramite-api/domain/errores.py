class TramiteError(Exception):
    """Base de todos los errores del dominio (sirva para araparlos a todos juntos)"""

class TramiteNoEncontrado(TramiteError):
    def __init__(self, tramite_id: int) -> None:
        super().__init__(f"No existe el tramite {tramite_id}")
        self.tramite_id = tramite_id

class TramiteFinalizado(TramiteError):
    def __init__(self, tramite_id: int) -> None: 
        super().__init__(f"El tramite {tramite_id} esta finalizado y no se puede modificar")
        self.tramite_id = tramite_id