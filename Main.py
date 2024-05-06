from MMU import MMU
import random
import json

def generate_operations(P, N):
    operations = []
    active_pointers = {}
    operations_count = {}

    for _ in range(N):
        op_type = random.choice(['new', 'use', 'delete', 'kill'])
        pid = random.randint(1, P)

        if op_type == 'new' and (pid not in operations_count or operations_count[pid]['kills'] == 0):
            size = random.randint(1, 400)
            ptr_id = len(operations) + 1
            operations.append(('new', pid, size))
            active_pointers[ptr_id] = {'pid': pid, 'alive': True}
            operations_count.setdefault(pid, {'news': 0, 'kills': 0, 'uses': 0, 'deletes': 0})
            operations_count[pid]['news'] += 1

        elif op_type == 'use' and any(ptr['alive'] for ptr in active_pointers.values() if ptr['pid'] == pid):
            if operations_count[pid]['news'] > operations_count[pid]['uses']:
                operations.append(('use', pid))
                operations_count[pid]['uses'] += 1

        elif op_type == 'delete' and any(ptr['alive'] for ptr in active_pointers.values() if ptr['pid'] == pid):
            if operations_count[pid]['news'] > operations_count[pid]['deletes']:
                operations.append(('delete', pid))
                operations_count[pid]['deletes'] += 1
                # Mark the pointer as not alive
                ptr_ids = [ptr_id for ptr_id, ptr in active_pointers.items() if ptr['pid'] == pid and ptr['alive']]
                if ptr_ids:
                    active_pointers[ptr_ids[0]]['alive'] = False

        elif op_type == 'kill' and pid in operations_count and operations_count[pid]['kills'] == 0:
            operations.append(('kill', pid))
            operations_count[pid]['kills'] += 1
            # Mark all pointers of this pid as not alive
            for ptr_id, ptr in active_pointers.items():
                if ptr['pid'] == pid:
                    ptr['alive'] = False

    return operations
def simulate_mmu(operations):
    mmu = MMU('FIFO')
    for op in operations:

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


P = 40  # Número de procesos
N = 1000  # Número de operaciones
operations = generate_operations(P, N)


with open('operations.json', 'w') as f:
    json.dump(operations, f)

simulate_mmu(operations)

opt_mmu = MMU("FIFO")
general_mmu = MMU("OPT")




