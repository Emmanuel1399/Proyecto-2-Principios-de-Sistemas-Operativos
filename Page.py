class Page:
    size = 4  # capacidad de paginas en KB
    def __init__(self, id,waste):
        self.id = id
        self.waste = waste
        self.in_virtual_memory = False
        self.second_change = True # mantener la segunda vida activa en principio
        self.last_used = 0  # Para el MRU
        self.time_in_ram = 0
