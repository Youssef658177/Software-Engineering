"""
Problem 3: Alice, Bob and Bell's Inequality & Grover's Algorithm (English & Arabic Explanation)
===============================================================================================
1. Problem Statement (English):
-------------------------------
This problem implements the protocol that allows Alice and Bob to beat the classical probability limit in the CHSH game (Bell's Inequality) using quantum entanglement.

- Alice and Bob are given a classical bit b1, q1 (for Alice) and b2, q2 (for Bob).
- The classical bits are fair coin tosses.
- The qubits of Alice/Bob are entangled: |q1, q2> = (|00> + |11>)/√2.
- They win if b1 ∧ b2 = z1 ⊕ z2. The classical limit is 0.75.
- Implement `alice_response` and `bob_response` to beat this limit using a quantum circuit.

Additionally, the problem extends to implementing Grover's Algorithm to search for marked states in a 4-qubit system. We implement the oracle (marking specific pure states) and the diffusion operator (reflection about the uniform state) to amplify the probability of the solutions.

===============================================================================================
2. Explanation (Arabic):
------------------------
هذه المسألة الكمية تتكون من جزأين:

**الجزء الأول: عدم مساواة بيل (CHSH Game):**
تستخدم خوارزمية "التخاطر الكمي" لزيادة فرص الفوز في لعبة تعتمد على القياس الكمي. 
- يتم تشابك كيوبتات أليس وبوب في حالة بيل `(|00⟩ + |11⟩)/√2`.
- كل منهم يحصل على بت عشوائي (`b1` و `b2`)، ويقوم بتطبيق بوابات كمية تعتمد على هذا البت، ثم القياس.
- باستخدام هذا البروتوكول، تصل فرصة الفوز إلى أكثر من 75% (وهو الحد الكلاسيكي)، حيث يصل الـ `success_rate` هنا في الاختبارات إلى حوالي `(cos^2(pi/8))`.

**الجزء الثاني: خوارزمية جروفر (Grover's Algorithm):**
تقوم الخوارزمية بالبحث عن عدة حالات محددة (`|0011⟩`, `|1010⟩`, `|1100⟩`) داخل فضاء من 16 حالة.
- **المُعَلِّم (Oracle):** دالة `mark_pure_states` تقوم بعكس طور (Phase flip) هذه الحالات باستخدام بوابات `mcp` (Multi-Controlled Phase).
- **الانتشار (Diffusion):** دالة `apply_reflection_about_uniform_state` تقوم بتضخيم سعة الاحتمال للحالات المُعلَّمة عن طريق "الانعكاس حول المتوسط".
- بتكرار عملية (Oracle + Diffusion) 4 مرات، تصل احتمالية قياس الحالات الصحيحة إلى أكثر من 50%.

===============================================================================================
3. Code Implementation:
-----------------------
"""

import numpy as np
from numpy import pi
from IPython.display import display

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, transpile, execute
from qiskit.tools.visualization import plot_histogram

# ==================== Part 1: Alice, Bob and Bell's Inequality ====================
def alice_response(qc, b1, qbit, cbit):
    if b1:
        qc.h(qbit)
    qc.measure(qbit, cbit)

def bob_response(qc, b2, qbit, cbit):
    if b2:
        qc.ry(pi/4, qbit)
    else:
        qc.ry(-pi/4, qbit)
    qc.measure(qbit, cbit)

def create_and_run_circuit(b1, b2):
    qbits11 = QuantumRegister(2, 'qbit')
    cbits11 = ClassicalRegister(2, 'z')
    
    print(f'Circuit for b1 = {b1} and b2 = {b2}')
    qc_11 = QuantumCircuit(qbits11, cbits11)
    
    # Create Bell state
    qc_11.h(qbits11[0])
    qc_11.cx(qbits11[0], qbits11[1])
    qc_11.barrier()
    
    alice_response(qc_11, b1, qbits11[0], cbits11[0])
    bob_response(qc_11, b2, qbits11[1], cbits11[1])
    
    display(qc_11.draw('mpl', style='iqp'))
    
    simulator = Aer.get_backend('aer_simulator')
    circ11 = transpile(qc_11, simulator)
    
    # Run and get counts
    result = simulator.run(circ11).result()
    counts = result.get_counts(circ11)
    print(counts)
    return counts 


# ==================== Part 2: Grover's Algorithm ====================
def mark_pure_states(qc, b0, b1, b2, b3):
    # Mark |0011⟩ (index 3)
    qc.x(b2)
    qc.x(b3)
    qc.mcp(pi, [b3, b2, b1], b0)
    qc.x(b2)
    qc.x(b3)

    # Mark |1010⟩ (index 10)
    qc.x(b2)
    qc.x(b0)
    qc.mcp(pi, [b3, b2, b1], b0)
    qc.x(b2)
    qc.x(b0)

    # Mark |1100⟩ (index 12)
    qc.x(b1)
    qc.x(b0)
    qc.mcp(pi, [b3, b2, b1], b0)
    qc.x(b1)
    qc.x(b0)

def Uf(qc, b):
    mark_pure_states(qc, b[0], b[1], b[2], b[3])

