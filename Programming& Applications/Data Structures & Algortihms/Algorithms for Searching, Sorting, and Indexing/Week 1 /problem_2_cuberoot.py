"""
Problem 2: Find Integer Cube Root (English & Arabic Explanation)
================================================================
1. Problem Statement (English):
-------------------------------
The integer cube root of a positive number n is the smallest number i such that:
    i^3 <= n but (i+1)^3 > n

For instance, the integer cube root of 100 is 4 since 4^3 <= 100 but 5^3 > 100.
Likewise, the integer cube root of 1000 is 10.

Write a function integerCubeRootHelper(n, left, right) that searches for the
integer cube root of n between left and right given the following pre-conditions:
- n >= 1
- left < right
- left^3 < n
- right^3 > n

================================================================
2. Explanation (Arabic):
------------------------
المسألة بتطلب إيجاد "الجذر التكعيبي الصحيح" لعدد موجب n.
الجذر التكعيبي الصحيح هو أصغر عدد صحيح i بحيث:
    i^3 <= n   و   (i+1)^3 > n

مثال: الجذر التكعيبي الصحيح لـ 100 هو 4 لأن:
    4^3 = 64 <= 100
    5^3 = 125 > 100

لحل المسألة، بنستخدم خوارزمية البحث الثنائي (Binary Search) في دالة مساعدة
integerCubeRootHelper. الدالة دي بتاخد n ومؤشرين left و right (اللي بينهم البحث).
شروط الدالة المساعدة:
- left < right
- left^3 < n
- right^3 > n

الدالة الرئيسية integerCubeRoot بتدير عملية البحث: بتلاقي right مناسب (بالمضاعفة)
وبتتأكد إن left مناسب، وبعدين بتنادي الدالة المساعدة.

================================================================
3. Algorithm (Modified Binary Search):
--------------------------------------
الخوارزمية بتعتمد على البحث الثنائي:
1. في الدالة integerCubeRoot:
   - بنبدأ بـ right = 1 ونضاعفه لحد ما right^3 > n.
   - بنحدد left = right // 2 ونتأكد إن left^3 < n.
2. في الدالة integerCubeRootHelper:
   - بنحسب المؤشر الأوسط: mid = (left + right) // 2.
   - بنقارن cube(mid) بـ n:
     - لو cube(mid) < n: الجذر في النص اليمين [mid, right].
     - لو cube(mid) == n: وجدنا الجذر الصحيح، نرجع mid.
     - لو cube(mid) > n: الجذر في النص الشمال [left, mid].
3. بنكرر الخطوات لحد ما نوصل left + 1 == right، وساعتها بنرجع left.

================================================================
4. Time Complexity:
-------------------
O(log n)
لأننا بنقسم نطاق البحث للنصف في كل خطوة (Binary Search).
الجزء الأول (تحديد right) بياخد O(log n) كمان لأنه بيضاعف right لحد ما يوصل n.

================================================================
5. Inductive Invariant (Parts B & C):
--------------------------------------
(B) Prove that the integer cube root j lies between left and right:
    Invariant: left^3 < n < right^3
    - Since j^3 <= n < (j+1)^3, and left^3 < n, right^3 > n, then left <= j < right.
    
(C) Maintain the invariant recursively:
    - If cube(mid) < n, call helper(n, mid, right). New range: mid^3 < n < right^3. Invariant holds.
    - If cube(mid) > n, call helper(n, left, mid). New range: left^3 < n < mid^3. Invariant holds.
    - If cube(mid) == n, return mid (recursion ends).

================================================================
6. Test Cases (Assertions):
----------------------------
الاختبارات بتتأكد إن الدالة شغالة صح لكل الأرقام:
- أرقام صغيرة: 1, 2, 4, 7 -> جذرهم 1
- 8 -> 2
- 20, 26 -> 2
- كل الأرقام من 27 لـ 63 -> 3
- وكل النطاقات لحد 512 -> 7

لو كل الاختبارات نجحت، بيظهر:
"Congrats: All tests passed! (10 points)"
================================================================
"""

# ------------------- Code Implementation -------------------

def integerCubeRootHelper(n, left, right):
    """
    Recursively searches for the integer cube root of n between left and right.
    Pre-conditions: n >= 1, left < right, left^3 < n, right^3 > n.
    """
    cube = lambda x: x * x * x
    assert(n >= 1)
    assert(left < right)
    assert(left >= 0)
    assert(right <= n)          # right يمكن أن يساوي n
    assert(cube(left) < n)      # ثابت: left^3 < n
    assert(cube(right) > n)     # ثابت: right^3 > n

    if left + 1 == right:       # فاصلتان متتاليتان فقط
        return left

    mid = (left + right) // 2
    if cube(mid) < n:
        return integerCubeRootHelper(n, mid, right)
    elif cube(mid) == n:        # وجدنا الجذر التكعيبي الصحيح
        return mid
    else:  # cube(mid) > n
        return integerCubeRootHelper(n, left, mid)

def integerCubeRoot(n):
    """
    Wrapper function for integerCubeRootHelper.
    Finds the integer cube root of positive integer n.
    """
    assert(n > 0)
    if n == 1:
        return 1
    # نجد right بحيث right^3 > n (بالمضاعفة)
    right = 1
    while right ** 3 <= n:
        right *= 2
    left = right // 2
    # نتأكد من أن left^3 < n (في حالة n كان مكعباً كاملاً)
    while left ** 3 >= n:
        left -= 1
    return integerCubeRootHelper(n, left, right)

# ------------------- Test Cases -------------------

if __name__ == "__main__":
    # اختبارات أساسية
    assert(integerCubeRoot(1) == 1)
    assert(integerCubeRoot(2) == 1)
    assert(integerCubeRoot(4) == 1)
    assert(integerCubeRoot(7) == 1)
    assert(integerCubeRoot(8) == 2)
    assert(integerCubeRoot(20) == 2)
    assert(integerCubeRoot(26) == 2)

    # اختبارات نطاقات كاملة للتأكد من صحة الخوارزمية
    for j in range(27, 64):
        assert(integerCubeRoot(j) == 3)
    for j in range(64, 125):
        assert(integerCubeRoot(j) == 4)
    for j in range(125, 216):
        assert(integerCubeRoot(j) == 5)
    for j in range(216, 343):
        assert(integerCubeRoot(j) == 6)
    for j in range(343, 512):
        assert(integerCubeRoot(j) == 7)

    print("Congrats: All tests passed! (10 points)")
