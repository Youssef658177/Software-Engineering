"""
Problem 1: Longest Stable Subsequence (English & Arabic Explanation)
=====================================================================
1. Problem Statement (English):
-------------------------------
Consider a list of numbers [a0, a1, ..., a_{n-1}]. Our goal is to find the longest stable subsequence: [a_{i1}, a_{i2}, ..., a_{ik}] which is a sub-list of the original list that selects elements at indices i1 < i2 < ... < ik from the original list such that:
1. Each a_{i_{t+1}} is within ±1 or equal to the previous element a_{i_t} (i.e., |a_{i_t} - a_{i_{t+1}}| <= 1).
2. The length of the subsequence k is maximized.

Example:
List = [1, 4, 2, -2, 0, -1, 2, 3]. The longest stable subsequence is [1, 2, 2, 3] of length 4.

=====================================================================
2. Explanation (Arabic):
------------------------
المسألة بتطلب إيجاد أطول "تابع مستقر" (Stable Subsequence) داخل مصفوفة.
الشرط الأساسي لأي عنصرين متتاليين في التابع هو أن يكون الفرق بينهما بالقيمة المطلقة <= 1.

لحل المسألة، نستخدم خوارزمية البرمجة الديناميكية (Dynamic Programming).
الخوارزمية (Bottom-up DP) بتعتمد على فكرة:
- بالنسبة لأي مؤشر `i` (العنصر الحالي) ومؤشر `j` (العنصر السابق المختار في التابع، و `-1` يعني "لا يوجد عنصر سابق"):
    1. إذا كان الفرق بين `a[i]` و `a[j]` (في حالة وجود `j`) أكبر من 1، لا يمكننا اختيار `a[i]`.
    2. إذا كان الفرق مقبولاً (أو `j == -1`)، يكون لدينا خياران: (أ) تخطي العنصر الحالي، أو (ب) اختيار العنصر الحالي (مما يزيد طول التابع بمقدار 1 ويجعل `i` هو العنصر السابق الجديد).
نقوم بحساب القيمة المثلى لكل حالة، ثم نعيد بناء التابع الفعلي باستخدام الجدول الناتج.

=====================================================================
3. Code Implementation:
-----------------------
"""

# ------------------- Recursive Solution (For Problem A) -------------------
def lssLength(a, i, j):
    """
    Recursively finds the length of the longest stable subsequence.
    a: The input array.
    i: The current index being considered.
    j: The index of the last chosen element (-1 indicates None).
    """
    aj = a[j] if 0 <= j < len(a) else None 
    
    # Base Case: If we have reached the end of the array
    if i == len(a):
        return 0
    
    # If we have a previous element (aj) and the difference is > 1,
    # we CANNOT take a[i]. We must skip it.
    if aj is not None and abs(a[i] - aj) > 1:
        return lssLength(a, i + 1, j)
    
    # Otherwise (aj is None or the difference is <= 1):
    # Option 1: Skip a[i]
    skip = lssLength(a, i + 1, j)
    # Option 2: Take a[i]
    take = 1 + lssLength(a, i + 1, i)
    
    # Return the maximum of the two options
    return max(skip, take) 


# ------------------- Memoized / DP Solution (For Problem B) -------------------
def memoizeLSS(a):
    """
    Constructs a memo table for the Longest Stable Subsequence using bottom-up DP.
    T[(i, j)] represents the LSS length for subarray a[i...] given last chosen index j.
    """
    T = {} # Initialize the memo table to empty dictionary
    n = len(a)
    
    # Base case: i = n (end of array)
    for j in range(-1, n):
        T[(n, j)] = 0
    
    # Fill out the table backwards
    for i in range(n-1, -1, -1):
        for j in range(-1, i):
            if j != -1 and abs(a[i] - a[j]) > 1:
                # If the difference is too large, we cannot pick a[i]
                T[(i, j)] = T[(i+1, j)]
            else:
                # Option 1: Skip a[i]
                skip = T[(i+1, j)]
                # Option 2: Take a[i], making i the new previous index
                take = 1 + T[(i+1, i)]
                T[(i, j)] = max(skip, take)
                
    return T


# ------------------- Solution Reconstruction (For Problem C) -------------------
def computeLSS(a):
    """
    Uses the DP table to reconstruct and return the actual longest stable subsequence.
    """
    n = len(a)
    # 1. Build the DP table
    T = {}
    for j in range(-1, n):
        T[(n, j)] = 0
    
    for i in range(n-1, -1, -1):
        for j in range(-1, i):
            if j != -1 and abs(a[i] - a[j]) > 1:
                T[(i, j)] = T[(i+1, j)]
            else:
                skip = T[(i+1, j)]
                take = 1 + T[(i+1, i)]
                T[(i, j)] = max(skip, take)
    
    # 2. Reconstruct the subsequence using the table
    subseq = []
    i = 0
    j = -1
    
    while i < n:
        if j != -1 and abs(a[i] - a[j]) > 1:
            # This element cannot be chosen, skip it
            i += 1
        else:
            # Check if choosing a[i] leads to the optimal solution
            take = 1 + T[(i+1, i)]
            skip = T[(i+1, j)]
            
            if take >= skip:
                subseq.append(a[i])
                j = i  # Update previous index
                i += 1
            else:
                i += 1  # Skip a[i]
                
    return subseq

