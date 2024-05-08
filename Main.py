import random

from MMU import MMU



# Función para generar un archivo con instrucciones
# Function to generate a file with instructions
def generate_operations(P, N, output_file='simulated_operations.txt',
                        prob_news=0.5, prob_uses=0.3, prob_deletes=0.19, prob_kills=0.01):
    operations_list = []
    active_pointers = {}
    operations_count = {pid: {'news': 0, 'uses': 0, 'deletes': 0, 'kills': 0} for pid in range(1, P + 1)}
    kill_set = set()
    global_ptr = 1

    # Adjusted probabilities for each operation type
    probabilities = [('new', prob_news), ('use', prob_uses), ('delete', prob_deletes), ('kill', prob_kills)]

    while len(operations_list) < N:
        op_type = random.choices(
            [op[0] for op in probabilities],
            [op[1] for op in probabilities],
            k=1
        )[0]
        pid = random.randint(1, P)

        # Operation 'new'
        if op_type == 'new' and pid not in kill_set:
            size = random.randint(10, 600)  # Random size between 100B and 5000B
            operations_list.append(('new', pid, size))
            active_pointers[global_ptr] = {'pid': pid, 'alive': True}
            operations_count[pid]['news'] += 1
            global_ptr += 1

        # Operation 'use'
        elif op_type == 'use' and pid not in kill_set:
            # Get live pointers for this process
            valid_ptrs = [ptr_id for ptr_id, ptr in active_pointers.items() if ptr['pid'] == pid and ptr['alive']]
            if valid_ptrs:
                ptr_id = random.choice(valid_ptrs)
                operations_list.append(('use', ptr_id))
                operations_count[pid]['uses'] += 1

        # Operation 'delete'
        elif op_type == 'delete' and pid not in kill_set:
            valid_ptrs = [ptr_id for ptr_id, ptr in active_pointers.items() if ptr['pid'] == pid and ptr['alive']]
            if valid_ptrs:
                ptr_id = valid_ptrs[0]
                operations_list.append(('delete', ptr_id))
                operations_count[pid]['deletes'] += 1
                active_pointers[ptr_id]['alive'] = False

        # Operation 'kill'
        elif op_type == 'kill' and pid not in kill_set:
            operations_list.append(('kill', pid))
            kill_set.add(pid)
            operations_count[pid]['kills'] = 1
            for ptr_id, ptr in active_pointers.items():
                if ptr['pid'] == pid:
                    ptr['alive'] = False

    # Write the instructions to a file
    with open(output_file, 'w') as file:
        for op in operations_list:
            if op[0] == 'new':
                file.write(f'new({op[1]},{op[2]})\n')
            elif op[0] == 'use':
                file.write(f'use({op[1]})\n')
            elif op[0] == 'delete':
                file.write(f'delete({op[1]})\n')
            elif op[0] == 'kill':
                file.write(f'kill({op[1]})\n')

    return operations_list
# Generar un ejemplo

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



future_refs = preprocess_references(operations)
mmu = MMU("OPT")
mmu.set_future_references(future_refs)

#simulate_mmu(operations, "OPT")
simulate_mmu(operations, "RND")
