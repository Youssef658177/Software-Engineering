"""
Assignment 4: Count-Min Sketch & Bloom Filter
================================================================================
1. Problem Statement (English):
-------------------------------
In this assignment, we will explore count-min sketches and bloom filters. We will use two text files:
- great-gatsby-fitzgerald.txt
- war-and-peace-tolstoy.txt

We will explore two tasks:
1. Counting the frequency of words of length 5 or more in both novels using a count-min sketch.
2. Using a bloom filter to approximately count how many words in the War and Peace novel already appear in the Great Gatsby.

Step 1: Making a Universal Hash Family (Already Done For You)
-------------------------------------------------------------
We will use a family of hash functions that first starts by:
(a) Generating a random prime number p (using the Miller-Rabin primality test).
(b) Generating random numbers a, b between 2 and p-1.

The hash function is:  h_{a,b,p}(n) = (a * n + b) mod p
To hash strings, we first use Python's built-in hash function and then apply h_{a,b,p} on the result.

Step 2: Universal Hash Families (Provided Functions)
----------------------------------------------------
- get_random_hash_function(): Generate triple (p, a, b) at random.
- hashfun(hfun_rep, num): Apply the random hash function on a number num.
- hash_string(hfun_rep, hstr): Apply the hash function on a string hstr.

Step 3: Loading Data
--------------------
Load two text files and filter words of length >= 5.

Step 4: Count-Min Sketch Implementation
----------------------------------------
Implement CountMinSketch class with:
- increment(word): Increment the count for a given word.
- approximateCount(word): Get the approximate count for a given word.

Step 5: Test the implementation
-------------------------------
Run tests on Great Gatsby and War and Peace data.

================================================================================
2. شرح المسألة بالعربي (Arabic Explanation):
-------------------------------------------
هذا الواجب يتطلب تنفيذ هيكل بيانات Count-Min Sketch لتقدير تكرار الكلمات في نصوص طويلة (روايات) بكفاءة عالية باستخدام دوال هاش عشوائية.

الخوارزمية (Count-Min Sketch) تعتمد على ثلاث خطوات رئيسية:
1. تهيئة عدة مصفوفات عدادات (Counters) مع دوال هاش مختلفة لكل مصفوفة.
2. عند إضافة كلمة، يتم حساب قيمة الهاش لكل مصفوفة وزيادة العداد المقابل.
3. عند تقدير تكرار كلمة، يتم أخذ القيمة الصغرى (Minimum) عبر كل المصفوفات.

هذا الأسلوب يقلل التصادمات ويعطي تقديراً دقيقاً مع ضمان أن التقدير يكون دائماً أكبر من أو يساوي القيمة الحقيقية (Upper Bound).

================================================================================
3. Code Implementation:
-----------------------
"""
# ============================== IMPORTS ==============================
import random
import matplotlib.pyplot as plt

# ============================== MILLER-RABIN PRIMALITY TEST ==============================
def power(x, y, p):
    """Calculate (x^y) % p efficiently."""
    res = 1
    x = x % p
    while y > 0:
        if y & 1:
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p
    return res

def miillerTest(d, n):
    """Miller-Rabin test for one random base a."""
    a = 2 + random.randint(1, n - 4)
    x = power(a, d, n)
    if x == 1 or x == n - 1:
        return True
    while d != n - 1:
        x = (x * x) % n
        d *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False

def isPrime(n, k):
    """Miller-Rabin primality test with k iterations."""
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    d = n - 1
    while d % 2 == 0:
        d //= 2
    for _ in range(k):
        if not miillerTest(d, n):
            return False
    return True

# ============================== UNIVERSAL HASH FAMILY ==============================
def get_random_hash_function():
    """Generate a random triple (p, a, b) where p is prime and a, b are between 2 and p-1."""
    n = random.getrandbits(64)
    if n < 0:
        n = -n
    if n % 2 == 0:
        n += 1
    while not isPrime(n, 20):
        n += 1
    a = random.randint(2, n - 1)
    b = random.randint(2, n - 1)
    return (n, a, b)

def hashfun(hfun_rep, num):
    """Apply hash function on a number: (a * num + b) mod p."""
    (p, a, b) = hfun_rep
    return (a * num + b) % p

def hash_string(hfun_rep, hstr):
    """Apply hash function on a string using Python's built-in hash."""
    n = hash(hstr)
    return hashfun(hfun_rep, n)

# ============================== DATA LOADING ==============================
def load_text(filename):
    """Load a text file and return all words of length >= 5."""
    with open(filename, 'r', encoding='utf-8') as file:
        txt = file.read()
    txt = txt.replace('\n', ' ')
    words = txt.split(' ')
    return list(filter(lambda s: len(s) >= 5, words))