def apply_reflection_about_uniform_state(qc, input_registers):
    # 1. Apply Hadamard on each of the input registers.
    # 2. Invert all the qubits
    for i in input_registers:
        qc.h(i)
        qc.x(i)
    n = len(input_registers)
    # 3. apply a multi controlled Z gate on the last qubit
    qc.mcp(np.pi, input_registers[0:n-1], input_registers[n-1])
    for i in input_registers:
        qc.x(i) # invert back
        qc.h(i) # apply Hadamard back

def Grover_diffuse(qc, inputs):
    Uf(qc, inputs)
    apply_reflection_about_uniform_state(qc, inputs)
    qc.barrier()

def create_quantum_circuit_for_grover(n_iters):
    inputs = QuantumRegister(4, 'b')
    cbit = ClassicalRegister(4, 'z')
    qc = QuantumCircuit(inputs, cbit)
    
    # Uniform superposition
    for i in inputs:
        qc.h(i)
    qc.barrier()
    
    # Grover iterations
    for i in range(n_iters):
        Grover_diffuse(qc, inputs)
    
    qc.measure(inputs, cbit)
    return qc


"""
===============================================================================================
4. Time & Space Complexity Analysis:
------------------------------------
1. Bell's Inequality Circuit:
   - Time Complexity: O(1) (Circuit Depth is constant: 1 Hadamard, 1 CNOT, plus local responses).
   - Space Complexity: O(1) (2 qubits and 2 classical bits).

2. Grover's Algorithm Circuit:
   - Time Complexity: O(√N * O(n)) ≈ O(2^(n/2) * n). 
     For 4 qubits (N=16), we need roughly √16 = 4 iterations. Each iteration uses multi-controlled gates which have a depth of O(n) when decomposed.
   - Space Complexity: O(n) (4 qubits and 4 classical bits).
===============================================================================================
"""

# ==================== Test Cases ====================
if __name__ == "__main__":
    print("--- Starting Bell's Inequality Tests ---")
    success_count = 0
    
    counts = create_and_run_circuit(True, True)
    assert '01' in counts, 'Result for b1=True and b2=True must have non-zero amplitude for |01>'
    assert '10' in counts, 'Result for b1=True and b2=True must have non-zero amplitude for |10>'
    success_count += (counts.get('01', 0) + counts.get('10', 0))
    
    counts = create_and_run_circuit(True, False)
    assert '00' in counts, 'Result for b1=True and b2=False must have non-zero amplitude for |00>'
    assert '11' in counts, 'Result for b1=True and b2=False must have non-zero amplitude for |11>'
    success_count += (counts.get('00', 0) + counts.get('11', 0))
    
    counts = create_and_run_circuit(False, True)
    assert '00' in counts, 'Result for b1=False and b2=True must have non-zero amplitude for |00>'
    assert '11' in counts, 'Result for b1=False and b2=True must have non-zero amplitude for |11>'
    success_count += (counts.get('00', 0) + counts.get('11', 0))
    
    counts = create_and_run_circuit(False, False)
    assert '00' in counts, 'Result for b1=False and b2=False must have non-zero amplitude for |00>'
    assert '11' in counts, 'Result for b1=False and b2=False must have non-zero amplitude for |11>'
    success_count += (counts.get('00', 0) + counts.get('11', 0))

    probability = success_count / (4 * 1024)
    print(f'Probability of Alice/Bob Winning is estimated to be: {probability}')
    print("Bell's Inequality Tests Passed!\n")


    print("--- Starting Grover's Algorithm Tests ---")
    # Test 1: State Vector verification for Marking
    b = QuantumRegister(4, 'b')
    qc_test_grover = QuantumCircuit(b)
    qc_test_grover.h(b[0])
    qc_test_grover.h(b[1])
    qc_test_grover.h(b[2])
    qc_test_grover.h(b[3])
    qc_test_grover.barrier()
    mark_pure_states(qc_test_grover, b[0], b[1], b[2], b[3])
    
    backend = Aer.get_backend('statevector_simulator')
    job = execute(qc_test_grover, backend)
    result = job.result()
    state_vector = result.get_statevector()
    
    for i in range(16):
        if i == 3 or i == 10 or i == 12:
            assert abs(state_vector[i] + 0.25) <= 0.001, f"Marking failed on index {i}"
        else:
            assert abs(state_vector[i] - 0.25) <= 0.001, f"Amplitude error at index {i}"
    print("State Vector Marking Test Passed!")

    # Test 2: Grover Simulation (Counts)
    qc2 = create_quantum_circuit_for_grover(4)
    display(qc2.draw('mpl', style='iqp'))
    
    simulator = Aer.get_backend('aer_simulator')
    circ = transpile(qc2, simulator)
    result = simulator.run(circ).result()
    counts = result.get_counts(circ)
    display(plot_histogram(counts, title='Grover Results (1024 simulations)'))
    
    # The marked states should account for more than 50% of the counts.
    marked_counts = counts.get('0011', 0) + counts.get('1010', 0) + counts.get('1100', 0)
    assert marked_counts >= 500, f"The marked states should be > 500 counts. Found {marked_counts}"
    
    print("Grover's Algorithm Tests Passed!")
    print("All Tests Passed Successfully!")
