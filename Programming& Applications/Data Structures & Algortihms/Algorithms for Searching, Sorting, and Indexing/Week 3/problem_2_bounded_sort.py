"""
Problem 2: Rapid Sorting of Arrays with Bounded Number of Elements
==================================================================
1. Problem Statement (English):
-------------------------------
We have presented sorting algorithms that are comparison-based. Now, develop a rapid sorting algorithm for an array of size n when all elements are between 1, ..., k for a given k.

Example: n = 100,000, k = 100.

Develop a sorting algorithm using partition that runs in Θ(n * k) time.

(A) Describe your algorithm as pseudocode and argue why it runs in Θ(n * k).

(B) Complete the implementation of `boundedSort(a, k)` by completing `simplePartition(a, pivot)`.

================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب خوارزمية فرز سريع للمصفوفات التي تحتوي على عناصر في نطاق محدود (1 إلى k).
الفكرة المستخدمة في الكود أدناه هي:
- نبدأ بـ `pivot = 1` ونجري `simplePartition` لتقسيم العناصر (<= 1) إلى البداية.
- ثم ننتقل إلى `pivot = 2` ونجري `simplePartition` لتقسيم العناصر (<= 2) إلى البداية.
- نكرر حتى `pivot = k-1`.
- النتيجة: مصفوفة مرتبة بالكامل.

تعقيد الوقت: Θ(n * k) لأن `simplePartition` تكلف Θ(n) وتُستدعى (k-1) مرة.

================================================================
3. Code Implementation (Part B):
--------------------------------
"""

def swap(a, i, j):
    assert 0 <= i < len(a), f'accessing index {i} beyond end of array {len(a)}'
    assert 0 <= j < len(a), f'accessing index {j} beyond end of array {len(a)}'
    a[i], a[j] = a[j], a[i]

def simplePartition(a, pivot):
    """Partition array a in-place: elements <= pivot first, then elements > pivot."""
    i = 0  # number of elements placed in the first part (<= pivot)
    for j in range(len(a)):
        if a[j] <= pivot:
            swap(a, i, j)
            i += 1

def boundedSort(a, k):
    for j in range(1, k):
        simplePartition(a, j)

"""
================================================================
4. Time Complexity Analysis (Part A & Part B):
---------------------------------------------
- `simplePartition` runs in Θ(n) because it iterates through the array once.
- `boundedSort` calls `simplePartition` (k-1) times.
- Total time: Θ(n * k).

================================================================
5. Test Cases:
--------------
"""
if __name__ == "__main__":
    a = [1, 3, 6, 1, 5, 4, 1, 1, 2, 3, 3, 1, 3, 5, 2, 2, 4]
    print("Original array:", a)

    simplePartition(a, 1)
    assert(a[:5] == [1,1,1,1,1]), 'Simple partition test 1 failed'

    simplePartition(a, 2)
    assert(a[:5] == [1,1,1,1,1]), 'Simple partition test 2(A) failed'
    assert(a[5:8] == [2,2,2]), 'Simple Partition test 2(B) failed'

    simplePartition(a, 3)
    assert(a[:5] == [1,1,1,1,1]), 'Simple partition test 3(A) failed'
    assert(a[5:8] == [2,2,2]), 'Simple Partition test 3(B) failed'
    assert(a[8:12] == [3,3,3,3]), 'Simple Partition test 3(C) failed'

    simplePartition(a, 4)
    assert(a[:5] == [1,1,1,1,1]), 'Simple partition test 4(A) failed'
    assert(a[5:8] == [2,2,2]), 'Simple Partition test 4(B) failed'
    assert(a[8:12] == [3,3,3,3]), 'Simple Partition test 4(C) failed'
    assert(a[12:14]==[4,4]), 'Simple Partition test 4(D) failed'

    simplePartition(a, 5)
    assert(a == [1]*5+[2]*3+[3]*4+[4]*2+[5]*2+[6]), 'Simple Partition test 5 failed'

    print('Passed all tests : 10 points!')
