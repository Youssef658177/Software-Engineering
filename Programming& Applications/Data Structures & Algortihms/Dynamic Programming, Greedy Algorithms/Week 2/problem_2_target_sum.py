"""
Problem 2: Target Sum (Subset Sum with Minimum Difference) (English & Arabic Explanation)
=========================================================================================
1. Problem Statement (English):
-------------------------------
We are given a set of natural numbers S = {n1, ..., nk} and a target natural number N.

Our goal is to choose a subset of numbers T = {n_{i1}, ..., n_{ij}} ⊆ S such that:
    1. The sum of chosen numbers is less than or equal to N.
    2. The difference N - sum(T) is made as small as possible.

Example:
    S = {1, 2, 3, 4, 5, 10} and N = 20.
    Choosing T = {2, 3, 5, 10} gives a sum of 20, achieving a difference of 0.

This is a classic variation of the Subset Sum problem solved using Dynamic Programming.

=========================================================================================
2. Explanation (Arabic):
------------------------
المسألة بتطلب اختيار مجموعة فرعية (Subset) من الأرقام المعطاة بحيث مجموعها أقل من أو يساوي رقم معين N، ويكون الفرق بين N ومجموع الأرقام المختارة هو أصغر فرق ممكن (أقرب قيمة ممكنة لـ N).

لحل المسألة، نستخدم خوارزمية البرمجة الديناميكية (Dynamic Programming):
- **الفكرة:** بالنسبة لأي عنصر `S[i]`، لدينا خياران: (1) تخطيه، أو (2) أخذه (إذا كان مجموع العناصر المأخوذة لا يتجاوز الهدف `tgt`).
- نقوم ببناء جدول `T` بحيث `T[(i, j)]` يمثل أفضل (أصغر) فرق يمكن تحقيقه عند النظر في المصفوفة الفرعية `S[i:]` مع هدف متبقي `j`.
- بعد حساب الجدول، نقوم بتراجع (Backtracking) لتحديد العناصر التي تم اختيارها فعليًا لتكوين المجموعة الفرعية المثلى.

=========================================================================================
3. Code Implementation:
-----------------------
"""

# ------------------- Part (A): Recursive Solution -------------------
def targetSum(S, i, tgt):
    """
    Recursively finds the minimum difference to reach the target `tgt` from array `S` starting at index `i`.
    """
    # Base Case 1: If we have gone beyond the target, this path is invalid
    if tgt < 0:
        return float('inf')
    
    # Base Case 2: If we have processed all elements, return the current difference
    if i >= len(S):
        return tgt
    
    # Recursive Case: Try both options and return the minimum difference
    # Option 1: Skip the current element S[i]
    skip = targetSum(S, i+1, tgt)
    
    # Option 2: Take the current element S[i]
    take = targetSum(S, i+1, tgt - S[i])
    
    # Return the better (smaller difference) option
    return min(skip, take) 

def tgtSum(tgt, S):
    """Wrapper function to easily call the targetSum recursion."""
    return targetSum(S, 0, tgt)


# ------------------- Part (B): Memoized / DP Solution -------------------
def memoTargetSum(S, tgt):
    """
    Constructs a memo table for the Target Sum problem using bottom-up DP.
    T[(i, j)] represents the best (minimum) difference achievable for subarray S[i:] with remaining target j.
    """
    k = len(S)
    assert tgt >= 0
    # Initialize memo table
    T = {}
    # Base case: when we reach the end of the array (i == k), difference is just the remaining target `j`
    for j in range(tgt + 1):
        T[(k, j)] = j
    
    # Fill the table from the bottom (i = k-1) to the top (i = 0)
    for i in range(k-1, -1, -1):
        for j in range(tgt + 1):
            # Option 1: Skip S[i]
            skip = T[(i+1, j)]
            
            # Option 2: Take S[i] (only if we have enough capacity j)
            if S[i] <= j:
                take = T[(i+1, j - S[i])]
                T[(i, j)] = min(skip, take)
            else:
                T[(i, j)] = skip
                
    return T


# ------------------- Part (C): Reconstruct the Subset -------------------
def getBestTargetSum(S, tgt):
    """
    Uses the DP table to reconstruct and return the actual subset `res` that achieves the optimal minimum difference.
    """
    k = len(S)
    assert tgt >= 0
    
    # 1. Build the DP table
    T = {}
    for j in range(tgt + 1):
        T[(k, j)] = j
        
    for i in range(k-1, -1, -1):
        for j in range(tgt + 1):
            skip_diff = T[(i+1, j)]
            if S[i] <= j:
                take_diff = T[(i+1, j - S[i])]
                T[(i, j)] = min(skip_diff, take_diff)
            else:
                T[(i, j)] = skip_diff
    
    # 2. Reconstruct the subset using backtracking
    res = []
    i = 0
    j = tgt
    
    while i < k:
        if S[i] <= j:
            take_diff = T[(i+1, j - S[i])]
            skip_diff = T[(i+1, j)]
            
            # If taking the element leads to a better (smaller) difference, include it
            if take_diff <= skip_diff:
                res.append(S[i])
                j -= S[i]  # Update the remaining target
        # Move to the next element
        i += 1
        
    return res


