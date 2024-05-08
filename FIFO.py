from Page import Page


def fifo(mmu, new_pages, ptr):
    for i in range(new_pages):
        page_waste = 0
        if i == new_pages - 1:
            page_size = ptr.size % mmu.page_size
            page_waste = mmu.page_size - page_size if page_size != 0 else 0
            mmu.waste += page_waste

        if len(mmu.ram_memory) < mmu.total_pages:
            page_number = len(mmu.ram_memory)
            new_page = Page(page_number, page_waste, ptr.index)
            mmu.ram_memory.append(new_page)
            ptr.page_list.append(new_page)
            mmu.time_process += 1
            mmu.count_page_hits += 1
        else:
            mmu.count_page_faults += 1
            mmu.time_process += 5
            fifo_page_fault(mmu, ptr, page_waste)


def fifo_page_fault(mmu, pointer, waste):
    num_page = len(mmu.virtual_memory)
    new_page = Page(num_page, waste , pointer.index)
    evicted_page = mmu.ram_memory.pop(0)
    evicted_page.in_virtual_memory = True
    mmu.virtual_memory.append(evicted_page)
    mmu.ram_memory.append(new_page)
    pointer.page_list.append(new_page)



def use_fifo_page_fault(self, page):
    """Reemplazo basado en el algoritmo FIFO."""
    evicted_page = self.ram_memory.pop(0)  # FIFO
    evicted_page.in_virtual_memory = True
    self.virtual_memory.append(evicted_page)
    page.in_virtual_memory = False
    self.ram_memory.append(page)

