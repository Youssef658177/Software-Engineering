"""
Assignment 3: Shor's Algorithm (English & Arabic Explanation)
=============================================================
1. Problem Statement (English):
-------------------------------
In this assignment, we will work through the disparate parts of Shor's algorithm to run through the various parts of the algorithm that were not clearly explored in our lectures.

Suppose we are interested in factoring the number 77 (which we know is 11 × 7) using a quantum computer and choose a = 4 as our number.

We construct the quantum circuit that implements the function f(j) = 10^j mod 77.

(a) What is the order r of 10 modulo 77?
(b) Find a number a whose order modulo 77 is odd.
(c) What factor (if any) of 77 can we extract by knowing the order of 10 modulo 77? Show the steps.
(d) Repeat part (c) for a = 12. Find the order of a modulo 77, check if we can find any prime factors of 77 using the information.
(e) Implement a classical function to find the order of a modulo n where a, n are inputs.

Additionally, we write a function `count_hits(n)` that counts the number of successful runs of Shor's algorithm for a given n.

=============================================================
2. Explanation (Arabic):
------------------------
هذا الواجب يتناول خوارزمية شور (Shor's Algorithm) لتحليل الأعداد إلى عواملها الأولية باستخدام الحوسبة الكمومية.
المسألة تطلب استخدام العدد 77 (الذي يساوي 7 × 11) كنموذج تدريبي للخوارزمية.

**الإجابات النظرية المطلوبة:**
(أ) **رتبة العدد 10 (mod 77):** 
بالحساب: 10^1 = 10, 10^2 = 100 ≡ 23, 10^3 = 230 ≡ 76 ≡ -1, 10^4 = (-1)^2 = 1.
إذن، الرتبة `r` للعدد 10 هي **4**.
(ب) **عدد a رتبته فردية:**
بما أن 77 = 7 × 11، وترتيب أي عنصر في مجموعة الضرب يقسم (7-1)(11-1) = 60. وبما أن 60 عدد زوجي، فإن العنصر الوحيد الذي يمكن أن تكون رتبته فردية هو العنصر المحايد **1**. لذا `a = 1` (أو أي عدد آخر يعطي رتبة 1).
(ج) **استخراج العامل من معرفة رتبة 10:**
بما أن الرتبة `r = 4` (زوجية)، يمكننا حساب `10^(r/2) = 10^2 = 23`.
العامل الأول: `gcd(23 - 1, 77) = gcd(22, 77) = 11`.
العامل الثاني: `gcd(23 + 1, 77) = gcd(24, 77) = 1`. (في هذه الحالة، نحتاج إلى تحليل الناتج الصحيح 11).
(د) **استخراج العامل من معرفة رتبة 12:**
حساب رتبة 12: 12^1=12, 12^2=67, 12^3=34, 12^4=23, 12^5=45, 12^6=1. الرتبة `r = 6` (زوجية).
العامل الأول: `gcd(12^(6/2) - 1, 77) = gcd(12^3 - 1, 77) = gcd(34 - 1, 77) = gcd(33, 77) = 11`.
العامل الثاني: `gcd(34 + 1, 77) = gcd(35, 77) = 7`.
باستخدام a=12 يمكننا إيجاد كلا العاملين (11 و 7) بنجاح.

الجزء البرمجي: تنفيذ دالة `find_order` لإيجاد رتبة أي عدد a mod n، ودالة `count_hits` لحساب عدد محاولات النجاح بناءً على شروط خوارزمية شور.

=============================================================
3. Code Implementation:
-----------------------
"""

# ------------------- Helper Functions -------------------
def gcd(m, n):
    (m, n) = max(m, n), min(m, n)
    assert m > 0
    assert n >= 0
    while n > 0:
        (m, n) = (n, m % n)
    return m

def modular_exponentiate(a, k, n):
    """
    Computes (a^k) mod n efficiently using exponentiation by squaring.
    """
    m = a
    j = 0
    res = 1
    while k > 0:
        if k % 2 == 1:
            res = (res * m) % n
        m = (m * m) % n
        k = k // 2
    return res

# ------------------- Problem 1 (e): find_order -------------------
def find_order(a, n):
    """
    Finds the multiplicative order of a modulo n.
    a: base integer.
    n: modulus.
    Returns: The smallest integer r > 0 such that a^r ≡ 1 (mod n).
    """
    r = 1
    cur = a % n
    while cur != 1:
        cur = (cur * a) % n
        r += 1
    return r

# ------------------- count_hits -------------------
def count_hits(n):
    """
    Counts the number of successful cases for Shor's Algorithm with modulus n.
    Success conditions: 
    1. Order r is even.
    2. a^(r/2) mod n != n - 1 (which means it's not -1 mod n).
    """
    hits = 0
    for a in range(1, n):
        # We only care about numbers that are relatively prime to n
        if gcd(a, n) == 1:
            # 1. Find the multiplicative order 'r' of a modulo n
            r = find_order(a, n)
            
            # 2. Check the Shor's Algorithm success conditions
            if r % 2 == 0:  # Condition 1: order r must be even
                x = modular_exponentiate(a, r // 2, n)
                if x != (n - 1): # Condition 2: a^(r/2) mod n must not equal n-1
                    hits += 1
    return hits

"""
=============================================================
4. Time & Space Complexity Analysis:
------------------------------------
- `gcd`: O(log min(m, n)).
- `modular_exponentiate`: O(log k).
- `find_order`: O(r) in the worst case (where r is the multiplicative order). For small n, this is acceptable.
- `count_hits`: O(n * r * log(n)). In a classical simulation, this is extremely slow for large n, which is why quantum computers are needed to find the period efficiently.
=============================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    # Basic test for find_order
    print(f"Order of 10 mod 77 is: {find_order(10, 77)}")  # Output should be 4
    
    # Tests from the assignment image
    h15 = count_hits(15)
    print(f'count_hits(15) = {h15}')
    assert h15 == 6, f'hits for 15 are 6 (2, 4, 7, 8, 11, 13)'

    h77 = count_hits(77)
    print(f'count_hits(77) = {h77}')
    assert h77 == 30, f'hits for 77 are 30'
    print(f'Note that \varphi(77) = 6 * 10 = 60')
    print(f'Fraction of hits among relatively prime = {h77/(60)}')

    h91 = count_hits(91)
    print(f'count_hits(91) = {h91}')
    assert h91 == 54, f'hits for 91 are 54'

    h111 = count_hits(111)
    print(f'count_hits(111) = {h111}')
    assert h111 == 54, f'hits for 111 are 54'

    h893 = count_hits(893)
    print(f'count_hits(893) = {h893}')
    assert h893 == 414, f'hits for 893 are 414'

    print('All tests passed successfully!')