"""
=========================================================================================
4. Time & Space Complexity Analysis:
------------------------------------
1. Recursive Solution (Part A): 
   - Time: O(2^n). Space: O(n) (stack depth).
2. Memoized/DP Solution (Parts B & C):
   - Time: O(n * tgt). The DP table is filled with a nested loop where `n` is len(S) and `tgt` is the target value.
   - Space: O(n * tgt) to store the DP table `T`.
=========================================================================================
"""

# ------------------- Helper Functions & Test Cases -------------------
def checkMemoTblTargetSum(a, tgt, expected):
    T = memoTargetSum(a, tgt)
    for i in range(len(a)+1):
        for j in range(tgt+1):
            assert (i, j) in T, f'Memo table fails to have entry for i, j = {(i, j)}'
    assert T[(0, tgt)] == expected, f'Expected answer = {expected}, your code returns {T[(0, tgt)]}'
    return 

def checkTgtSumRes(a, tgt, expected):
    a = sorted(a)
    res = getBestTargetSum(a, tgt)
    res = sorted(res)
    print('Your result:' , res)
    assert tgt - sum(res)  == expected, f'Your code returns result that sums up to {sum(res)}, expected was {expected}'
    # Verify `res` is a valid subset of `a`
    i = 0
    j = 0
    n = len(a)
    m = len(res)
    while (i < n and j < m):
        if a[i] == res[j]: 
            j = j + 1
        i = i + 1
    assert j == m, 'Your result {res} is not a subset of {a}'

if __name__ == "__main__":
    # --- Part A: Recursion Tests ---
    print('-- Recursive Tests --')
    t1 = tgtSum(15, [1, 2, 3, 4, 5, 10])
    assert t1 == 0, 'Test 1 failed'
    t2 = tgtSum(26, [1, 2, 3, 4, 5, 10])
    assert t2 == 1, 'Test 2 failed'
    t3 = tgtSum(23, [1, 2, 3, 4, 5, 10])
    assert t3 == 0, 'Test 3 failed'
    t4 = tgtSum(18, [1, 2, 3, 4, 5, 10])
    assert t4 == 0, 'Test 4 failed'
    t5 = tgtSum(9, [1, 2, 3, 4, 5, 10])
    assert t5 == 0, 'Test 5 failed'
    t6 = tgtSum(457, [11, 23, 37, 48, 94, 152, 230, 312, 339, 413])
    assert t6 == 1, 'Test 6 failed'
    t7 = tgtSum(512, [11, 23, 37, 48, 94, 152, 230, 312, 339, 413])
    assert t7 == 0, 'Test 7 failed'
    t8 = tgtSum(616, [11, 23, 37, 48, 94, 152, 230, 312, 339, 413])
    assert t8 == 1, 'Test 8 failed'
    print('All tests passed (10 points)!')

    # --- Part B: Memoization Tests ---
    print('\n-- Memoization Tests --')
    print('--test 1--')
    a1 = [1, 2, 3, 4, 5, 10]
    print(a1, 15)
    checkMemoTblTargetSum(a1, 15, 0)

    print('--test 2--')
    a2 = [1, 2, 3, 4, 5, 10]
    print(a2, 26)
    checkMemoTblTargetSum(a2, 26, 1)

    print('--test3--')
    a3 = [11, 23, 37, 48, 94, 152, 230, 312, 339, 413]
    print(a3, 457)
    checkMemoTblTargetSum(a3, 457, 1)

    print('--test4--')
    print(a3, 512)
    checkMemoTblTargetSum(a3, 512, 0)

    print('--test5--')
    print(a3, 616)
    checkMemoTblTargetSum(a3, 616, 1)
    print('All tests passed (10 points)!')

    # --- Part C: Reconstruction Tests ---
    print('\n-- Reconstruction Tests --')
    print('--test 1--')
    a1 = [1, 2, 3, 4, 5, 10]
    print(a1, 15)
    checkTgtSumRes(a1, 15, 0)

    print('--test 2--')
    a2 = [1, 8, 3, 4, 5, 12]
    print(a2, 26)
    checkTgtSumRes(a2, 26, 0)

    print('--test 3--')
    a3 = [8, 3, 2, 4, 5, 7, 12]
    print(a3, 38)
    checkTgtSumRes(a3, 38, 0)

    print('--test 4 --')
    a4 = sorted([1, 10, 19, 18, 12, 11, 0, 9, 16, 17, 2, 7, 14, 29, 38, 45, 13, 26, 51, 82, 111, 124, 135, 189])
    print(a4)
    checkTgtSumRes(a4, 155, 0)
    
    print('--test 5--')
    checkTgtSumRes(a4, 189, 0)

    print('--test 7--')
    checkTgtSumRes(a4, 347, 0)

    print('--test 8--')
    checkTgtSumRes(a4, 461, 0)

    print('--test 9--')
    checkTgtSumRes(a4, 462, 0)

    print('--test 9--')
    checkTgtSumRes(a4, 517, 0)

    print('--test 10--')
    checkTgtSumRes(a4, 975, 3)

    print('All Tests Passed (15 points)')
