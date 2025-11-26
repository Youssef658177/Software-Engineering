# -----------------------------------------
# Simple 5-Stage Pipeline CPU Simulator
# IF → ID → EX → MEM → WB
# -----------------------------------------

from collections import deque

# Example instruction format:
# ("ADD", dest, src1, src2)
# ("SUB", dest, src1, src2)
# ("LOAD", dest, address)
# ("STORE", src, address)

# Initial register file
registers = {
    "R0": 0,
    "R1": 5,
    "R2": 10,
    "R3": 15,
    "R4": 20
}

# Simple memory
memory = {100: 50, 200: 99}

# Example program (instruction list)
program = deque([
    ("ADD", "R4", "R1", "R2"),   # R4 = R1 + R2
    ("SUB", "R3", "R4", "R1"),   # R3 = R4 - R1
    ("LOAD", "R1", 100),         # R1 = Mem[100]
    ("STORE", "R2", 200),        # Mem[200] = R2
])

# Pipeline registers each stage
IF = None
ID = None
EX = None
MEM = None
WB = None

cycle = 1

def print_pipeline():
    print(f"\n===== CYCLE {cycle} =====")
    print(f"IF  : {IF}")
    print(f"ID  : {ID}")
    print(f"EX  : {EX}")
    print(f"MEM : {MEM}")
    print(f"WB  : {WB}")

def execute_EX(instruction):
    if instruction is None:
        return None
    
    op = instruction[0]

    if op == "ADD":
        return ("WRITE", instruction[1], registers[instruction[2]] + registers[instruction[3]])
    elif op == "SUB":
        return ("WRITE", instruction[1], registers[instruction[2]] - registers[instruction[3]])
    elif op == "LOAD":
        return ("LOAD", instruction[1], instruction[2])
    elif op == "STORE":
        return ("STORE", instruction[1], instruction[2])

def execute_MEM(result):
    if result is None:
        return None

    op = result[0]

    if op == "LOAD":
        return ("WRITE", result[1], memory[result[2]])
    elif op == "STORE":
        memory[result[2]] = registers[result[1]]
        return None
    else:
        return result

def execute_WB(result):
    if result is None:
        return
    op, reg, value = result
    registers[reg] = value

# -----------------------------------------
# Main Pipeline Loop
# -----------------------------------------

while program or any([IF, ID, EX, MEM, WB]):
    print_pipeline()

    # WB stage
    execute_WB(WB)

    # Shift pipeline backwards
    WB = MEM
    MEM = EX
    EX = execute_EX(ID) if ID else None
    ID = IF

    # IF stage loads next instruction
    IF = program.popleft() if program else None

    # MEM stage processing
    MEM = execute_MEM(MEM)

    cycle += 1

print("\n===== FINAL REGISTER VALUES =====")
for r in registers:
    print(f"{r} = {registers[r]}")

print("\n===== FINAL MEMORY =====")
for addr in memory:
    print(f"Mem[{addr}] = {memory[addr]}")
