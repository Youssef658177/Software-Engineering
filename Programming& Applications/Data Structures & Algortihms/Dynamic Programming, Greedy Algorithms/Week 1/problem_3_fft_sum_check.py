"""
Problem 3: Sum Existence Check using FFT (English & Arabic Explanation)
=======================================================================
1. Problem Statement (English):
-------------------------------
We are given three subsets of numbers A, B, C ⊆ {0, ..., n}. Design an algorithm that runs in worst case time Θ(n log n) that checks if there exists numbers n1 in A, n2 in B respectively and n3 in C such that n1 + n2 = n3.

Hint: Convert the set A = {n0, n1, ..., nk} into the polynomial p_A(x) = x^{n0} + x^{n1} + ... + x^{nk}. Suppose p_A(x), p_B(x) are polynomials obtained from the sets A, B respectively, interpret what the product p_A(x) × p_B(x) signifies. Use this to complete an algorithm for the problem at hand that runs in n log n time.

=======================================================================
2. Explanation (Arabic):
------------------------
المسألة بتسأل: هل فيه رقم في المجموعة A ورقم في المجموعة B مجموعهم بيعطينا رقم موجود في المجموعة C؟
الحل بيعتمد على تمثيل المجموعات كـ "كثيرات حدود" (Polynomials) وضربهم باستخدام FFT:

1. بننشئ متجهين `a_coeffs` و `b_coeffs` طولهم `n` (حيث n هو أقصى رقم ممكن).
2. لو الرقم `val` موجود في المجموعة A، بنحط `a_coeffs[val] = 1`. (نفس الكلام للمجموعة B).
3. بنضرب المتجهين باستخدام دالة `polynomial_multiply` (اللي بتستخدم FFT).
4. معامل (Coefficient) الـ `x^k` في الناتج بيمثل "عدد الطرق" اللي ممكن نكون بيها الرقم `k` عن طريق جمع رقم من A ورقم من B.
5. أخيراً بنمر على أرقام المجموعة C ونتأكد إن معاملها في الناتج أكبر من 0.5 (عشان نتخلص من أخطاء الفاصلة العائمة).

=======================================================================
3. Code Implementation:
-----------------------
"""
# ملاحظة: الكود ده بيعتمد على دالة `polynomial_multiply` من Problem 2
# لازم تكون معرفة في نفس الملف عشان الكود يشتغل.

def check_sum_exists(a, b, c, n):
    a_coeffs = [0] * n
    b_coeffs = [0] * n 
    
    # 1. Convert sets a and b into coefficient vectors
    # The coefficient of x^k in the polynomial is 1 if k is in the set, and 0 otherwise
    for val in a:
        a_coeffs[val] = 1
    for val in b:
        b_coeffs[val] = 1
    
    # 2. Multiply them together using FFT
    # The coefficient of x^k in the product represents the number of ways
    # to form k as a sum of an element from a and an element from b.
    c_coeffs = polynomial_multiply(a_coeffs, b_coeffs)
    
    # 3. Use the result to solve the problem
    # Check if any element in set c has a non-zero coefficient in the product
    for val in c:
        # Check > 0.5 to account for floating-point precision errors
        if c_coeffs[val] > 0.5: 
            return True
    
    return False

"""
=======================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: Θ(n log n)
  - تحويل المجموعات إلى مصفوفات: O(n)
  - ضرب كثيرات الحدود باستخدام FFT: O(n log n)
  - التحقق من النتيجة: O(n) (حجم المجموعة C)
- Space Complexity: O(n)
  - لتخزين المصفوفات `a_coeffs` و `b_coeffs` و `c_coeffs`.
=======================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    # Test 1
    print('-- Test 1 --')
    a = set([1, 2, 10, 11])
    b = set([2, 5, 8, 10])
    c = set([1, 2, 5, 8])
    assert not check_sum_exists(a, b, c, 12), f'Failed Test 1: your code returned true when the expected answer is false'
    print('Passed')

    # Test 2
    print('-- Test 2 --')
    a = set([1, 2, 10, 11])
    b = set([2, 5, 8, 10])
    c = set([1, 2, 5, 8, 11])
    assert check_sum_exists(a, b, c, 12), f'Failed Test 2: your code returns false but note that 1 in a + 10 in b = 11 in c '
    print('Passed')

    # Test 3
    print('-- Test 3 --')
    a={1, 4, 5, 7, 11, 13, 14, 15, 17, 19, 22, 23, 24, 28, 34, 35, 37, 39, 42, 44}
    b={0, 1, 4, 9, 10, 11, 12, 15, 18, 20, 25, 31, 34, 36, 38, 40, 43, 44, 47, 49}
    c={3, 4, 5, 7, 8, 10, 19, 20, 21, 24, 31, 35, 36, 37, 38, 39, 42, 44, 46, 49}
    assert check_sum_exists(a, b, c, 50), f'Failed Test 3: your code returns False whereas the correct answer is true eg., 4 + 0 = 4'
    print('Passed')

    # Test 4
    print('-- Test 4 --')
    a={98, 2, 99, 40, 77, 79, 87, 88, 89, 27}
    b={64, 66, 35, 69, 70, 40, 76, 45, 12, 60}
    c={36, 70, 10, 44, 15, 16, 83, 20, 84, 55}
    assert not check_sum_exists(a, b, c, 100), f'Failed Test 4: your code returns True whereas the correct answer is False'

    print('All Tests Passed (15 points)!')
