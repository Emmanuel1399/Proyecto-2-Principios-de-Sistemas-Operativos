from Page import Page


import random

# Function to assign pages randomly during a page fault
def rnd_page_fault(mmu, pointer):
    # If there is space in RAM, add directly
    if len(mmu.ram_memory) < mmu.total_pages:
        new_page = Page(id=len(mmu.ram_memory) + 1, waste=0, ptr_index=pointer.index)
        pointer.page_list.append(new_page)
        mmu.ram_memory.append(new_page)
    else:
        # If RAM is full, replace a random page
        random_page = random.choice(mmu.ram_memory)
        mmu.ram_memory.remove(random_page)
        random_page.in_virtual_memory = True
        mmu.virtual_memory.append(random_page)

        # Add new page in RAM
        new_page = Page(id=len(mmu.ram_memory) + 1, waste=0, ptr_index=pointer.index)
        pointer.page_list.append(new_page)
        mmu.ram_memory.append(new_page)

# Function to allocate new pages using the Random page replacement algorithm
def rnd(mmu, num_pages, ptr):
    for i in range(num_pages):
        page_waste = 0
        if i == num_pages - 1:
            page_size = ptr.size % mmu.page_size
            page_waste = mmu.page_size - page_size if page_size != 0 else 0
            mmu.waste += page_waste
        if len(mmu.ram_memory) < mmu.total_pages:
            new_page = Page(len(mmu.ram_memory), page_waste, ptr.index)
            ptr.page_list.append(new_page)
            mmu.ram_memory.append(new_page)
            mmu.count_page_hits += 1
            mmu.time_process += 1
        else:
            # If RAM is full, handle the page fault with rnd_page_fault
            rnd_page_fault(mmu, ptr)
            mmu.count_page_faults += 1
            mmu.time_process += 5

def use_rnd_page_fault(mmu, page):
    """
    Handles a page fault using a Random page replacement algorithm.
    Moves a random page from RAM to virtual memory to make space.
    """
    # If RAM is full, replace a random page
    if len(mmu.ram_memory) >= mmu.total_pages:
        # Choose a random page currently in RAM
        random_page = random.choice(mmu.ram_memory)
        # Move the randomly selected page to virtual memory
        random_page.in_virtual_memory = True
        mmu.virtual_memory.append(random_page)
        mmu.ram_memory.remove(random_page)

    # Move the requested page from virtual memory back to RAM
    page.in_virtual_memory = False
    mmu.ram_memory.append(page)
