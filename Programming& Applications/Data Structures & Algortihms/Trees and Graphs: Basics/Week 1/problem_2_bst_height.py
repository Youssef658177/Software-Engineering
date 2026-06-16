"""
Problem 2: Height of Random Binary Search Trees (English & Arabic Explanation)
==============================================================================
1. Problem Statement (English):
-------------------------------
The height of a binary search tree depends on the order in which we insert the keys of the tree.
In this problem, we investigate a curious link between the recursion depth of quicksort algorithm on
an array of n elements and the depth of binary search trees.

Suppose we wish to insert keys the set of keys from {0, ..., n - 1} into a binary search tree.
Answer the questions below:

(A2) Provide examples of insertion sequences such that the resulting tree will have the worst possible height of n.

(B2) Let s1, ..., sj be a sequence of j >= 1 keys inserted, wherein each si is a number between 0 and n-1 and each number in the sequence is unique. Prove that if the sequence yields a tree of height j (worst possible case) then s1 must be the minimum or maximum element in the sequence.

(C2) Using the implementation of the binary search tree in part 1, complete the function calculateAverageDepth(n, numTrials) that performs the following experiment numTrials number of times:
    1. Take a list of numbers from 0 to n-1.
    2. Randomly shuffle the list.
    3. Insert the randomly shuffled list into a tree.
    4. Find and return the depth of the tree.
    5. Run the experiment numTrials times and return the average depth.

==========================================================================
2. Explanation (Arabic):
------------------------
هذه المسألة تدرس العلاقة بين ارتفاع شجرة البحث الثنائي وترتيب إدخال العناصر.

(A2) أسوأ حالة لارتفاع الشجرة (n) تحدث عندما يتم إدخال العناصر بترتيب تصاعدي أو تنازلي، مما يجعل الشجرة تتحول إلى قائمة متصلة (Linked List).

(B2) لإثبات أن العنصر الأول في التسلسل يجب أن يكون العنصر الأصغر أو الأكبر، نستخدم البرهان بالتناقض: إذا كان العنصر الأول ليس الأصغر وليس الأكبر، فسيوجد عناصر في كلا الجانبين (أكبر وأصغر منه)، مما يعني أن الشجرة ستحتوي على شجرتين فرعيتين غير فارغتين، وبالتالي سيكون الارتفاع أقل من n.

(C2) الكود المقدم يقوم بتنفيذ التجربة المطلوبة: إنشاء قائمة عشوائية، إدخالها في شجرة، حساب الارتفاع، وتكرار ذلك numTrials مرة لحساب المتوسط.

==========================================================================
3. Conceptual Answers (Part A2 & Part B2):
------------------------------------------
(A2) Examples of insertion sequences yielding worst case height n:
    - Increasing order: [0, 1, 2, 3, ..., n-1]
    - Decreasing order: [n-1, n-2, n-3, ..., 0]
    - Any sequence where each new element becomes either the new maximum or the new minimum.

(B2) Proof by contradiction:
    - Assume that s1 is neither the minimum nor the maximum element in the sequence.
    - This means there exists at least one element smaller than s1 (call it x) and at least one element larger than s1 (call it y) in the sequence.
    - Since s1 is inserted first, it becomes the root of the tree.
    - All smaller elements (including x) go to the left subtree of s1.
    - All larger elements (including y) go to the right subtree of s1.
    - Both left and right subtrees will be non-empty.
    - The height of the tree = 1 + max(height(left), height(right)).
    - Since both subtrees are non-empty, the maximum possible height is n-1 (if one subtree has height n-2 and the other has height 0).
    - Therefore, the height cannot be n (worst case).
    - This contradicts the assumption that the sequence yields a tree of height n.
    - Hence, s1 must be either the minimum or the maximum element in the sequence.

==========================================================================
4. Code Implementation (Part C2):
---------------------------------
"""

import random
from matplotlib import pyplot as plt
import math

# --- NOTE: The following class Node must be present for this code to work ---
# class Node: (from Part 1) -- assumed to be defined earlier

def run_single_experiment(n):
    """
    1. Make a list of numbers from 0 to n-1.
    2. Randomly shuffle the list.
    3. Insert the random list elements in order into a tree.
    4. Return the height of the resulting tree.
    """
    numbers = list(range(n))
    random.shuffle(numbers)
    
    if n == 0:
        return 0
    root = Node(numbers[0])
    for num in numbers[1:]:
        root.insert(num)
    return root.height()

def run_multiple_trials(n, numTrials):
    """
    Runs the experiment numTrials times.
    Returns (Average Depth, List of Depths).
    """
    lst_of_depths = [run_single_experiment(n) for _ in range(numTrials)]
    return (sum(lst_of_depths) / len(lst_of_depths), lst_of_depths)

def calculateAverageDepth(n, numTrials):
    """Wrapper function to return only the average depth."""
    avg, _ = run_multiple_trials(n, numTrials)
    return avg

"""
==========================================================================
5. Time Complexity Analysis:
----------------------------
- run_single_experiment(n): O(n log n) on average, O(n^2) in worst case (when tree becomes a chain).
- run_multiple_trials(n, numTrials): O(numTrials * n log n) on average.
- calculateAverageDepth(n, numTrials): Same as run_multiple_trials.

Theoretical average depth of a randomly built BST:
    E[depth] ≈ 2 log2(n) ≈ 1.39 log2(n) + O(1)
(This is why the average depth for n=64 is around 11-12 and for n=128 is around 14-15)
==========================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    print("Running experiments...")
    
    # Experiment 1: n = 64
    (avg64, lst_of_results_64) = run_multiple_trials(64, 1000)
    plt.hist(lst_of_results_64)
    plt.xlim(0, 64)
    plt.xlabel('Depth of Tree')
    plt.ylabel('Frequency')
    plt.title('Histogram of depths for n = 64')
    print(f'Average depth for 64 = {avg64}')
    assert avg64 <= 12 and avg64 >= 8, "Average depth for n=64 should be between 8 and 12"
    plt.show()

    # Experiment 2: n = 128
    plt.figure()
    (avg128, lst_of_results_128) = run_multiple_trials(128, 1000)
    print(f'Average depth for 128 = {avg128}')
    assert avg128 <= 16 and avg128 >= 12, "Average depth for n=128 should be between 12 and 16"
    
    plt.hist(lst_of_results_128)
    plt.xlim(0, 128)
    plt.xlabel('Depth of Tree')
    plt.ylabel('Frequency')
    plt.title('Histogram of depths for n = 128')
    plt.show()

    # Experiment 3: Average depth as a function of n
    nmin, nmax = 16, 64
    lst_of_average_depths = [run_multiple_trials(j, 1000)[0] for j in range(nmin, nmax)]
    
    plt.figure()
    plt.plot(range(nmin, nmax), lst_of_average_depths, label='Avg. Depth')
    plt.plot(range(nmin, nmax), [1.6 * math.log(j) / math.log(2) for j in range(nmin, nmax)], '--r', label='1.6 log2(n)')
    plt.plot(range(nmin, nmax), [2.2 * math.log(j) / math.log(2) for j in range(nmin, nmax)], '--b', label='2.2 log2(n)')
    plt.xlabel('n')
    plt.ylabel('depth')
    plt.title('Average depth as a function of n')
    plt.legend()
    plt.show()
    
    print('Passed all tests -- 15 points')
