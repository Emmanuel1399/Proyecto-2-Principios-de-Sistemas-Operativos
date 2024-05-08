from Page import Page
import random


def rnd(mmu, new_pages, ptr):
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
            rnd_page_fault(mmu, ptr)




def rnd_page_fault(mmu, ptr):
    evicted_page = random.choice(mmu.ram_memory)
    mmu.ram_memory.remove(evicted_page)
    evicted_page.in_virtual_memory = True
    mmu.virtual_memory.append(evicted_page)

    page_waste = ptr.page_list[-1].waste if ptr.page_list else 0
    new_page = Page(len(mmu.virtual_memory), page_waste, ptr.index)
    mmu.ram_memory.append(new_page)
    ptr.page_list.append(new_page)

