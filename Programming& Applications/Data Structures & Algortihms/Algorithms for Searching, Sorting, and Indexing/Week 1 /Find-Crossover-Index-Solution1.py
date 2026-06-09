"""
Problem 1: Find Crossover Indices (English & Arabic Explanation)
================================================================
1. Problem Statement (English):
-------------------------------
You are given data that consists of points (x_0, y_0), ..., (x_n, y_n), wherein
x_0 < x_1 < ... < x_n, and y_0 < y_1 < ... < y_n as well.

Furthermore, it is given that y_0 < x_0 and y_n > x_n.

Find a "cross-over" index i between 0 and n - 1 such that y_i <= x_i and
y_{i+1} > x_{i+1}. Note that such an index must always exist.

Example: Your algorithm must find the index i = 3 as the crossover point.
   i:   0  1  2  3  4  5  6  7
   x_i: 0  2  4  5  6  7  8  10
   y_i: -2 0  2  4  7  8  10 12 (Crossover at i=3)

Design an algorithm to find an index i in {0, 1, ..., n - 1} such that
x_i >= y_i but x_{i+1} < y_{i+1}.

Describe your algorithm using python code for a function:
findCrossoverIndexHelper(x, y, left, right)

Parameters:
- x: list of x values sorted in increasing order.
- y: list of y values sorted in increasing order.
- x and y are lists of same size (n).
- left and right are indices that represent the current search region
  in the list such that 0 <= left < right <= n.

Hint: Modify the binary search algorithm. Your solution must use recursion.

================================================================
2. Explanation (Arabic):
------------------------
عندنا مصفوفتين مرتبين تصاعدياً: x و y.
المطلوب: إيجاد "نقطة عبور" (Crossover Index) i.

الشروط اللي بتحدد نقطة العبور:
1. x[i] >= y[i]  (قبل العبور، x أكبر أو يساوي y)
2. x[i+1] < y[i+1] (بعد العبور، x أصبح أصغر من y)

الخصائص المهمة في البيانات (مضمونة):
- في البداية: y0 < x0  (لأن y أقل من x)
- في النهاية: yn > xn  (لأن y أكبر من x)
- مضمون وجود نقطة عبور واحدة على الأقل في النطاق من 0 لـ n-1.

================================================================
3. Algorithm (Modified Binary Search):
--------------------------------------
الحل بيعتمد على البحث الثنائي (Binary Search) لكن بشكل مختلف:
1. بنحسب المؤشر الأوسط (mid) بين left و right.
2. بنقارن x[mid] بـ y[mid]:
   - لو x[mid] >= y[mid]: ده معناه إننا لسه في المنطقة اللي قبل العبور،
     يبقى العبور موجود في النص اللي بعد الـ mid (نبحث في [mid, right]).
   - لو x[mid] < y[mid]: ده معناه إننا تعدينا العبور ودخلنا المنطقة اللي بعده،
     يبقى العبور موجود في النص اللي قبل الـ mid (نبحث في [left, mid]).
3. بنكرر الخطوات دي (Recursion) لحد ما نوصل لمؤشرين متجاورين (left, right).
4. ساعتها بنرجع left، لأنه هو آخر مؤشر حقق الشرط الأول.

================================================================
4. Time Complexity:
-------------------
O(log n)
لأننا بنقسم نطاق البحث للنصف في كل خطوة، الخوارزمية بتاخد وقت لوغاريتمي.
ده معناه إنها سريعة جداً حتى لو البيانات كبيرة.

================================================================
5. Test Cases (Assertions):
----------------------------
الاختبارات بتتأكد إن الدالة شغالة صح في حالات مختلفة:
1. حالة عادية (j1) → الناتج المفروض 1.
2. حالة فيها كسور وعشوائية (j2) → الناتج المفروض 1 أو 5 (لأن المسار في البحث الثنائي ممكن يوصل لأي منهم والاتنين صح).
3. حالة فيها عنصرين فقط (j3) → الناتج المفروض 0.
4. حالة عادية تانية (j4) → الناتج المفروض 2.

لو كل الاختبارات دي نجحت، بيظهر: "Congratulations: all test cases passed - 10 points"
وده معناه إن الحل صحيح 100%.
================================================================
"""

# ------------------- Code Implementation -------------------

def findCrossoverIndexHelper(x, y, left, right):
    """
    Recursively find crossover index i in [left, right] such that:
        x[i] >= y[i] and x[i+1] < y[i+1]
    Invariants maintained:
        x[left] > y[left]
        x[right] < y[right]
    """
    # Base case: adjacent indices -> crossover at left
    if left + 1 == right:
        return left

    mid = (left + right) // 2

    if x[mid] >= y[mid]:
        # Crossover is to the right (or at mid)
        return findCrossoverIndexHelper(x, y, mid, right)
    else:
        # x[mid] < y[mid] -> crossover to the left
        return findCrossoverIndexHelper(x, y, left, mid)

def findCrossoverIndex(x, y):
    """
    Wrapper function that calls the helper with the full range.
    Assumes:
        len(x) == len(y) >= 2
        x[0] > y[0]   (given y0 < x0)
        x[-1] < y[-1] (given yn > xn)
    """
    return findCrossoverIndexHelper(x, y, 0, len(x) - 1)

# ------------------- Test Cases -------------------

if __name__ == "__main__":
    print("Running Test Cases...")
    
    # Test Case 1: Standard case
    j1 = findCrossoverIndex([0, 1, 2, 3, 4, 5, 6, 7], [-2, 0, 4, 5, 6, 7, 8, 9])
    print('j1 = %d' % j1)
    assert j1 == 1, "Test Case # 1 Failed"

    # Test Case 2: Case where there could be multiple crossovers (due to float points)
    j2 = findCrossoverIndex([0, 1, 2, 3, 4, 5, 6, 7], [-2, 0, 4, 4.2, 4.3, 4.5, 8, 9])
    print('j2 = %d' % j2)
    # It can output either 1 or 5 depending on the binary search path, both are correct
    assert j2 == 1 or j2 == 5, "Test Case # 2 Failed"

    # Test Case 3: Small array edge case
    j3 = findCrossoverIndex([0, 1], [-10, 10])
    print('j3 = %d' % j3)
    assert j3 == 0, "Test Case # 3 Failed"

    # Test Case 4: Another standard case
    j4 = findCrossoverIndex([0, 1, 2, 3], [-10, -9, -8, 5])
    print('j4 = %d' % j4)
    assert j4 == 2, "Test Case # 4 Failed"

    print("Congratulations: all test cases passed - 10 points")
