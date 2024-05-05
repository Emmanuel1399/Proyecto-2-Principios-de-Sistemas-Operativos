class Page:
    size = 4  # capacidad de paginas en KB
    def __init__(self, identificador):
        self.id = identificador
        self.virtual_memory = False

