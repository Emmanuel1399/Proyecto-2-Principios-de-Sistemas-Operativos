from Pointer import Pointer
from Page import Page
from FIFO import *
from SC import *
from MRU import *
from RND import *

class MMU:
    def __init__(self, algorithm):
        self.ram_memory = []
        self.virtual_memory = []
        self.map_memory = []
        self.page_size = 4
        self.total_pages = 100
        self.waste = 0
        self.ram_used = 0
        self.virtual_used = 0
        self.algorithm = algorithm
        self.time_process = 0
        self.count_process = 0
        self.future_references = {}
        self.count_page_faults = 0
        self.count_page_hits = 0

    def new(self, pid, size):

        num_pages = (size + self.page_size - 1) // self.page_size
        ptr_index = len(self.map_memory) + 1
        new_ptr = Pointer(pid, size, ptr_index)
        self.count_process += 1
        self.map_memory.append(new_ptr)
        self.count_page_faults += num_pages
        if self.algorithm == "FIFO":
            fifo(self, num_pages, new_ptr)
        elif self.algorithm == "SC":
            second_chance(self, num_pages, new_ptr)
        elif self.algorithm == "MRU":
            mru(self, num_pages, new_ptr)
        elif self.algorithm == "RND":
            rnd(self, num_pages, new_ptr)

    def use(self, ptr):
        self.count_process += 1
        pointer = self.map_memory[ptr-1]
        if pointer.kill:
            print("PTR already killed")
            return
        for page in pointer.page_list:
            if page.in_virtual_memory:
                self.handle_page_fault(page, pointer)
                self.count_page_faults += 1
                self.time_process += 5
            else:
                self.count_page_hits += 1
                self.time_process += 1

    def delete(self, ptr):
        self.count_process += 1
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
        self.count_process += 1
        pointer_to_remove = [ptr for ptr in self.map_memory if ptr.pid == pid]
        if pointer_to_remove:
            pointer = pointer_to_remove[0]
            # Eliminar todas las páginas asociadas al puntero
            for page in pointer.page_list:
                if page.in_virtual_memory:
                    self.virtual_memory.remove(page)
                else:
                    self.ram_memory.remove(page)
                self.waste -= page.waste
            # Marcar el puntero como eliminado y quitarlo del mapa
            pointer.Kill()
    def handle_page_fault(self, page, pointer):
        self.count_process += 1
        self.time_process += 5
        if self.algorithm == "FIFO":
            use_fifo_page_fault(self, page)
        elif self.algorithm == "MRU":
            use_mru_page_fault(self, page)
        elif self.algorithm == "SC":
            use_second_chance_page_fault(self, page)
        elif self.algorithm == "RND":
            use_rnd_page_fault(self, page)
    #    elif self.algorithm == "OPT":
          #  opt_page_fault(self, page)

    def calc_ram_used(self):
        self.ram_used = 4 * len(self.ram_memory)
        self.virtual_used = 4 * len(self.virtual_memory)

    def set_future_references(self, references):
        """Preprocesa la secuencia de referencias futuras."""
        for pid, pages in references.items():
            self.future_references[pid] = pages
