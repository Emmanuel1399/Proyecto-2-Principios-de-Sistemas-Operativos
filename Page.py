class Page:
    size = 4  # capacidad de paginas en KB
    def __init__(self, id,waste,ptr_index):
        self.id = id
        self.ptr_index = ptr_index
        self.waste = waste
        self.in_virtual_memory = False
        self.second_chance = True # mantener la segunda vida activa en principio
        self.last_used = 0  # Para el MRU
        self.time_in_ram = 0
        self.time_in_virtual_memory = 0
