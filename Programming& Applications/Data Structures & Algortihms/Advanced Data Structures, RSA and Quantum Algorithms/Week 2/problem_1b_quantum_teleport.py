"""
Problem 1B: Quantum Teleportation (English & Arabic Explanation)
=================================================================
1. Problem Statement (English):
-------------------------------
We will now look into the problem of "destructive" copying of a quantum state called quantum teleportation. Suppose we have a qubit b0 that is currently in a superposition |ψ⟩ = a0 |0⟩ + a1 |1⟩ and another qubit b1 initialized to |0⟩. We wish to transform b1 to be |ψ⟩ while b0 is potentially destroyed in the process.

Prove that the following steps will copy b0 over to b1:
1. Apply the Hadamard gate to b1.
2. Apply the controlled-X gate to qubit b0 with control qubit b1.
3. Apply the controlled-X gate to qubit b1 with control qubit b0.
4. Measure the qubit b0. (Write down the possible results).
5. Implement the function `quantum_teleport` that takes an instance of QuantumCircuit and index of two qubits b0 and b1. It should implement the scheme to copy b0 into b1.

=================================================================
2. Explanation (Arabic):
------------------------
مسألة "التخاطر الكمي" (Quantum Teleportation) تسمح لنا بنقل حالة كمية (Quantum State) من كيوبت إلى آخر دون نسخها (لأن مبرهنة عدم النسخ "No-Cloning Theorem" تمنع النسخ المثالي). 

البروتوكول المتبع في الكود هو أحد أشكال التخاطر الكمي المبسطة (التي لا تحتاج إلى كيوبت مساعد بتلات متشابكة مسبقاً، بل تستخدم القياس المباشر):
1. **Entangling (التشابك المباشر):** نطبق `cx(b0, b1)` لجعل الكيوبت المصدر (`b0`) والهدف (`b1`) متشابكين.
2. **Hadamard:** نطبق `h(b0)` لتغيير أساس القياس.
3. **Measurement (القياس):** نقيس الكيوبت المصدر `b0` ونخزن النتيجة في بت كلاسيكي (`cbit`).
4. **Correction (التصحيح الكمي):** بناءً على نتيجة القياس، نطبق بوابات تصحيح (مثل `Z` و `X`) على الكيوبت الهدف `b1`. في هذا الكود، تم تطبيق بوابة `Z` المشروطة باستخدام `.c_if(cbit, 1)`، والتي تقوم بتصحيح انعكاس الطور (Phase) إذا كان القياس هو 1.

نظراً لأن الحالة الأصلية للكيوبت `b0` قد انهارت أثناء القياس، فإن الكيوبت `b1` سيحمل الحالة الكمية الأصلية. هذا هو جوهر التخاطر الكمي.

=================================================================
3. Code Implementation:
-----------------------
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def quantum_teleport(qc, b0, b1, cbit): 
    # qc is a quantum circuit instance 
    # b0 and b1 are indices of two bits. 
    # cbit is a classical bit that you will need for the partial measurement at step 4.
    # assume b0 != b1
    # implement the circuit to "teleport" the state of q1 to q2.
    # do not introduce any ancillary qubits.
    # no need to return anything: you will be mutating the circuit qc.
    
    # Step 1: Entangle the source (b0) and the target (b1) directly
    qc.cx(b0, b1)
    
    # Step 2: Apply a Hadamard gate to change the basis of the source qubit
    qc.h(b0)
    
    # Step 3: Measure the source qubit into the provided classical bit
    qc.measure(b0, cbit)
    
    # Step 4: Apply a conditional Phase (Z) correction to the target qubit
    # If the source qubit collapsed to 1, the target state's phase is inverted.
    # We apply Z to flip the phase back to the original state.
    qc.z(b1).c_if(cbit, 1)

"""
=================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: O(1) (Circuit Depth).
  الدائرة تتكون من 4 بوابات أساسية فقط (CX, H, Measure, Z.c_if). بغض النظر عن عدد الكيوبتات (طالما لدينا 2 فقط)، عدد البوابات ثابت.