"""
=====================================================================
4. Time & Space Complexity Analysis:
------------------------------------
1. Recursive Solution: O(2^n) time, O(n) stack space.
2. Memoized/DP Solution: O(n^2) time, O(n^2) space for the DP table.
   - The nested loops fill a table where i ranges from n down to 0, 
     and j ranges from -1 to i-1. 
   - This results in roughly n*(n+1)/2 states, so Θ(n^2).
=====================================================================
"""

# ------------------- Helper Functions & Test Cases -------------------
def checkMemoTableHasEntries(a, T):
    n = len(a)
    for i in range(n+1):
        for j in range(i):
            assert (i, j) in T, f'entry for {(i,j)} not in memo table'
            
def checkMemoTableBaseCase(a, T):
    n = len(a)
    for j in range(-1, n):
        assert T[(n, j)] == 0, f'entry for {(n,j)} is not zero as expected'

def checkSubsequence(a, b):
    i, j = 0, 0
    n, m = len(a), len(b)
    # Verify stable property of subsequence
    for k in range(m-1):
        assert abs(b[k] - b[k+1]) <= 1, "Subsequence is not stable"
    # Verify it is a valid subsequence of a
    while i < n and j < m:
        if a[i] == b[j]: 
            j += 1
        i += 1
    return j == m

if __name__ == "__main__":
    # --- Test Part 1: Recursion ---
    print('-- Recursive Tests --')
    n1 = lssLength([1, 4, 2, -2, 0, -1, 2, 3], 0, -1)
    assert n1 == 4, f'Test 1 failed: expected 4, got {n1}'
    print('Test 1 passed')

    n2 = lssLength([1, 2, 3, 4, 0, 1, -1, -2, -3, -4, 5, -5, -6], 0, -1)
    assert n2 == 8, f'Test 2 failed: expected 8, got {n2}'
    print('Test 2 passed')

    n3 = lssLength([0, 2, 4, 6, 8, 10, 12], 0, -1)
    assert n3 == 1, f'Test 3 failed: expected 1, got {n3}'
    print('Test 3 passed')

    n4 = lssLength([4, 8, 7, 5, 3, 2, 5, 6, 7, 1, 3, -1, 0, -2, -3, 0, 1, 2, 1, 3, 1, 0, -1, 2, 4, 5, 0, 2, -3, -9, -4, -2, -3, -1], 0, -1)
    assert n4 == 14, f'Test 4 failed: expected 14, got {n4}'
    print('Recursive All Tests Passed (8 points)')
    print()

    # --- Test Part 2: Memoization ---
    print('-- Memoization Tests --')
    a1 = [1, 4, 2, -2, 0, -1, 2, 3]
    T1 = memoizeLSS(a1)
    checkMemoTableHasEntries(a1, T1)
    checkMemoTableBaseCase(a1, T1)
    assert T1[(0, -1)] == 4, f'Test 1: Expected answer is 4. got {T1[(0, -1)]}'
    print('Test 1 passed')

    a2 = [1, 2, 3, 4, 0, 1, -1, -2, -3, -4, 5, -5, -6]
    T2 = memoizeLSS(a2)
    checkMemoTableHasEntries(a2, T2)
    checkMemoTableBaseCase(a2, T2)
    assert T2[(0, -1)] == 8, f'Test 2: Expected answer is 8. got {T2[(0, -1)]}'
    print('Test 2 passed')

    a3 = [0, 2, 4, 6, 8, 10, 12]
    T3 = memoizeLSS(a3)
    checkMemoTableHasEntries(a3, T3)
    checkMemoTableBaseCase(a3, T3)
    assert T3[(0, -1)] == 1, f'Test 3: Expected answer is 1. got {T3[(0, -1)]}'
    print('Test 3 passed')

    a4 = [4, 8, 7, 5, 3, 2, 5, 6, 7, 1, 3, -1, 0, -2, -3, 0, 1, 2, 1, 3, 1, 0, -1, 2, 4, 5, 0, 2, -3, -9, -4, -2, -3, -1]
    T4 = memoizeLSS(a4)
    checkMemoTableHasEntries(a4, T4)
    checkMemoTableBaseCase(a4, T4)
    assert T4[(0, -1)] == 14, f'Test 4: Expected answer is 14. got {T4[(0, -1)]}'
    print('Memoization All Tests Passed (7 points)')
    print()

    # --- Test Part 3: Reconstruction ---
    print('-- Reconstruction Tests --')
    a1 = [1, 4, 2, -2, 0, -1, 2, 3]
    sub1 = computeLSS(a1)
    assert len(sub1) == 4, f'Subsequence length should be 4'
    assert checkSubsequence(a1, sub1), f'Subsequence is not valid'
    print('Test 1 passed')

    a2 = [1, 2, 3, 4, 0, 1, -1, -2, -3, -4, 5, -5, -6]
    sub2 = computeLSS(a2)
    assert len(sub2) == 8
    assert checkSubsequence(a2, sub2)
    print('Test 2 passed')

    a3 = [0, 2, 4, 6, 8, 10, 12]
    sub3 = computeLSS(a3)
    assert len(sub3) == 1
    assert checkSubsequence(a3, sub3)
    print('Test 3 passed')

    a4 = [4, 8, 7, 5, 3, 2, 5, 6, 7, 1, 3, -1, 0, -2, -3, 0, 1, 2, 1, 3, 1, 0, -1, 2, 4, 5, 0, 2, -3, -9, -4, -2, -3, -1]
    sub4 = computeLSS(a4)
    assert len(sub4) == 14
    assert checkSubsequence(a4, sub4)
    print('Test 4 passed')
    
    print('Reconstruction All Tests Passed (10 points)')
