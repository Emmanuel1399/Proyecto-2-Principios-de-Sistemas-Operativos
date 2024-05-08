# Function to handle optimal page faults
from Page import Page


def opt_page_fault(mmu, page, pointer):
    """
    Handle a page fault using the Optimal (OPT) page replacement algorithm.
    Replace the page that will not be used for the longest time in the future.
    """
    future_pages = mmu.future_references.get(pointer.index, [])

    # Identificar la página más lejana en el futuro o no utilizada
    farthest_page = None
    max_distance = -1

    for current_page in mmu.ram_memory:
        try:
            next_use = future_pages.index(current_page.id)
        except ValueError:
            # Si la página no está en la lista, reemplazar inmediatamente
            farthest_page = current_page
            break
        else:
            # Actualiza la página que tiene la referencia más lejana
            if next_use > max_distance:
                max_distance = next_use
                farthest_page = current_page

    # Remover la página seleccionada de RAM y moverla a memoria virtual
    farthest_page.in_virtual_memory = True
    mmu.virtual_memory.append(farthest_page)
    mmu.ram_memory.remove(farthest_page)

    # Mover la página solicitada de vuelta a RAM
    page.in_virtual_memory = False
    mmu.ram_memory.append(page)


def opt(mmu, num_pages, ptr):
    """
    Allocate pages using the Optimal (OPT) page replacement algorithm.
    """
    for i in range(num_pages):
        page_waste = 0
        if i == num_pages - 1:
            page_size = ptr.size % mmu.page_size
            page_waste = mmu.page_size - page_size if page_size != 0 else 0
            mmu.waste += page_waste
        new_page = Page(len(mmu.ram_memory), page_waste, ptr.index)
        if len(mmu.ram_memory) < mmu.total_pages:

            ptr.page_list.append(new_page)
            mmu.ram_memory.append(new_page)
            mmu.count_page_hits += 1
            mmu.time_process += 1
        else:
            # Maneja el fallo de página con el algoritmo óptimo
            opt_page_fault(mmu, new_page, ptr)
            mmu.count_page_faults += 1
            mmu.time_process += 5

def use_opt_page_fault(mmu, page):
    """
    Handle a page fault optimally when a 'use(ptr)' instruction is called.
    This will replace the page that will not be used for the longest time, or not at all.
    """
    # Check if there are pages in virtual memory; if not, need to swap out a page from RAM
    if not mmu.virtual_memory:
        # Calculate the next use distance for each page in RAM
        next_use_distances = {}
        for p in mmu.ram_memory:
            next_uses = [i for i, ref in enumerate(mmu.future_references.get(p.ptr_index, [])) if ref == p.id]
            if next_uses:
                next_use_distances[p] = min(next_uses)  # the nearest future use
            else:
                next_use_distances[p] = float('inf')  # no future use found

        # Find the page with the furthest next use or no use at all
        page_to_replace = max(next_use_distances, key=next_use_distances.get)
        mmu.ram_memory.remove(page_to_replace)
        page_to_replace.in_virtual_memory = True
        mmu.virtual_memory.append(page_to_replace)

    # Now bring the requested page into RAM from virtual memory
    mmu.virtual_memory.remove(page)
    page.in_virtual_memory = False
    mmu.ram_memory.append(page)




