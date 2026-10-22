from domain.home import Home


class HomeService:
    def get_texto_home(self, casa:Home):
        return {"mensaje":casa.hola()}