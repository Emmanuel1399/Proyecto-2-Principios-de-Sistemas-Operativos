from Page import *
from Pointer import *


class MMU:

    def __init__(self, algorithm):
        self.time_process = 0
        self.ram_memory = []
        self.virtual_memory = []
        self.map_memory = []
        self.page_size = 4
        self.total_pages = 100
        self.waste = 0
        self.ram_used = 0
        self.virtual_used = 0
        self.algorithm = algorithm

    def new(self, pid, size):
        num_pages = (size + self.page_size - 1) // self.page_size
        new_ptr = Pointer(pid, size)

        match self.algorithm:
            case "FIFO":
                self.fifo(num_pages, new_ptr)
            case "SC":
                None
            case "MRU":
                None
            case "RND":
                None
            case "OPT":
                None

    def calc_ram_used(self):
        for i in range(len(self.map_memory)):
            ptr_list = self.map_memory[i].page_list
            for j in range(len(ptr_list)):
                page = ptr_list[j]
                if page.virtual_memory:
                    self.virtual_used += self.page_size
                else:
                    self.ram_used += self.page_size

    def fifo(self, new_pages, ptr):
        for i in range(new_pages):
            page_waste = 0
            if i == new_pages - 1:
                page_size = ptr.size % self.page_size
                page_waste = self.page_size - page_size if page_size != 0 else 0
                self.waste += page_waste

            if len(self.ram_memory) < self.total_pages:
                page_number = len(self.ram_memory)
                new_page = Page(page_number, page_waste)
                self.ram_memory.append(new_page)
                ptr.page_list.append(new_page)
                self.time_process +=1
            else:
                # Handle page fault if needed
                self.fifo_page_fault(ptr,page_waste)
        self.map_memory.append(ptr)

    def handle_page_fault(self, page):
        # Asumiendo que la página necesita ser traída de memoria virtual a RAM:
        self.virtual_memory.remove(page)
        evicted_page = self.ram_memory.pop(0)  # Aplicar FIFO
        evicted_page.in_virtual_memory = True
        self.virtual_memory.append(evicted_page)
        page.in_virtual_memory = False
        self.ram_memory.append(page)
        self.time_process += 5

    def fifo_page_fault(self, pointer, waste):
        num_page = len(self.virtual_memory)
        new_page = Page(num_page, waste)
        evicted_page = self.ram_memory.pop(0)  # FIFO
        evicted_page.in_virtual_memory = True
        self.virtual_memory.append(evicted_page)
        self.ram_memory.append(new_page)
        pointer.page_list.append(new_page)
        self.time_process += 5

    def use(self, ptr):
        if ptr in self.map_memory:
            pointer = self.map_memory[ptr] # Obtener el puntero para el PID dado
            if pointer.kill:
                print("PTR already killed")
                return
            for page in pointer.page_list:  # Revisar cada página en el puntero
                if page.in_virtual_memory:  # Si la página está en memoria virtual
                    self.handle_page_fault(page)  # Manejar el fallo de página

    def delete(self, ptr):
        if ptr in self.map_memory:
            pointer = self.map_memory[ptr]
            waste_removed = pointer.delete()  # Llamada al método delete del objeto Pointer
            self.waste -= waste_removed  # Actualizar el conteo de residuos en MMU

            # Remover páginas de la memoria RAM y memoria virtual
            for page in pointer.page_list:
                if page.in_virtual_memory:
                    self.virtual_memory.remove(page)
                else:
                    self.ram_memory.remove(page)

            del self.map_memory[ptr]  # Eliminar el puntero del mapa de memoria

    def kill(self, pid):
        # Verificar si el pid existe en el mapa de memoria
        for ptr in self.map_memory:
            if ptr.pid == pid:
                pointer = ptr  # Obtener el puntero asociado al pid
                # Eliminar todas las páginas asociadas al puntero tanto en RAM como en memoria virtual
                for page in pointer.page_list:
                    if page.in_virtual_memory:
                        # Si la página está en la memoria virtual, removerla
                        self.virtual_memory.remove(page)
                    else:
                        # Si la página está en RAM, también removerla
                        self.ram_memory.remove(page)
                    self.waste -= page.waste  # Restar el desperdicio asociado a cada página

                # Llamar al método Kill del objeto Pointer, que limpia la lista de páginas y marca el puntero como eliminado
                pointer.Kill()
                #Error al hacer los kills, tengo que arreglar esta parte
