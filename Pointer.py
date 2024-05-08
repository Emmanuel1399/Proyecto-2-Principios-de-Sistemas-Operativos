class Pointer:
    def __init__(self, pid, size, index):
        self.index = index #indice del puntero
        self.page_list = [] #paginas asociadas al puntero
        self.pid = pid # Id del proceso asociado a este puntero
        self.size = size #cantidad de kb de este puntero
        self.kill = False
        self.in_ram = False # puntero que se encuentra en memoria real

    def Kill(self):
        self.page_list = []
        self.kill = True

