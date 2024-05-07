from MMU import MMU
import random
import json


def generate_operations(P, N, prob_news=0.5, prob_uses=0.30, prob_deletes=0.19, prob_kills=0.01):
    operations_list = []
    active_pointers = {}
    operations_count = {}
    kill_set = set()

    for pid in range(1, P + 1):
        operations_count[pid] = {'news': 0, 'uses': 0, 'deletes': 0, 'kills': 0}

    # Probabilidades ajustadas para cada tipo de operación
    probabilities = [('new', prob_news), ('use', prob_uses), ('delete', prob_deletes), ('kill', prob_kills)]

    while len(operations_list) < N:
        op_type = random.choices(
            [op[0] for op in probabilities],
            [op[1] for op in probabilities],
            k=1
        )[0]
        pid = random.randint(1, P)

        # Operación 'new'
        if op_type == 'new' and pid not in kill_set:
            size = random.randint(1, 400)
            ptr_id = len(operations_list) + 1
            operations_list.append(('new', pid, size))
            active_pointers[ptr_id] = {'pid': pid, 'alive': True}
            operations_count[pid]['news'] += 1

        # Operación 'use'
        elif op_type == 'use' and pid not in kill_set and any(
                ptr['alive'] for ptr in active_pointers.values() if ptr['pid'] == pid):
            if operations_count[pid]['news'] > operations_count[pid]['uses']:
                operations_list.append(('use', pid))
                operations_count[pid]['uses'] += 1

        # Operación 'delete'
        elif op_type == 'delete' and pid not in kill_set and any(
                ptr['alive'] for ptr in active_pointers.values() if ptr['pid'] == pid):
            if operations_count[pid]['news'] > operations_count[pid]['deletes']:
                operations_list.append(('delete', pid))
                operations_count[pid]['deletes'] += 1
                ptr_ids = [ptr_id for ptr_id, ptr in active_pointers.items() if ptr['pid'] == pid and ptr['alive']]
                if ptr_ids:
                    active_pointers[ptr_ids[0]]['alive'] = False

        # Operación 'kill'
        elif op_type == 'kill' and pid not in kill_set:
            operations_list.append(('kill', pid))
            kill_set.add(pid)
            operations_count[pid]['kills'] = 1
            for ptr_id, ptr in active_pointers.items():
                if ptr['pid'] == pid:
                    ptr['alive'] = False

    return operations_list


def simulate_mmu(operations_list, type_algorithm):
    mmu = MMU(type_algorithm)
    for op in operations_list:
        if op[0] == 'new':
            _, pid, size = op
            mmu.new(pid, size)
        elif op[0] == 'use':
            _, pid = op
            mmu.use(pid)
        elif op[0] == 'delete':
            _, pid = op
            mmu.delete(pid)
        elif op[0] == 'kill':
            _, pid = op
            mmu.kill(pid)
    print(mmu.count_page_hits)
    print(mmu.count_page_faults)


def preprocess_references(operations):
    """Genera un mapa de futuras referencias para cada proceso"""
    future_references = {}

    # Procesar cada operación
    for index, op in enumerate(operations):
        if op[0] == 'use':
            pid = op[1]  # Identificador de proceso

            # Inicializar el diccionario si es la primera vez
            if pid not in future_references:
                future_references[pid] = []

            # Añadir el índice de uso para este proceso
            future_references[pid].append(index)
    print(future_references)
    # Almacenar el resultado en el objeto
    return future_references


P = 10  # Número de procesos
N = 500  # Número de operaciones
operations = generate_operations(P, N)


#operations = generate_operations(50, 1000, prob_news=0.5, prob_uses=0.3, prob_deletes=0.15, prob_kills=0.05)

def save_operations_to_file(operations, filename="operations.txt"):
    with open(filename, "w") as file:
        for operation in operations:
            file.write(f"{operation[0]}({', '.join(map(str, operation[1:]))})\n")


future_refs = preprocess_references(operations)
mmu = MMU("OPT")
mmu.set_future_references(future_refs)

save_operations_to_file(operations)
simulate_mmu(operations, "OPT")
simulate_mmu(operations, "RND")
