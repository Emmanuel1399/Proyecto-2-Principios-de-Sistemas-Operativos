import random

from MMU import MMU


# Función para generar un archivo con instrucciones
# Function to generate a file with instructions
def generate_operations(P, N, output_file='simulated_operations.txt',
                        prob_news=0.49, prob_uses=0.3, prob_deletes=0.20, prob_kills=0.01):
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
            size = random.randint(10, 5000)  # Random size between 10B and 500B
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

def simulate_mmu(operations_list, type_algorithm, ):
    future_reference = build_future_references("simulated_operations.txt")
    mmu = MMU(type_algorithm)
    mmu.set_future_references(future_reference)
    for op in operations_list:
        mmu.calc_ram_used()
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


def build_future_references(filename):
    """
    Build a dictionary of future references for each pointer index based on the instructions from a file.
    """
    future_references = {}
    ptr_page_usage = {}

    # Leer todas las instrucciones del archivo
    with open(filename, 'r') as file:
        instructions = file.readlines()

    # Procesar en orden inverso para identificar próximas referencias
    reversed_instructions = list(reversed(instructions))

    for idx, instruction in enumerate(reversed_instructions):
        # Separar y analizar el tipo de instrucción
        parts = instruction.strip('()\n').split(',')
        command = parts[0]

        # Manejar la instrucción `new` mapeando un puntero a un conjunto de páginas
        if command == 'new':
            pid = int(parts[1])
            ptr_index = len(ptr_page_usage) + 1
            size = int(parts[2])
            num_pages = (size + 4 - 1) // 4

            # Crear una lista de IDs de páginas para el nuevo puntero
            ptr_page_usage[ptr_index] = [ptr_index * 100 + i for i in range(num_pages)]

        # Rastrear el uso de páginas en `use`
        elif command == 'use':
            ptr_index = int(parts[1])
            if ptr_index not in future_references:
                future_references[ptr_index] = []

            if ptr_index in ptr_page_usage:
                # Agregar las páginas asociadas al puntero en orden inverso
                for page in ptr_page_usage[ptr_index]:
                    if page not in future_references[ptr_index]:
                        future_references[ptr_index].insert(0, page)

        # Actualizar el uso de páginas en `delete` o `kill`
        elif command in {'delete', 'kill'}:
            ptr_index = int(parts[1])
            if ptr_index in ptr_page_usage:
                del ptr_page_usage[ptr_index]

    return future_references


P = 50  # Número de procesos
N = 1000  # Número de operaciones
operations = generate_operations(P, N)

#operations = generate_operations(50, 1000, prob_news=0.5, prob_uses=0.3, prob_deletes=0.15, prob_kills=0.05)

simulate_mmu(operations, "OPT")
simulate_mmu(operations, "RND")