# ============================== COUNT-MIN SKETCH ==============================
class CountMinSketch:
    """Single bank of counters with one hash function."""
    def __init__(self, num_counters):
        self.m = num_counters
        self.hash_fun_rep = get_random_hash_function()
        self.counters = [0] * self.m

    def increment(self, word):
        """Increment the count for a word."""
        h_val = hash_string(self.hash_fun_rep, word)
        idx = h_val % self.m
        self.counters[idx] += 1

    def approximateCount(self, word):
        """Get the approximate count for a word."""
        h_val = hash_string(self.hash_fun_rep, word)
        idx = h_val % self.m
        return self.counters[idx]

def initialize_k_counters(k, m):
    """Initialize k different CountMinSketch instances."""
    return [CountMinSketch(m) for _ in range(k)]

def increment_counters(count_min_sketches, word):
    """Increment all counters in the list with the given word."""
    for cms in count_min_sketches:
        cms.increment(word)

def approximate_count(count_min_sketches, word):
    """Get the approximate count by taking the minimum over all banks."""
    return min(cms.approximateCount(word) for cms in count_min_sketches)

# ============================== TEST CASES ==============================
if __name__ == "__main__":
    print("=" * 70)
    print("Assignment 4: Count-Min Sketch Tests")
    print("=" * 70)

    # ------------------------------
    # Part 1: Great Gatsby
    # ------------------------------
    print("\n1. Loading Great Gatsby text...")
    longer_words_gg = load_text('great-gatsby-fitzgerald.txt')
    print(f"   Number of words (length >= 5): {len(longer_words_gg)}")

    # Compute exact frequencies
    word_freq_gg = {}
    for elt in longer_words_gg:
        word_freq_gg[elt] = word_freq_gg.get(elt, 0) + 1
    print(f"   Unique words: {len(word_freq_gg)}")

    # Count-Min Sketch implementation
    print("\n2. Running Count-Min Sketch on Great Gatsby...")
    cms_list = initialize_k_counters(5, 1000)
    for word in longer_words_gg:
        increment_counters(cms_list, word)

    # Measure discrepancies
    discrepancies = []
    for word in longer_words_gg:
        estimated = approximate_count(cms_list, word)
        actual = word_freq_gg[word]
        assert estimated >= actual, f"Estimated count ({estimated}) < actual count ({actual})"
        discrepancies.append(estimated - actual)

    # Histogram of discrepancies
    plt.figure()
    plt.hist(discrepancies, bins=20)
    plt.title('Great Gatsby: Discrepancies (Estimated - Actual)')
    plt.xlabel('Difference')
    plt.ylabel('Frequency')
    plt.show()

    max_disc = max(discrepancies)
    assert max_disc <= 200, f"Largest discrepancy = {max_disc} > 200. Check implementation."
    print(f"   Passed! Largest discrepancy = {max_disc} (<= 200)")

    # ------------------------------
    # Part 2: War and Peace
    # ------------------------------
    print("\n3. Loading War and Peace text...")
    longer_words_wp = load_text('war-and-peace-tolstoy.txt')
    print(f"   Number of words (length >= 5): {len(longer_words_wp)}")

    word_freq_wp = {}
    for elt in longer_words_wp:
        word_freq_wp[elt] = word_freq_wp.get(elt, 0) + 1
    print(f"   Unique words: {len(word_freq_wp)}")

    print("\n4. Running Count-Min Sketch on War and Peace...")
    cms_list = initialize_k_counters(5, 5000)
    for word in longer_words_wp:
        increment_counters(cms_list, word)

    discrepancies = []
    for word in longer_words_wp:
        estimated = approximate_count(cms_list, word)
        actual = word_freq_wp[word]
        assert estimated >= actual, f"Estimated count ({estimated}) < actual count ({actual})"
        discrepancies.append(estimated - actual)

    plt.figure()
    plt.hist(discrepancies, bins=20)
    plt.title('War and Peace: Discrepancies (Estimated - Actual)')
    plt.xlabel('Difference')
    plt.ylabel('Frequency')
    plt.show()

    print("   Passed! All assertions satisfied.")
    print("\n" + "=" * 70)
    print("All tests passed: 15 points")
    print("=" * 70)

"""
================================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Space Complexity: O(k * m) where k is the number of hash functions (banks) and m is the number of counters per bank.
- Time Complexity (increment/approximateCount): O(k) per operation because we iterate over the k banks.
================================================================================
"""
