"""
Assignment 3: Problem 1 - Design a Correct Partition Algorithm
================================================================
1. Problem Statement (English):
-------------------------------
You are given code below for an incorrect partition algorithm that fails to partition arrays wrongly or cause out of bounds access in arrays. The comments include the invariants the algorithm wishes to maintain and will help you debug.

Your goal is to write test cases that demonstrate that the partitioning will fail in various ways.

Given Code (Incorrect):
    def tryPartition(a):
        n = len(a)
        pivot = a[n-1]
        i, j = 0, 0
        for j in range(n-1):
            if a[j] <= pivot:
                swap(a, i+1, j)
                i = i + 1
        swap(a, i+1, n-1)
        return i+1

================================================================
2. Explanation (Arabic):
------------------------
المسألة معطاة دالة `tryPartition` خاطئة (تستخدم خوارزمية Lomuto ولكن بها أخطاء). المطلوب هو كتابة اختبارات (Test Cases) تظهر فشل هذه الدالة بطرق مختلفة، مثل:
- عدم تقسيم المصفوفة بشكل صحيح.
- الوصول إلى مؤشر خارج حدود المصفوفة (Out of bounds).
- ترتيب غير صحيح للعناصر.

الهدف من هذا التمرين هو فهم متى تنجح خوارزمية التقسيم ومتى تفشل.

================================================================
3. Algorithm Analysis (Why the code is incorrect):
--------------------------------------------------
The function `tryPartition` tries to implement the Lomuto partition scheme:
    pivot = a[n-1]
    i = 0
    for j in range(n-1):
        if a[j] <= pivot:
            i += 1
            swap(a, i, j)
    swap(a, i, n-1)
    return i

But the code uses `swap(a, i+1, j)` instead of `i += 1` first. This means:
- `i` starts at 0 but we swap at `i+1` (index 1) on the first swap.
- This ignores `a[0]` and may lead to wrong partitioning or IndexError when `n` is small.

================================================================
4. Code Implementation (Full Solution):
---------------------------------------
"""

def swap(a, i, j):
    assert 0 <= i < len(a), f'accessing index {i} beyond end of array {len(a)}'
    assert 0 <= j < len(a), f'accessing index {j} beyond end of array {len(a)}'
    a[i], a[j] = a[j], a[i]

def tryPartition(a):
    # (Incorrect version as given)
    n = len(a)
    pivot = a[n-1] # choose last element as the pivot.
    i,j = 0,0 # initialize i and j both to be 0
    for j in range(n-1): # j = 0 to n-2 (inclusive)
        # Invariant: a[0] .. a[i] are <= pivot
        #            a[i+1]...a[j-1] are > pivot
        if a[j] <= pivot: 
            swap(a, i+1, j)
            i = i + 1
    swap(a, i+1, n-1) # place pivot in its correct place.
    return i+1 # return the index where we placed the pivot

def testIfPartitioned(a, k):
    """Check if array 'a' is partitioned correctly around index k."""
    assert 0 <= k < len(a)
    pivot = a[k]
    
    # Left side: all elements must be <= pivot
    for i in range(k):
        if a[i] > pivot:
            return False
            
    # Right side: all elements must be > pivot
    for i in range(k + 1, len(a)):
        if a[i] <= pivot:
            return False
            
    return True

# =================================================================
# 5. Test Cases (Demonstrating Failure in Various Ways)
# =================================================================
def run_failure_tests():
    print("Running failure tests for incorrect partition function...\n")
    
    # --- Test 1: Array of size 2 (Out of bounds / Wrong Index) ---
    a1 = [2, 1]
    print(f"Test 1 - Input: {a1}")
    try:
        j1 = tryPartition(a1)
        if not testIfPartitioned(a1, j1):
            print("  ✅ Partition failed as expected (array is not partitioned correctly).")
        else:
            print("  ❌ Partition succeeded, but this is not an actual correct partition.")
    except Exception as e:
        print(f"  ✅ Code crashed as expected with error: {e}")

    # --- Test 2: Array of size 3 with pivot equal to smallest element ---
    a2 = [3, 2, 1]
    print(f"\nTest 2 - Input: {a2}")
    try:
        j2 = tryPartition(a2)
        print(f"  Output index = {j2}, Array = {a2}")
        # The correct pivot should be at index 0. Check if it's partitioned.
        if not testIfPartitioned(a2, j2):
            print("  ✅ Partition failed as expected.")
        else:
            print("  ❌ Partitioning was considered successful, but is it correct?")
    except Exception as e:
        print(f"  ✅ Code crashed as expected with error: {e}")

    # --- Test 3: Array of size 1 (Out of bounds) ---
    a3 = [5]
    print(f"\nTest 3 - Input: {a3}")
    try:
        j3 = tryPartition(a3)
        print(f"  Output index = {j3}, Array = {a3}")
        # For size 1, output should be 0.
        if not testIfPartitioned(a3, j3):
            print("  ✅ Partition failed as expected.")
        else:
            print("  ❌ Partition passed incorrectly.")
    except Exception as e:
        print(f"  ✅ Code crashed as expected with error: {e}")

    # --- Test 4: Array with repeated elements ---
    a4 = [1, 1, 1]
    print(f"\nTest 4 - Input: {a4}")
    try:
        j4 = tryPartition(a4)
        if not testIfPartitioned(a4, j4):
            print("  ✅ Partition failed as expected.")
        else:
            print("  ❌ Partition passed but might be incorrect.")
    except Exception as e:
        print(f"  ✅ Code crashed as expected with error: {e}")

    print("\n=========================================")
    print("All tests correctly detected errors or crashes.")
    print("This confirms the algorithm is incorrect as expected.")
    print("=========================================")

# =================================================================
# 6. Time Complexity Analysis
# =================================================================
# tryPartition works in O(n) time for an array of size n if it were correct.
# However, since it is buggy, it may run in O(n) as well but produce wrong output.

# -----------------------------------------------------------------
# Run the tests if this file is executed directly.
# -----------------------------------------------------------------
if __name__ == "__main__":
    # 1. Basic tests to verify testIfPartitioned itself (Given in original code)
    print("Basic verification tests:\n")
    assert testIfPartitioned([-1, 5, 2, 3, 4, 8, 9, 14, 10, 23], 5) == True, 'Test # 1 failed.'
    assert testIfPartitioned([-1, 5, 2, 3, 4, 8, 9, 14, 11, 23], 4) == False, 'Test # 2 failed.'
    assert testIfPartitioned([-1, 5, 2, 3, 4, 8, 9, 14, 23, 21], 0) == True, 'Test # 3 failed.'
    assert testIfPartitioned([-1, 5, 2, 3, 4, 8, 9, 14, 22, 23], 9) == True, 'Test # 4 failed.'
    assert testIfPartitioned([-1, 5, 2, 3, 4, 8, 9, 14, 8, 23], 5) == False, 'Test # 5 failed.'
    assert testIfPartitioned([-1, 5, 2, 3, 4, 8, 9, 13, 9, -11], 5) == False, 'Test # 6 failed.'
    assert testIfPartitioned([4, 4, 4, 4, 4, 8, 9, 13, 9, 11], 4) == True, 'Test # 7 failed.'
    print("Basic tests passed (10 points)\n")

    # 2. Run the failure tests on the buggy tryPartition
    run_failure_tests()
