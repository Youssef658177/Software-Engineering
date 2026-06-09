"""
Problem 3: Develop Multiway Merge Algorithm (English & Arabic Explanation)
==========================================================================
1. Problem Statement (English):
-------------------------------
We studied the problem of merging 2 sorted lists lst1 and lst2 into a single sorted list in time O(m + n) where m is the size of lst1 and n is the size of lst2. Let twoWayMerge(lst1, lst2) represent the python function that returns the merged result.

In this problem, we will explore algorithms for merging k different sorted lists, usually represented as a list of sorted lists into a single list.

(A) Suppose we have k lists: lists[0], lists[1], ..., lists[k-1]. For convenience, the size of these lists are all assumed to be the same value n.
We wish to solve multiway merge by merging two lists at a time:
    mergedList = lists[0]
    for i = 1, ..., k-1:
        mergedList = twoWayMerge(mergedList, lists[i])
    return mergedList

Question: Knowing the running time of the twoWayMerge algorithm as mentioned above, what is the overall running time of the algorithm in terms of n, k?

(B) Implement an algorithm that will implement the k-way merge by calling twoWayMerge repeatedly as follows:
    1. Call twoWayMerge on consecutive pairs of lists: twoWayMerge(lists[0], lists[1]), ..., twoWayMerge(lists[k-2], lists[k-1]) (assume k is even).
    2. Thus, we create a new list of lists of size k/2.
    3. Repeat steps 1, 2 until we have a single list left.

(C) What is the overall running time of the algorithm in (B) as a function of n and k?

==========================================================================
2. Explanation (Arabic):
------------------------
المسألة بتطلب دمج k من القوائم المرتبة في قائمة واحدة مرتبة. عندنا دالة twoWayMerge بتدمج قائمتين في وقت O(m+n).

الجزء (A): خوارزمية "الدمج المتسلسل" (Sequential Merge).
- بنبدأ بالقائمة الأولى، ونضيف القائمة الثانية عن طريق twoWayMerge، والناتج ندمجه مع الثالثة، وهكذا.
- السؤال: إيه التعقيد الزمني لطريقة دي بدلالة n و k؟

الجزء (B): خوارزمية "الدمج الزوجي" (Pairwise Merge).
- في كل خطوة، بندمج كل زوج من القوائم (list0 + list1, list2 + list3, ...).
- عدد القوائم بيتقسم على 2 في كل مرة.
- بنكرر لحد ما يتبقى قائمة واحدة.
- المطلوب: تنفيذ الخوارزمية دي.

الجزء (C): إيه التعقيد الزمني لخوارزمية (B) بدلالة n و k؟

==========================================================================
3. Time Complexity Analysis (Parts A & C):
------------------------------------------
(Part A): Sequential Merge
- After merging first 2 lists: O(n + n) = O(2n)
- Merge result (size 2n) with 3rd list (size n): O(2n + n) = O(3n)
- ...
- Final merge: O((k-1)n + n) = O(kn)
- Total: O(n + 2n + 3n + ... + kn) = O(n * (1 + 2 + ... + k)) = O(n * k^2)

(Part C): Pairwise Merge
- At iteration i: number of lists = k / 2^i, size of each list = n * 2^i
- Number of merge operations = k / 2^i
- Time for each merge = O(n * 2^i + n * 2^i) = O(n * 2^i)
- Total work at iteration i = (k / 2^i) * (n * 2^i) = O(k * n)
- Number of iterations = log k
- Overall: O(k * n * log k)

==========================================================================
4. Conceptual Solutions (from Image 4):
---------------------------------------
Problem 3A Solution:
    O(n * k^2)
    Explanation: The overall running time is O(n * (1 + 2 + ... + k)) = O(n * k^2).

Problem 3C Solution:
    O(n * k * log k)
    Explanation: At iteration i, the list of lists has size k/2^i with each element of size n * 2^i.
    The number of merge operations is k/2^i with each merge operation taking O(n * 2^i) time.
    The overall work done at iteration i remains O(k * n). There are O(log k) iterations.
    Therefore, the overall complexity is O(n * k * log k).
==========================================================================
"""

# ------------------- Code Implementation -------------------

def twoWayMerge(lst1, lst2):
    """
    Merge two sorted lists into one sorted list.
    Time: O(len(lst1) + len(lst2))
    Arabic: دمج قائمتين مرتبتين في قائمة واحدة مرتبة.
    """
    i, j = 0, 0
    merged = []
    while i < len(lst1) and j < len(lst2):
        if lst1[i] <= lst2[j]:
            merged.append(lst1[i])
            i += 1
        else:
            merged.append(lst2[j])
            j += 1
    # Append remaining elements
    merged.extend(lst1[i:])
    merged.extend(lst2[j:])
    return merged

def oneStepKWayMerge(list_of_lists):
    """
    Pairwise merge consecutive lists and return a new list of merged lists.
    If odd number of lists, the last list remains untouched.
    Arabic: خطوة واحدة من الدمج الزوجي.
    """
    if len(list_of_lists) <= 1:
        return list_of_lists
    new_list = []
    k = len(list_of_lists)
    for i in range(0, k, 2):
        if i + 1 < k:
            new_list.append(twoWayMerge(list_of_lists[i], list_of_lists[i+1]))
        else:
            # Odd last list remains as is
            new_list.append(list_of_lists[i])
    return new_list

def kWayMerge(list_of_lists):
    """
    Recursively merge all lists using pairwise merging until one list remains.
    Arabic: الدمج الزوجي المتكرر باستخدام recursion.
    """
    if len(list_of_lists) == 0:
        return []
    if len(list_of_lists) == 1:
        return list_of_lists[0]
    new_list_of_lists = oneStepKWayMerge(list_of_lists)
    return kWayMerge(new_list_of_lists)

# ------------------- Test Cases -------------------

if __name__ == "__main__":
    # Test 1
    lst1 = kWayMerge([[1,2,3], [4,5,7], [-2,0,6], [5]])
    assert lst1 == [-2, 0, 1, 2, 3, 4, 5, 5, 6, 7], "Test 1 failed"

    # Test 2
    lst2 = kWayMerge([[-2, 4, 5, 8], [0, 1, 2], [-1, 3, 6, 7]])
    assert lst2 == [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8], "Test 2 failed"

    # Test 3
    lst3 = kWayMerge([[-1, 1, 2, 3, 4, 5]])
    assert lst3 == [-1, 1, 2, 3, 4, 5], "Test 3 failed"

    print('All Tests Passed = 15 points')
