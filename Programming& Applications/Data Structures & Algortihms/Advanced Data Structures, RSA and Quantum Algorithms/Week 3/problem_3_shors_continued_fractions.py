"""
Problem 3: Shor's Algorithm - Continued Fractions & Order Extraction (English & Arabic Explanation)
====================================================================================================
1. Problem Statement (English):
-------------------------------
In this problem, we will explore the continued fraction method to extract the possible order r of a from a measurement meas. We know with high probability that:
    meas / 2^m ≈ j / r
for some natural number j and the order r that we are seeking.

In general, meas / 2^m is a decimal number between [0, 1]. We use the continued fraction approximation to obtain possible values of j / r.

Part A: Write a function `get_continued_fraction(lst)` which given a list of numbers [a0, ..., a_{n-1}] computes the continued fraction:
    1 / (a0 + 1/(a1 + 1/(a2 + ...)))
and returns a pair of integers (a, b) where b != 0.

Part B: Write a function `extract_order(meas, m, a, n)` that extracts the order r of a modulo n from a phase estimation measurement.
- meas: integer measurement outcome (0 <= meas < 2^m)
- m: number of estimation qubits
- a: base integer
- n: modulus
Returns r such that a^r ≡ 1 (mod n), or None if it cannot be found.

====================================================================================================
2. Explanation (Arabic):
------------------------
في خوارزمية شور، بعد إجراء تقدير الطور الكمي (Phase Estimation)، نحصل على قياس `meas`. العلاقة بين هذا القياس والرتبة `r` هي أن الكسر `meas / 2^m` يكون قريباً جداً من الكسر `j / r`، حيث `j` عدد صحيح عشوائي و `r` هو الترتيب الذي نبحث عنه.

**الجزء أ (Continued Fractions):**
لإيجاد الكسر `j / r`، نستخدم خوارزمية الكسور المستمرة (Continued Fractions). هذه الخوارزمية تحول أي عدد عشري إلى سلسلة من الأعداد الصحيحة، وتسمح لنا بإيجاد "تقاربات" (Convergents) تكون أقرب الكسور ذات المقامات الصغيرة للعدد الأصلي. في الكود المرفق، دالة `get_continued_fraction` تحسب قيمة كسر مستمر من معاملاته، ودالة `make_continued_fraction` تحول أي كسر إلى معاملاته.

**الجزء ب (Extract Order):**
بمجرد أن نحصل على كسر تقريبي `p/q`، يكون `q` مرشحاً للرتبة `r`. ولكن قد يكون الكسر `p/q` مختزلاً، وقد تكون الرتبة هي `2q` أو `3q`. لذلك، نقوم باختبار القيم `q`، `2q`، و `3q` (إذا كانت أقل من أو تساوي `n`) للتأكد من أي منها يحقق `a^r ≡ 1 (mod n)`.

====================================================================================================
3. Code Implementation:
-----------------------
"""

# ------------------- Part A: Continued Fractions Helpers -------------------
def get_continued_fraction(lst):
    """
    Evaluate the fraction 1 / (a0 + 1/(a1 + 1/(a2 + ...))) where `lst` = [a0, a1, a2, ...].
    Returns (numerator, denominator) of the resulting simple fraction.
    """
    # Use the standard recurrence for the simple continued fraction [a0; a1, a2, ...]
    # p[-2]=0, p[-1]=1; q[-2]=1, q[-1]=0
    p_prev2, p_prev1 = 0, 1
    q_prev2, q_prev1 = 1, 0

    for a in lst:
        p = a * p_prev1 + p_prev2
        q = a * q_prev1 + q_prev2
        p_prev2, p_prev1 = p_prev1, p
        q_prev2, q_prev1 = q_prev1, q

    # The standard fraction is p_prev1 / q_prev1.
    # We want the reciprocal of that standard fraction because the provided formula starts with 1/(...).
    return (q_prev1, p_prev1)

def make_continued_fraction(a, b):
    """
    Return the continued fraction coefficients of the reciprocal b/a.
    The expansion is [q0, q1, q2, ...] such that
        b/a = q0 + 1/(q1 + 1/(q2 + ...))
    where a > 0 and a <= b.
    """
    assert a > 0
    assert a <= b

    coeffs = []
    while a != 0:
        q = b // a
        r = b % a
        coeffs.append(q)
        b, a = a, r
    return coeffs

