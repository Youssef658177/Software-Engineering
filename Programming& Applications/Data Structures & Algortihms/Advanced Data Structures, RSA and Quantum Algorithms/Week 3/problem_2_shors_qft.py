"""
Problem 2: Shor's Algorithm - QFT and Measurement Analysis (English & Arabic Explanation)
=========================================================================================
1. Problem Statement (English):
-------------------------------
We will now explore the use of QFT to extract the order r. We will skip the construction of the circuit to implement the function f(j) = a^j mod n for fixed a.

(A) Suppose a = 2 and n = 15, and suppose the first measurement in Shor's algorithm yielded f(x) = 8. Write down the superposition for the input qubits after this measurement is performed.

(B) Write a classical function `find_possible_inputs(a, n, m, k)` that outputs a list of all numbers x from 1, ..., 2^m - 1 such that `a^x mod n == k`. The list must be output in ascending order. Example: `find_possible_inputs(5, 21, 4, 4)` should yield `[2, 8, 14, 20]`.

(C) We will run 7-bit QFT on a circuit but force it to be initialized to a special superposition state to verify the measurement outcomes, using the function `implement_seven_qubit_QFT(qc, b)`.

=========================================================================================
2. Explanation (Arabic):
------------------------
**الجزء (أ):** بعد القياس الأول، ينهار المجال الكمي (Superposition). بما أن `f(j) = 2^j mod 15`، والقياس كان `8`، فإن الـ Input Qubits ينهار إلى التراكب التالي: `Σ_{x} |x⟩` حيث `x` تحقق الشرط `2^x mod 15 = 8`. ومن المعروف أن `r = 4`، لذا فإن القيم المحتملة هي `x = 3, 7, 11, 15, ...`. التراكب الناتج هو: `(1/√N) * (|3⟩ + |7⟩ + |11⟩ + |15⟩ + ... )`.

**الجزء (ب):** كتابة دالة كلاسيكية (غير كمية) تبحث في الفضاء من 1 إلى `2^m - 1` وتجمع الأرقام التي تحقق شرط القدرة (الأسي) النمطي `a^x mod n == k`. الكود المرفق يقوم بهذا الحساب بشكل عام باستخدام دالة `pow(a, x, n)`.

**الجزء (ج):** تنفيذ دائرة QFT لـ 7 كيوبت في Qiskit. نقوم بتهيئة الكيوبتات إلى حالة خاصة (superposition) تم إنشاؤها عن طريق حساب قيمة `f(j)`، ونقوم بتطبيق QFT عليها. الهدف هو التأكد أن قياسات الناتج (Measured outputs) تكون قريبة من مضاعفات `2^m / r`. في هذا المثال، `r=12`, `m=7`، لذا القياسات ستتركز حول قيم مثل `64` و `96`.

=========================================================================================
3. Code Implementation:
-----------------------
"""

# ---------- Part (B): find_possible_inputs ----------
def find_possible_inputs(a, n, m, k):
    possible_inputs = []
    # Range is from 1 to 2^m - 1
    max_range = (1 << m) 
    for x in range(1, max_range):
        if pow(a, x, n) == k:
            possible_inputs.append(x)
    return possible_inputs

# ---------- Part (C): Qiskit Circuit for 7-Qubit QFT ----------
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, Aer, transpile
from numpy import pi, sqrt
from qiskit.tools.visualization import plot_histogram

def implement_seven_qubit_QFT(qc, b):
    n = 7  # number of qubits
    # Apply Hadamards and controlled phase rotations
    for i in range(n):
        qc.h(b[i])  # Hadamard on qubit i
        for j in range(i + 1, n):
            # Controlled phase rotation: angle = 2π / (2^(j - i + 1))
            angle = 2 * pi / (2 ** (j - i + 1))
            qc.cp(angle, b[j], b[i])  # control = b[j], target = b[i]
    # Swap qubits to reverse the order (correct bit.endianness)
    for i in range(n // 2):
        qc.swap(b[i], b[n - 1 - i])

# ------------------- Running the Circuit -------------------
if __name__ == "__main__":
    b = QuantumRegister(7, 'b')
    m_out = ClassicalRegister(7, 'm')
    qc = QuantumCircuit(b, m_out)

    # Create the initialization vector based on the given superposition
    lst = [4, 16, 28, 40, 52, 64, 76, 88, 100, 112, 124]
    c = 1.0 / sqrt(len(lst))
    state_vector = [c if i in lst else 0.0 for i in range(128)]
    print('Initial superposition is : ', state_vector)
    qc.initialize(state_vector, b)

    implement_seven_qubit_QFT(qc, b)
    qc.measure(b, m_out)

    # Run simulation
    simulator = Aer.get_backend('aer_simulator')
    circ = transpile(qc, simulator)
    result = simulator.run(circ).result()
    counts = result.get_counts(circ)
    
    display(plot_histogram(counts, title='Result counts (1024 simulations)'))

    # Analyze results (Verifying the condition)
    res_list = [(0, 0)] * 1024
    for (k, v) in counts.items():
        j = int(k, 2)
        res_list[j] = (v / 1024, j)
    res_list.sort(reverse=True)
    
    sum_prob = 0.0
    idx = 0
    print('\nMeasurements obtained 75% of the time:')
    while sum_prob <= 0.75:
        sum_prob += res_list[idx][0]
        meas = res_list[idx][1]
        print(f'\t Measurement {meas} is obtained with probability {res_list[idx][0]}')
        # test that meas * r/2^m is very close to an integer. Here we know r = 12 (secretly) and m = 7 qubits
        print(f'\t\t {meas} * 12/2^7 = {meas * 12 / 2**7}')
        idx += 1

"""
=========================================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Part (B) `find_possible_inputs`:
    - Time Complexity: O(2^m). مطلوب حساب القدرة النمطية (modular exponentiation) لكل رقم في الفضاء الكمي. وهي عملية تستغرق وقتاً أسياً لأنها تفحص فضاء كامل حجمه 2^m، وهذا يوضح لماذا خوارزمية شور تحتاج للكمبيوتر الكمي.
    - Space Complexity: O(2^m) لتخزين القائمة الناتجة في أسوأ الأحوال.

- Part (C) `implement_seven_qubit_QFT`:
    - Time Complexity: O(m^2) من حيث عمق الدائرة الكمومية (لأنها تستخدم 2 حلقات متداخلة `for`، حيث نطبق بوابة `h` و `cp`).
    - Space Complexity: O(m) حيث m هو عدد الكيوبتات (7).
=========================================================================================
"""
