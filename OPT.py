from Page import Page


def opt(self, new_pages, ptr):
    for i in range(new_pages):
        page_waste = 0
        if i == new_pages - 1:
            page_size = ptr.size % self.page_size
            page_waste = self.page_size - page_size if page_size != 0 else 0
            self.waste += page_waste

        if len(self.ram_memory) < self.total_pages:
            page_number = len(self.ram_memory)
            new_page = Page(page_number, page_waste, ptr.index)
            self.ram_memory.append(new_page)
            ptr.page_list.append(new_page)
            self.count_page_hits += 1
            self.time_process += 1
        else:
            self.count_page_faults += 1
            self.opt_page_fault(ptr)
    self.calc_ram_used()


def opt_page_fault(self, pointer):
    longest_request_ptr = None
    for ptr in self.map_memory:
        if longest_request_ptr is None:
            longest_request_ptr = ptr
        else:
            None