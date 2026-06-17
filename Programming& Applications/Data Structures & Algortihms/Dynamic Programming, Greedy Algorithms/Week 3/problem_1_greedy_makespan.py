"""
Problem 1: Greedy Makespan Minimization (English & Arabic Explanation)
=======================================================================
1. Problem Statement (English):
-------------------------------
The idea is simple: we go through each job and assign it to the processor that currently has the least load.

Given an array T of n numbers (job times) and m processors, we implement a greedy algorithm:
1. Initialize assignment A to nil.
2. Initialize the current load of each processor M to 0.
3. For i = 1 to n (or 0 to n-1):
   a. Find processor j for which M[j] is the least.
   b. Assign job i to processor j: A[i] = j.
   c. Update load: M[j] = M[j] + T[i].
4. The makespan is max(M[0], ..., M[m-1]).

Question 4: What is the running time of the greedy makespan algorithm? What data structure would you use to achieve a running time of n log(m)?

=======================================================================
2. Explanation (Arabic):
------------------------
المسألة بتطبق خوارزمية "جشعة" (Greedy) لتوزيع المهام على المعالجات بأقل وقت إنجاز (Makespan).
فكرة الخوارزمية بسيطة جداً:
- بنمر على كل مهمة بالترتيب.
- في كل خطوة، بنختار المعالج اللي عنده "أقل حمل حالياً" ونحط المهمة عليه.
- بعد التوزيع، الـ Makespan هو أقصى حمل ممكن يوصله أي معالج.

**إجابة Question 4:**
- التعقيد الزمني للخوارزمية هو `O(n log m)`.
- هيكل البيانات اللي لازم نستخدمه عشان نوصل للتعقيد ده هو **Min-Heap** (الكومة الدنيا). الكومة الدنيا بتخلينا نقدر نستخرج (pop) المعالج الأقل حملاً في وقت `O(log m)`، وبعدين نحدث حمله ونرجعه للكومة (push) في وقت `O(log m)` تاني. وبما إننا بنعمل ده لـ `n` مهمة، الوقت الكلي بيبقى `O(n log m)`.
- في الكود المرفق، تم استخدام مكتبة `heapq` في بايثون لتنفيذ الكومة الدنيا (Min-Heap).

=======================================================================
3. Code Implementation:
-----------------------
"""

import heapq

def greedy_makespan_min(times, m):
    # times is a list of n jobs.
    assert len(times) >= 1
    assert all(elt >= 0 for elt in times)
    assert m >= 2
    n = len(times)
    
    # Initialize a min-heap to keep track of (current_load, machine_id)
    # This helps us quickly find the machine with the smallest load
    heap = [(0, i) for i in range(m)]
    heapq.heapify(heap)
    
    assignments = [0] * n
    
    # Iterate through jobs in the given order
    for i, job_time in enumerate(times):
        # Pop the machine with the smallest current load (O(log m))
        load, machine_id = heapq.heappop(heap)
        
        # Assign the job to this machine
        assignments[i] = machine_id
        
        # Update the machine's load and push it back to the heap (O(log m))
        heapq.heappush(heap, (load + job_time, machine_id))
    
    # The makespan is the highest load among all machines
    # Since we have m items in the heap, we can find the max load
    makespan = max(load for load, _ in heap)
    
    return (assignments, makespan)

"""
=======================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: O(n log m)
  - n هو عدد المهام.
  - m هو عدد المعالجات.
  - كل عملية `heappop` و `heappush` بتكلف `O(log m)`.
  - الخوارزمية بتنفذ هاتين العمليتين n مرة، فالتعقيد الكلي `O(n log m)`.

- Space Complexity: O(n + m)
  - O(m) لتخزين الكومة (heap) الخاصة بحمولات المعالجات.
  - O(n) لتخزين مصفوفة التوزيع `assignments`.
=======================================================================
"""

# ------------------- Helper (from Previous Problem) -------------------
def compute_makespan(times, m, assign):
    processor_times = [0] * m
    for i in range(len(times)):
        processor_id = assign[i]
        processor_times[processor_id] += times[i]
    return max(processor_times)

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    def do_test(times, m, expected):
        (a, makespan) = greedy_makespan_min(times, m)
        print('\t Assignment returned: ', a)
        print('\t Claimed makespan: ', makespan)
        assert compute_makespan(times, m, a) == makespan, 'Assignment returned is not consistent with the reported makespan'
        assert makespan == expected, f'Expected makespan should be {expected}, your code returned {makespan}'
        print('Passed')

    print('Test 1:')
    times = [2, 2, 2, 2, 2, 2, 2, 2, 3] 
    m = 3
    expected = 7
    do_test(times, m, expected)

    print('Test 2:')
    times = [1]*20 + [5]
    m = 5
    expected = 9
    do_test(times, m, expected)

    print('Test 3:')
    times = [1]*40 + [2]
    m = 20
    expected = 4
    do_test(times, m, expected)
    
    print('All tests passed: 15 points!')