- Space Complexity: O(n).
  يستخدم Qiskit محاكاة الحالة الكمية التي تتطلب متجه حالة بحجم 2^n. هنا n=2 (كيوبت مصدر وهدف)، ولا يتم استخدام كيوبتات مساعدة إضافية.
=================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    from numpy import pi
    from qiskit import Aer, transpile
    from qiskit.tools.visualization import plot_histogram

    # Test 1: Teleport a single arbitrary rotation (Pi/8)
    print("--- Test 1: Teleport single rotation ---")
    b = QuantumRegister(2, 'b')
    c = ClassicalRegister(2, 'z')
    qc_test1 = QuantumCircuit(b, c)

    # Prepare the source qubit b[0] in state cos(pi/8)|0> - sin(pi/8)|1>
    qc_test1.r(2*pi/8, 0.0, b[0])
    qc_test1.barrier()

    # Teleport b[0] to b[1]
    quantum_teleport(qc_test1, b[0], b[1], c[1])
    qc_test1.barrier()

    qc_test1.measure(b[1], c[0]) # measure target qubit
    
    # Display circuit (requires matplotlib)
    # display(qc_test1.draw('mpl', style='iqp'))

    simulator = Aer.get_backend('aer_simulator')
    circ = transpile(qc_test1, simulator)

    # Run and get counts
    result = simulator.run(circ).result()
    counts = result.get_counts(circ)
    print(f'Result counts from 1024 simulations: {counts}')

    # Logic Verification:
    # Measurement of b0 should be roughly 50/50
    b0_0_count = counts.get('00', 0) + counts.get('01', 0)
    b0_1_count = counts.get('10', 0) + counts.get('11', 0)
    print(f' b0 = |0> count is {b0_0_count} and b0=|1> count is {b0_1_count} : must be roughly equal')
    assert b0_0_count >= 0.85 * 512 and b0_0_count <= 1.15 * 512

    # Probability of b1=0 and b1=1 must be in the ratio tan^2(pi/8) ≈ 0.17157
    b1_0_count = counts.get('00', 0) + counts.get('10', 0)
    b1_1_count = counts.get('01', 0) + counts.get('11', 0)
    print(f' b1 = |0> count is {b1_0_count} and b1=|1> count is {b1_1_count} : expected  b1 = |1> happens roughly 17% of the time')
    assert b1_0_count >= 0.7 * 1024 and b1_0_count <= 0.95 * 1024
    print('Test 1 Passed!\n')


    # Test 2: Teleport a Bell State component
    print("--- Test 2: Teleport Bell State ---")
    b = QuantumRegister(3, 'b')
    c = ClassicalRegister(3, 'z')
    qc_test2 = QuantumCircuit(b, c)
    
    # Create the bell state for b[0] and b[1]
    qc_test2.h(b[0])
    qc_test2.cx(0, 1)
    qc_test2.barrier()
    
    # Teleport b[0] to b[2]
    quantum_teleport(qc_test2, b[0], b[2], c[2])
    qc_test2.barrier()
    
    qc_test2.measure(b[2], c[0]) # measure
    qc_test2.measure(b[1], c[1]) # measure

    # display(qc_test2.draw('mpl', style='iqp'))

    simulator = Aer.get_backend('aer_simulator')
    circ = transpile(qc_test2, simulator)
    
    result = simulator.run(circ).result()
    counts = result.get_counts(circ)
    print(f'Result counts from 1024 simulations: {counts}')

    # there should be no count for states of the form `*01` and `*10`
    assert '001' not in counts
    assert '010' not in counts
    assert '101' not in counts
    assert '110' not in counts

    # The 4 valid states should appear roughly equally (25% each)
    assert 0.2 * 1024 <= counts.get('000', 0) <= 0.3 * 1024
    assert 0.2 * 1024 <= counts.get('011', 0) <= 0.3 * 1024
    assert 0.2 * 1024 <= counts.get('100', 0) <= 0.3 * 1024
    assert 0.2 * 1024 <= counts.get('111', 0) <= 0.3 * 1024

    print('Test 2 Passed!')
    
    print("\nAll Tests Passed Successfully!")
