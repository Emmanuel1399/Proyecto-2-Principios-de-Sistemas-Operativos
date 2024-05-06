from Page import *
from Pointer import *
class MMU:

    def __init__(self,algorithm):
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
                self.fifo(num_pages,new_ptr)
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

    def fifo(self,new_pages,ptr):
        for i in range(new_pages):
            if len(self.ram_memory) < self.total_pages:
                page_number = len(self.ram_memory)
                page_size = ptr.size % self.page_size
                page_waste = self.page_size - page_size if page_size != 0 else 0
                self.waste += page_waste
                new_page = Page(page_number,page_waste)
                self.ram_memory.append(new_page)
                ptr.page_list.append(new_page)
            else:
                # Handle page fault if needed
                self.fifo_page_fault(ptr)

    def fifo_page_fault(self,pointer):
        new_page = len(self.virtual_memory)
        evicted_page = self.ram_memory.pop(0)  # FIFO
        evicted_page.in_ram = False
        self.virtual_memory.append(evicted_page)
        self.ram_memory.append(new_page)
        pointer.append(new_page)
