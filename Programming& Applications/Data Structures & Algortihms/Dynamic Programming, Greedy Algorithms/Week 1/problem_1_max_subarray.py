"""
Problem 1: Max Subarray Problem (English & Arabic Explanation)
===============================================================
1. Problem Statement (English):
-------------------------------
Recall the max subarray problem presented in class. We used divide and conquer method to derive a Θ(n log n) worst case time algorithm to solve it.

In this assignment, we would like you to solve this problem in Θ(n) time. i.e, your algorithm should be able to compute the result by just iterating through the array and keeping track of some quantities.

Let [a0, a1, ..., ak] be a python array (list) of size k + 1. Here is the idea:
As we iterate index i from 0 to k (inclusive), track a quantity `minSoFar` that is the minimum of the array so far from 0 to i-1. Initialize `minSoFar` to +infinity.
Consider the difference `a[i] - minSoFar`. Calculate the maximum such difference when iterating over the entire array.

Convince yourself that this will yield the overall solution to the max subarray problem with a Θ(n) complexity.

================================================================
2. Explanation (Arabic):
------------------------
المسألة بتطلب إيجاد **أقصى فرق (Max Difference)** بين عنصرين في مصفوفة، بحيث يكون العنصر الأكبر في الجانب الأيمن (يأتي بعد) العنصر الأصغر.
الفكرة المستخدمة في الكود لتحقيق تعقيد زمني خطي `Θ(n)`:
- بنمر على المصفوفة مرة واحدة (Loop واحد).
- بنحتفظ بمتغير `minSoFar`، وده بيخزن أقل قيمة شوفناها في المصفوفة من أول عنصر لحد العنصر اللي قبل العنصر الحالي.
- بنحسب الفرق بين العنصر الحالي `a[i]` وأقل قيمة سابقة `minSoFar`.
- لو الفرق ده أكبر من أقصى فرق سجلناه (`max_diff`)، بنحدث `max_diff`.
- ولو لقينا عنصر أصغر من `minSoFar`، بنحدث `minSoFar` عشان نستخدمه في الحسابات الجاية.

================================================================
3. Code Implementation:
-----------------------
"""

def maxSubArray(a):
    n = len(a)
    if n == 1:
        return 0
    # Initialize minSoFar to positive infinity
    minSoFar = float('inf')
    max_diff = 0
    # Iterate through the array
    for i in range(n):
        # Update minSoFar with the first element
        if i == 0:
            minSoFar = a[0]
            continue
        # Calculate the difference between current element and minSoFar
        diff = a[i] - minSoFar
        # Update max_diff if a larger difference is found
        if diff > max_diff:
            max_diff = diff
        # Update minSoFar if a smaller element is found
        if a[i] < minSoFar:
            minSoFar = a[i]
    return max_diff

"""
================================================================
4. Time Complexity Analysis:
----------------------------
- Time Complexity: Θ(n)
  لأن الخوارزمية بتستخدم حلقة واحدة (for loop) بتعدي على عناصر المصفوفة مرة واحدة فقط.
- Space Complexity: O(1)
  لأننا بنستخدم فقط متغيرات بسيطة (`minSoFar`, `max_diff`, `diff`) ولا بنخزن أي مصفوفات إضافية.
================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    from random import randint

    print("Running basic tests...")
    assert(maxSubArray([100, -2, 5, 10, 11, -4, 15, 9, 18, -2, 21, -11]) == 25), 'Test 1 failed'
    assert(maxSubArray([-5, 1, 10, 4, 11, 4, 15, 9, 18, 0, 21, -11]) == 26), 'Test 2 failed'
    assert(maxSubArray([26, 0, 5, 18, 11, -1, 15, 9, 13, 5, 16, -11]) == 18), 'Test 3 failed'

    def get_random_array(n):
        assert(n > 100)
        lst = [randint(0, 25) for j in range(n)]
        lst[0] = 1000
        lst[10] = -15
        lst[25] = 40
        lst[n-10] = 60
        lst[n-3] = -40
        return lst

    print("Running large random array tests...")
    assert(maxSubArray(get_random_array(50000)) == 75), 'Test on large random array 50000 failed'
    assert(maxSubArray(get_random_array(500000)) == 75), 'Test on large random array of size 500000 failed'
    
    print('All tests passed (10 points!)')
