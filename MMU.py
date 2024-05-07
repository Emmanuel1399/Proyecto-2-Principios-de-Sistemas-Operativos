from Page import *
from Pointer import *
import random
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
        self.future_references = {}
        self.count_page_faults = 0
        self.counte_page_hits = 0

    def new(self, pid, size):
        num_pages = (size + self.page_size - 1) // self.page_size
        new_ptr = Pointer(pid, size)
        self.map_memory.append(new_ptr)
        if self.algorithm == "FIFO":
            self.fifo(num_pages, new_ptr)
        elif self.algorithm == "SC":
            self.second_chance(num_pages, new_ptr)
        elif self.algorithm == "MRU":
            self.mru(num_pages, new_ptr)
        elif self.algorithm == "RND":
            self.rnd(num_pages, new_ptr)
        elif self.algorithm == "OPT":
            self.opt(num_pages, new_ptr)


    def calc_ram_used(self):
        self.ram_used = 4 * len(self.ram_memory)
        self.virtual_used = 4 * len(self.virtual_memory)

    def fifo(self, new_pages, ptr):
        for i in range(new_pages):
            self.calc_ram_used()
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
                self.time_process += 1
            else:
                # Handle page fault if needed
                self.count_page_faults += 1
                self.fifo_page_fault(ptr, page_waste)
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
            pointer = self.map_memory[ptr]  # Obtener el puntero para el PID dado
            if pointer.kill:
                print("PTR already killed")
                return
            for page in pointer.page_list:  # Revisar cada página en el puntero
                if page.in_virtual_memory:  # Si la página está en memoria virtual
                    self.handle_page_fault(page)  # Manejar el fallo de página
                else:

                    self.time_process += 1

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
                        self.time_process += 5
                    else:
                        # Si la página está en RAM, también removerla
                        self.ram_memory.remove(page)
                        self.time_process += 1

                    self.waste -= page.waste  # Restar el desperdicio asociado a cada página

                # Llamar al método Kill del objeto Pointer
                pointer.Kill()
                # Error al hacer los kills, tengo que arreglar esta parte

    def mru(self, new_pages, ptr):
        for i in range(new_pages):
            page_waste = 0
            if i == new_pages - 1:
                page_size = ptr.size % self.page_size
                page_waste = self.page_size - page_size if page_size != 0 else 0
                self.waste += page_waste

            if len(self.ram_memory) < self.total_pages:
                page_number = len(self.ram_memory)
                new_page = Page(page_number, page_waste)
                new_page.last_used = self.time_process
                self.ram_memory.append(new_page)
                ptr.page_list.append(new_page)
                self.time_process += 1
            else:
                self.mru_page_fault(ptr)
                self.map_memory.append(ptr)

    def mru_page_fault(self, ptr):
        most_recently_used_page = max(self.ram_memory, key=lambda x: x.last_used)
        self.ram_memory.remove(most_recently_used_page)
        most_recently_used_page.in_virtual_memory = True
        self.virtual_memory.append(most_recently_used_page)

        page_waste = ptr.page_list[-1].waste if ptr.page_list else 0
        new_page = Page(len(self.virtual_memory), page_waste)
        new_page.last_used = self.time_process
        self.ram_memory.append(new_page)
        ptr.page_list.append(new_page)
        self.time_process += 5

    # Parte Second Cange

    def second_chance(self, new_pages, ptr):
        for _ in range(new_pages):
            if len(self.ram_memory) < self.total_pages:
                new_page = Page(len(self.ram_memory), 0)
                new_page.time_in_ram += 1
                self.ram_memory.append(new_page)
                ptr.page_list.append(new_page)
            else:
                self.handle_second_chance()

    def handle_second_chance(self):
        i = 0
        page = self.ram_memory[i]
        if not page.second_chance:
            page.second_chance = False
            self.ram_memory.append(self.ram_memory.pop(i))
        else:
            self.ram_memory.pop(i)
            page.in_virtual_memory = True
            page.time_in_virtual_memory += 5
            self.virtual_memory.append(page)

    def rnd(self, new_pages, ptr):
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
                self.time_process += 1
            else:
                self.rnd_page_fault(ptr)
        self.map_memory.append(ptr)

    def rnd_page_fault(self, ptr):
        evicted_page = random.choice(self.ram_memory)
        self.ram_memory.remove(evicted_page)
        evicted_page.in_virtual_memory = True
        self.virtual_memory.append(evicted_page)

        page_waste = ptr.page_list[-1].waste if ptr.page_list else 0
        new_page = Page(len(self.virtual_memory), page_waste)
        self.ram_memory.append(new_page)
        ptr.page_list.append(new_page)
        self.time_process += 5

    def set_future_references(self, references):
        """Preprocesa la secuencia de referencias futuras."""
        for pid, pages in references.items():
            self.future_references[pid] = pages

    def opt(self, new_pages, ptr):
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
                self.time_process += 1
            else:
                self.opt_page_fault(ptr)

    def opt_page_fault(self, ptr):
        longest_future_use = -1
        page_to_remove = None

        for page in self.ram_memory:
            pid = page.id
            if pid not in self.future_references or not self.future_references[pid]:
                longest_future_use = float("inf")
                page_to_remove = page
                break
            next_use = self.future_references[pid].pop(0)

            if next_use > longest_future_use:
                longest_future_use = next_use
                page_to_remove = page

        if page_to_remove:
            self.ram_memory.remove(page_to_remove)
            page_to_remove.in_virtual_memory = True
            self.virtual_memory.append(page_to_remove)

        page_waste = ptr.page_list[-1].waste if ptr.page_list else 0
        new_page = Page(len(self.virtual_memory), page_waste)
        self.ram_memory.append(new_page)
        ptr.page_list.append(new_page)
        self.time_process += 5