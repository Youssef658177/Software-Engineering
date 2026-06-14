"""
Problem 3: Design a Universal Family Hash Function (English & Arabic Explanation)
==================================================================================
1. Problem Statement (English):
-------------------------------
Suppose we are interested in hashing n bit keys into m bit hash values to hash into a table of size 2^m. We view our key as a bit vector of n bits in binary.

The hash family is defined by random boolean matrices H with m rows and n columns. To compute the hash function, we perform a matrix multiplication. The matrix multiplication is carried out using AND for multiplication and XOR instead of addition.

For a given matrix H and two keys x, y that differ only in their i-th bits, provide a condition for Hx = Hy holding.

(A) Provide a condition for Hx = Hy for keys x, y that differ only in their i-th bits.

(B) Prove that the probability that two keys x, y such that x ≠ y collide under the random choice of a matrix x, y is at most 1/2.

================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب تصميم عائلة دوال تجزئة (Hash Function) تعتمد على المصفوفات العشوائية. 
الفكرة:
- يتم تمثيل المفتاح كمتجه بتات (bit vector) بطول n.
- يتم اختيار مصفوفة H بشكل عشوائي بأبعاد m × n.
- يتم حساب قيمة التجزئة بضرب H في المفتاح، باستخدام AND بدلاً من الضرب العادي و XOR بدلاً من الجمع.

الجزء (A): إذا كان المفتاحان x و y يختلفان فقط في البت رقم i، فما هو الشرط الذي يجعل Hx = Hy؟

الجزء (B): أثبت أن احتمال أن يتصادم مفتاحان مختلفان x ≠ y تحت الاختيار العشوائي للمصفوفة H هو على الأكثر 1/2.

================================================================
3. Code Implementation (Part A & B):
------------------------------------
"""

from random import random

def dot_product(lst_a, lst_b):
    """
    Calculate dot product in GF(2) (AND for multiplication, XOR for addition).
    مثال: (0*1) XOR (1*1) XOR (0*1) XOR (1*0) = 0 XOR 1 XOR 0 XOR 0 = 1
    """
    and_list = [elt_a * elt_b for (elt_a, elt_b) in zip(lst_a, lst_b)]
    return 0 if sum(and_list) % 2 == 0 else 1

def matrix_multiplication(H, lst):
    """
    Perform matrix multiplication by taking the dot product of each row in H with the column vector lst.
    Using AND for multiplication and XOR for addition.
    """
    return [dot_product(row, lst) for row in H]

def return_random_hash_function(m, n):
    """
    Generate a random m × n matrix.
    Each entry is chosen as 1 with probability >= 1/2 and 0 with probability < 1/2.
    """
    return [[1 if random() < 0.5 else 0 for _ in range(n)] for _ in range(m)]

"""
================================================================
4. Conceptual Answers (Part A & Part B):
----------------------------------------

Part (A) - Condition for Hx = Hy:
---------------------------------
Let x and y be two keys (bit vectors of length n) that differ only in their i-th bit (0-based indexing).
Let d = x ⊕ y (bitwise XOR). Then d has a 1 only at position i, and 0 elsewhere.
The condition Hx = Hy is equivalent to Hx ⊕ Hy = 0, which simplifies to H(x ⊕ y) = 0 (since matrix multiplication is linear in GF(2)).
Therefore, Hd = 0, where d has a 1 at position i and 0 elsewhere.
This means that the i-th column of H must be a zero vector. So, the condition is:
    Hx = Hy  ⇔  The i-th column of H is all zeros.

Part (B) - Collision Probability:
---------------------------------
We want to prove that for any two distinct keys x and y, the probability that Hx = Hy is at most 1/2.
As shown in Part (A), Hx = Hy ⇔ H(x ⊕ y) = 0.
Let d = x ⊕ y. Since x ≠ y, d is a non-zero vector. Let j be the position where d has a 1.
The j-th column of H, denoted as c_j, is a random vector in GF(2)^m.
The result Hd is a linear combination of the columns of H where d has a 1.
For Hd to be 0, the j-th column c_j must be equal to the sum of the other columns involved.
For a fixed d, the j-th column is independent of the other columns. Since c_j is chosen uniformly at random from GF(2)^m,
the probability that it equals a specific value is 1/2^m.
The probability that Hx = Hy is exactly 1/2^m, which is ≤ 1/2 for any m ≥ 1.
Therefore, the collision probability is at most 1/2.

This confirms the universal hashing property.
================================================================
"""

# ------------------- Test Cases -------------------

if __name__ == "__main__":
    # Test 1: Basic matrix multiplication
    A1 = [[0,1,0,1],[1,0,0,0],[1,0,1,1]]
    b1 = [1,1,1,0]
    c1 = matrix_multiplication(A1, b1)
    print('c1=', c1)
    assert c1 == [1,1,0] , 'Test 1 failed'

    # Test 2: Another multiplication
    A2 = [[1,1],[0,1]]
    b2 = [1,0]
    c2 = matrix_multiplication(A2, b2)
    print('c2=', c2)
    assert c2 == [1, 0], 'Test 2 failed'

    # Test 3: Third multiplication
    A3 = [[1,1,1,0],[0,1,1,0]]
    b3 = [1, 0,0,1]
    c3 = matrix_multiplication(A3, b3)
    print('c3=', c3)
    assert c3 == [1, 0], 'Test 3 failed'

    # Test 4: Random matrix generation (m=5, n=4)
    H = return_random_hash_function(5,4)
    print('H=', H)
    assert len(H) == 5, 'Test 5 failed'
    assert all(len(row) == 4 for row in H), 'Test 6 failed'
    assert all(elt == 0 or elt == 1 for row in H for elt in row ),  'Test 7 failed'

    # Test 5: Random matrix generation (m=6, n=3)
    H2 = return_random_hash_function(6,3)
    print('H2=', H2)
    assert len(H2) == 6, 'Test 8 failed'
    assert all(len(row) == 3 for row in H2),  'Test 9 failed'
    assert all(elt == 0 or elt == 1 for row in H2 for elt in row ), 'Test 10 failed'

    print('Tests passed: 10 points!')
