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
        last_page_size = size % self.page_size
        last_page_waste = self.page_size - last_page_size if last_page_size != 0 else 0
        self.waste += last_page_waste


    def cal_ram_used(self):
        for i in range(len(self.map_memory)):
            ptr_list = self.map_memory[i].page_list
            for j in range(len(ptr_list)):
                page = ptr_list[j]
                if page.virtual_memory:
                    self.virtual_used += self.page_size
                else:
                    self.ram_used += self.page_size

    def fifo(self,pid,new_pages):
        new_ptr = Pointer(pid,)
        for i in range(new_pages):
            if len(self.ram_memory) < self.total_pages:
                page_number = len(self.ram_memory)
                new_page = Page()
                if i == num_pages - 1:  # Last page
                    new_page.waste = last_page_waste
                self.ram_memory.append(new_page)
                pages_allocated.append(new_page)
                self.total_waste += new_page.waste
            else:
                # Handle page fault if needed
                self.handle_page_fault(new_page, pages_allocated)


    def handle_page_fault(self, page, pages_allocated):
        evicted_page = self.ram_memory.pop(0)  # FIFO
        evicted_page.in_ram = False
        self.virtual_memory.append(evicted_page)
        self.total_waste -= evicted_page.waste  # Adjust waste when page is evicted
        page.in_ram = True
        self.ram_memory.append(page)
        pages_allocated.append(page)
