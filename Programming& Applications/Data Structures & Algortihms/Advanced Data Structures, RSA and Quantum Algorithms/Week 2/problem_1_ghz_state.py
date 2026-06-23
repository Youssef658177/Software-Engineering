"""
Problem 1: 3-Qubit GHZ State (English & Arabic Explanation)
============================================================
1. Problem Statement (English):
-------------------------------
This problem set will require you to create simple quantum algorithms and implement them in QISKIT.

Implement a three-bit quantum circuit that starts with the bits initialized in the pure state |000⟩ and yields the following state:
    1/√2 * (|000⟩ + |111⟩)

Design your circuit using IBM's qiskit library. Please do not create/use any ancillary qubits besides the input qubits. Also, please do not use any measurements on your circuit (measurements are done outside in the test harness).

============================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب إنشاء دائرة كمومية (Quantum Circuit) مكونة من 3 كيوبتات (Qubits) تبدأ من الحالة الصافية |000⟩ وتنتج "حالة GHZ" (Greenberger–Horne–Zeilinger state)، وهي حالة متشابكة ثلاثية الأطراف.

الخطوات الفيزيائية لإنشاء الحالة:
1. نطبق بوابة **Hadamard (H)** على الكيوبت رقم 0. هذا يضع الكيوبت الأول في حالة تراكب (Superposition): 1/√2 * (|0⟩ + |1⟩).
2. نطبق بوابة **CNOT (Controlled-NOT)** باستخدام الكيوبت 0 كـ `control` والكيوبت 1 كـ `target`. إذا كان الكيوبت 0 هو |1⟩، فإن الكيوبت 1 ينقلب.
3. نطبق بوابة **CNOT** باستخدام الكيوبت 0 كـ `control` والكيوبت 2 كـ `target`.
النتيجة النهائية: كلما كان الكيوبت 0 هو |1⟩، ينقلب الكيوبت 1 و 2، مما ينتج الحالة المطلوبة: 1/√2 * (|000⟩ + |111⟩).

============================================================
3. Code Implementation:
-----------------------
"""

from qiskit import QuantumCircuit, transpile
from qiskit import Aer
from qiskit.tools.visualization import plot_histogram

def create_ghz_circuit(qc):
    """
    Creates a 3-qubit GHZ state on the given quantum circuit.
    Input: qc (QuantumCircuit object with 3 qubits).
    Result: qc is modified to prepare the state (|000> + |111>)/√2.
    """
    # Step 1: Put qubit 0 in superposition
    qc.h(0)
    
    # Step 2: Entangle qubit 1 with qubit 0
    qc.cx(0, 1)
    
    # Step 3: Entangle qubit 2 with qubit 0
    qc.cx(0, 2)

# ------------------- Main Execution & Tests -------------------
if __name__ == "__main__":
    # Build the circuit
    qc = QuantumCircuit(3)
    create_ghz_circuit(qc)
    qc.measure_all()
    
    # Draw the circuit (optional)
    # qc.draw('mpl', style="iqp")

    # Simulate using Aer simulator
    simulator = Aer.get_backend('aer_simulator')
    circ = transpile(qc, simulator)

    # Run and get counts (1024 shots by default)
    result = simulator.run(circ).result()
    counts = result.get_counts(circ)
    print(f'Result counts from 1024 simulations: {counts}')

    # Verify that only '000' and '111' appear and are roughly equal
    assert counts.get('000', 0) >= 450, 'counts of 000 state are too low'
    assert counts.get('111', 0) >= 450, 'counts of 111 state are too low'
    
    # Ensure no other states appear (noise should be minimal)
    for state in ['001', '011', '010', '100', '101', '110']:
        assert state not in counts, f'Qubit state {state} appeared unexpectedly'

    print("\nTests Passed Successfully!")
    
    # Plot the histogram (optional)
    plot_histogram(counts, title='Result counts (1024 simulations)')

"""
============================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: O(1) (Circuit Depth). 
  The circuit only requires 3 quantum gates (1 Hadamard, 2 CNOTs) regardless of the number of runs. 
  The simulation time depends on the number of shots (1024), which is a constant.
- Space Complexity: O(n) where n is the number of qubits (n=3).
  Qiskit handles the quantum state vector simulation which requires 2^n amplitudes, but this is managed by the Aer simulator backend.
============================================================
"""
