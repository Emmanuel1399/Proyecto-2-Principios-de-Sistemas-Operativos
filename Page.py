class Page:
    size = 4  # capacidad de paginas en KB
    def __init__(self, id,waste):
        self.id = id
        self.waste = waste
        self.in_virtual_memory = False

