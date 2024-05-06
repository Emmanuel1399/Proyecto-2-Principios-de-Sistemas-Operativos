class Page:
    size = 4  # capacidad de paginas en KB
    def __init__(self, id):
        self.id = id
        self.in_virtual_memory = False

