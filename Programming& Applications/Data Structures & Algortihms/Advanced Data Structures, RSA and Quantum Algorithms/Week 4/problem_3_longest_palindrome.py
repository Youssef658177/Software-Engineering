"""
Problem 3: Longest Palindrome Substring (English & Arabic Explanation)
=======================================================================
1. Problem Statement (English):
-------------------------------
Given a string s of length n, find the longest palindrome that is a substring of s in time O(|s|).
You may use copy over the implementation of Ukkonen's algorithm from the notes compute the suffix trie for s or the method from the previous problem even though it takes O(|s|^2).

In this solution, we implement the "Expand Around Center" algorithm which runs in O(n^2) time and O(1) space. 
For each index `i`, we consider two cases:
1. Odd length palindrome: The center is `i` itself.
2. Even length palindrome: The center is between `i` and `i+1`.
We expand outwards from these centers while the characters on both sides are equal, and keep track of the longest one found.

=======================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب إيجاد أطول سلسلة فرعية متناظرة (Palindrome) داخل سلسلة نصية معينة.

الخوارزمية المستخدمة هنا هي **"التوسع حول المركز" (Expand Around Center)**:
- الفكرة بسيطة جداً: أي سلسلة متناظرة لها مركز. هذا المركز قد يكون حرفاً واحداً (في حالة السلاسل ذات الطول الفردي، مثل "ABA")، أو نقطة بين حرفين (في حالة السلاسل ذات الطول الزوجي، مثل "ABBA").
- نقوم بالمرور على كل حرف في السلسلة `s` (ليكن مؤشره `i`).
- نوسع من المركز `i` في الاتجاهين (يسار ويمين) طالما أن الحروف متطابقة، ونسجل طول السلسلة المتناظرة الناتجة.
- نكرر نفس العملية للمركز بين `i` و `i+1`.
- نقوم بتحديث السلسلة الأطول التي نجدها أثناء العملية.

التعقيد الزمني للخوارزمية هو `O(n^2)` لأننا نمر على كل حرف (n مرة)، وفي أسوأ الحالات قد نوسع `n` مرة لكل حرف (كما في حالة كل الحروف متشابهة). التعقيد المكاني هو `O(1)` لأننا لا نستخدم مصفوفات إضافية.

=======================================================================
3. Code Implementation:
-----------------------
"""

def find_longest_palindrome(s):
    """
    Finds the longest palindromic substring in a string `s` using Expand Around Center.
    If the string ends with a '$' symbol (used in suffix trie problems), it is removed first.
    """
    # Remove the trailing '$' if present to avoid it affecting palindrome detection
    if s.endswith('$'):
        s = s[:-1]
        
    if not s:
        return ""
        
    longest = ""
    
    # Helper function to expand around a given center
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # Return the palindrome found (excluding the mismatched boundaries)
        return s[left + 1:right]

    for i in range(len(s)):
        # Case 1: Odd length palindromes (center is a single character)
        p1 = expand_around_center(i, i)
        if len(p1) > len(longest):
            longest = p1
            
        # Case 2: Even length palindromes (center is between two characters)
        p2 = expand_around_center(i, i + 1)
        if len(p2) > len(longest):
            longest = p2
            
    return longest

"""
=======================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: O(n^2)
  - The outer loop runs `n` times.
  - In the worst case (e.g., "aaaa..."), the inner expansion loop can run up to `O(n)` for each `i`.
  - Therefore, the overall time complexity is O(n^2).

- Space Complexity: O(1)
  - The algorithm uses only a few constant-space variables (`longest`, `left`, `right`, `p1`, `p2`).
  - It does not allocate any additional arrays or tables proportional to `n` (unlike DP approaches).
=======================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    # Test 1
    t = find_longest_palindrome("ABRACADABRA$")
    print(f"Result 1: {t}")
    assert t == "ADA" or t == "ACA", "Test 1 failed"

    # Test 2
    t = find_longest_palindrome("MALAYALAM$")
    print(f"Result 2: {t}")
    assert t == "MALAYALAM", "Test 2 failed"

    # Test 3
    t = find_longest_palindrome("ABCDCAB$")
    print(f"Result 3: {t}")
    assert t == "CDC", "Test 3 failed"

    # Test 4
    t = find_longest_palindrome("ACAGCGACTTAGGCAGACTGGGGGTCAGCGATTGAGGCA$")
    print(f"Result 4: {t}")
    assert len(t) == 13, "Test 4 failed: Length mismatch"
    assert t == "GACTGGGGGTCAG", f"Test 4 failed: Expected 'GACTGGGGGTCAG', got '{t}'"

    print("\nجميع الاختبارات تم اجتيازها بنجاح! (All tests passed successfully!) 🎉")
