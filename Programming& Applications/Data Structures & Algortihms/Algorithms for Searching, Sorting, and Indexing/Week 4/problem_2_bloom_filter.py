"""
Problem 2: Using a Bloom Filter to Count Common Words (English & Arabic Explanation)
====================================================================================
1. Problem Statement (English):
-------------------------------
In this problem, we will implement a Bloom filter to count how many elements of
longer_words_wp (the words of length 5 or more in War and Peace) appear in the
Great-Gatsby novel.

To do so, we will do the following:
    1. Instantiate a Bloom filter with number of bits n and number of hash functions k.
    2. Insert all words from great-gatsby into the filter.
    3. For each word from war and peace, check membership in the Bloom filter and count the number of "yes" answers.

================================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب استخدام Bloom Filter لحساب عدد الكلمات المشتركة (التي تظهر في الروايتين) بطريقة تقريبية سريعة.

الفكرة الأساسية:
1. إنشاء Bloom Filter بعدد بتات `n` وعدد دوال هاش `k`.
2. إدخال كل كلمات رواية "Great Gatsby" في الفلتر.
3. المرور على كلمات رواية "War and Peace" والتحقق من وجود كل كلمة في الفلتر.
4. عد الكلمات التي يجيب الفلتر عليها بـ "نعم" (True).

النتيجة: عدد تقريبي للكلمات المشتركة، وهو دائماً أكبر من أو يساوي العدد الحقيقي (لأن Bloom Filter يعطي إجابات إيجابية كاذبة إيجابية False Positives، لكن لا يعطي إجابات سلبية كاذبة False Negatives).

================================================================================
3. Code Implementation:
-----------------------
"""

class BloomFilter:
    def __init__(self, nbits, nhash):
        self.bits = [False] * nbits  # Initialize all bits to false
        self.m = nbits
        self.k = nhash
        # Get k random hash functions
        self.hash_fun_reps = [get_random_hash_function() for _ in range(self.k)]

    # Function to insert a word in a Bloom filter.
    def insert(self, word):
        # Step 1: Loop through each hash function
        for hf in self.hash_fun_reps:
            # Step 2: Hash the word and take modulo m
            idx = hash_string(hf, word) % self.m
            # Step 3: Set the bit at that index to True
            self.bits[idx] = True

    # Check if a word belongs to the Bloom Filter
    def member(self, word):
        # Step 1: Loop through each hash function
        for hf in self.hash_fun_reps:
            # Step 2: Hash the word and take modulo m
            idx = hash_string(hf, word) % self.m
            # Step 3: If any bit is False, the word is NOT in the filter
            if not self.bits[idx]:
                return False
        # Step 4: If all bits are True, the word is PROBABLY in the filter
        return True

"""
================================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Space Complexity: O(n) where n is the number of bits in the Bloom filter.
- Time Complexity (insert/member): O(k) where k is the number of hash functions.
================================================================================
"""

# ======================================================================
# NOTE: To run the code below, ensure the variables longer_words_gg and
# longer_words_wp are already defined from the previous assignment code.
# If you are testing locally without loading the text files, you can
# uncomment the lines below to create dummy data for testing.
# ======================================================================
# longer_words_gg = ["hello", "world", "hello", "python", "test"]
# longer_words_wp = ["hello", "java", "python", "ruby", "world"]

# --- Exact Count (Using Python Set) ---
all_words_gg = set(longer_words_gg)
exact_common_wc = 0
for word in longer_words_wp:
    if word in all_words_gg:
        exact_common_wc += 1
print(f"Exact common word count = {exact_common_wc}")

# --- Approximate Count (Using Bloom Filter) ---
bf = BloomFilter(100000, 5)  # 100,000 bits, 5 hash functions
for word in longer_words_gg:
    bf.insert(word)

# Sanity check: All words inserted should be recognized as members
for word in longer_words_gg:
    assert bf.member(word), f"Word: {word} should be a member"

common_word_count = 0
for word in longer_words_wp:
    if bf.member(word):
        common_word_count += 1

print(f"Number of common words of length >= 5 equals : {common_word_count}")
assert common_word_count >= exact_common_wc, "Approximate count should be >= exact count"
print("All Tests Passed: 10 points")
