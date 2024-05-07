from Page import Page


def second_chance(mmu, new_pages, ptr):
    for i in range(new_pages):
        page_waste = 0
        if i == new_pages - 1:
            page_size = ptr.size % mmu.page_size
            page_waste = mmu.page_size - page_size if page_size != 0 else 0
            mmu.waste += page_waste
        if len(mmu.ram_memory) < mmu.total_pages:
            new_page = Page(len(mmu.ram_memory), 0, ptr.index)
            new_page.time_in_ram += 1
            mmu.ram_memory.append(new_page)
            ptr.page_list.append(new_page)
            mmu.time_process += 1
            mmu.count_page_hits += 1
        else:
            mmu.count_page_faults += 1
            second_chance_page_fault(mmu)

    mmu.map_memory.append(ptr)


def second_chance_page_fault(mmu):
    i = 0
    while True:
        current_page = mmu.ram_memory[i]
        if not current_page.second_chance:
            evicted_page = mmu.ram_memory.pop(i)
            evicted_page.in_virtual_memory = True
            mmu.virtual_memory.append(evicted_page)
            mmu.time_process += 5
            break
        else:
            current_page.second_chance = False
            i = (i + 1) % len(mmu.ram_memory)
