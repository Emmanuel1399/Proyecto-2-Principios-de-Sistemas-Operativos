class Page:
    size = 4  # capacidad de paginas en KB

    def __init__(self, id, waste, ptr_index):
        self.id = id #ID de la pagina
        self.ptr_index = ptr_index # indice del puntero al que pertenece la pagina
        self.waste = waste # gasto de la pagina
        self.in_virtual_memory = False
        self.second_chance = True  # mantener la segunda vida activa en principio
        self.last_used = 0  # Para el MRU
        self.time_in_ram = 0 # Tiempo en memoria real
        self.time_in_virtual_memory = 0 # tiempo en memoria virtual