# ------------------- Part B: Order Extraction -------------------
def modular_exponentiate(a, k, n):
    """
    Compute (a^k) mod n using exponentiation by squaring.
    """
    mu = a
    res = 1
    while k > 0:
        if k % 2 == 1:
            res = (res * mu) % n   
        mu = (mu * mu) % n
        k = k // 2
    return res

def extract_order(meas, m, a, n):
    """
    Extract the order r of a modulo n from a phase estimation measurement.
    meas: integer measurement outcome (0 <= meas < 2^m)
    m: number of estimation qubits
    a: base integer
    n: modulus
    Returns r such that a^r ≡ 1 (mod n), or None if it cannot be found.
    """
    if meas == 0:
        return None

    N = 2 ** m
    
    # We want the continued fraction of meas / N
    num = meas
    den = N
    
    # Standard convergence recurrence initialization (p_i / q_i)
    p_prev2, p_prev1 = 0, 1
    q_prev2, q_prev1 = 1, 0
    
    while den != 0:
        # Evaluate standard continued fraction coefficient
        a_i = num // den
        rem = num % den
        
        # Step to next fraction element
        num = den
        den = rem
        
        # Compute current convergent fraction elements
        p = a_i * p_prev1 + p_prev2
        q = a_i * q_prev1 + q_prev2
        
        # Shift variables for the next recurrence
        p_prev2, p_prev1 = p_prev1, p
        q_prev2, q_prev1 = q_prev1, q
        
        # q is our candidate r'
        if q > n:
            break # We can stop safely if the denominator exceeds the modulus n
            
        # As per the heuristic: test r', 2r', 3r'
        if q > 0: 
            for multiplier in [1, 2, 3]:
                cand = q * multiplier
                if cand <= n:  # Valid candidate size check
                    if modular_exponentiate(a, cand, n) == 1:
                        return cand

    return None

"""
====================================================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- get_continued_fraction: O(k) حيث k هو طول القائمة المدخلة للكسور المستمرة.
- make_continued_fraction: O(log b) (باستخدام خوارزمية إقليدس).
- extract_order:
    - في كل خطوة من خطوات الكسر المستمر، نتحقق من مقام التقارب (Denominator).
    - الخوارزمية تعمل في وقت O(log N) (حيث N = 2^m)، وهو وقت فعال جداً حتى بالنسبة للقياسات الكبيرة.
====================================================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    print("--- Part A: Continued Fractions Tests ---")
    (n4, d4) = get_continued_fraction([5])
    print(f'Test # 0: {n4}/{d4}')
    assert n4 == 1 and d4 == 5

    (n1, d1) = get_continued_fraction([1,2,2])
    print(f'Test # 1: {n1}/{d1}')
    assert n1 == 5 and d1 == 7

    (n2, d2) = get_continued_fraction([1, 2, 1, 2, 1])
    print(f'Test # 2: {n2}/{d2}')
    assert n2 == 11 and d2 == 15

    (n3, d3) = get_continued_fraction([1,1,1,1,1,1])
    print(f'Test # 3: {n3}/{d3}')
    assert n3 == 8 and d3 == 13

    f1 = make_continued_fraction(197, 1024) 
    print(f'197/1024 = ContinuedFraction({f1})')
    assert f1 == [5, 5, 19, 2]

    f2 = make_continued_fraction(64, 128) 
    print(f'64/128 = ContinuedFraction({f2})')
    assert f2 == [2]

    f3 = make_continued_fraction(1, 1) 
    print(f'1/1 = ContinuedFraction({f3})')
    assert f3 == [1]

    f4 = make_continued_fraction(314157, 1000000)
    print(f'314157/1000000 = ContinuedFraction({f4})')
    assert f4 == [3, 5, 2, 5, 1, 7, 1, 2, 3, 2, 1, 15]
    print("Part A Tests Passed!\n")


    print("--- Part B: Order Extraction Tests ---")
    # Test cases from the prompt
    r1 = extract_order(75, 7, 5, 91)
    assert r1 == 12

    r2 = extract_order(53, 7, 5, 91)
    assert r2 == 12

    r3 = extract_order(96, 7, 5, 91)
    assert r3 == 12

    r4 = extract_order(32, 7, 5, 91)
    assert r4 == 12

    r5 = extract_order(64, 7, 5, 91)
    assert r5 == None

    r6 = extract_order(11, 7, 5, 91)
    assert r6 == 12

    print("Part B Tests Passed!")
    print("All Tests Passed Successfully!")
