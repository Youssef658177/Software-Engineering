"""
Problem 2: Heap data structure to maintain/extract median (instead of minimum/maximum key) (English & Arabic Explanation)
============================================================================================================================
1. Problem Statement (English):
-------------------------------
We have seen how min-heaps can efficiently extract the smallest element and maintain the least element as we insert/delete elements. Similarly, max-heaps can maintain the largest element. In this exercise, we combine both to maintain the "median" element of a list of numbers.

The median is the middle element of a list of numbers:
- If the list has size n where n is odd, the median is the (n-1)/2-th element (where 0-th is least and n-1-th is maximum).
- If n is even, we designate the median as the average of the (n/2 - 1)-th and (n/2)-th elements.

We maintain the data using two heaps, H_min and H_max:
- H_min is a min-heap (stores the larger half).
- H_max is a max-heap (stores the smaller half).
- Invariant: max(H_max) <= min(H_min).
- Size invariant: Sizes of H_max and H_min are either equal or H_max has one more element than H_min.

(A) Design algorithm for insertion: 
    Describe the algorithm to insert an element e and how to maintain the size balance condition.

(B) Design algorithm for finding the median:
    Implement an algorithm for finding the median given the heaps H_min and H_max. What is its complexity?

(C) Implement the algorithm: Complete the implementation for maxheap and create the MedianMaintainingHeap class.

==========================================================================
2. Explanation (Arabic):
------------------------
المسألة بتطلب تصميم خوارزمية للحفاظ على "الوسيط" (Median) باستخدام كومتين:
1. Max-Heap (H_max): بيحفظ النصف الأصغر من الأرقام.
2. Min-Heap (H_min): بيحفظ النصف الأكبر من الأرقام.
الشرط الأساسي: أكبر عنصر في H_max <= أصغر عنصر في H_min.

الجزء (A): خوارزمية الإدخال (Insertion).
- نقارن العنصر الجديد مع أكبر عنصر في H_max (أو أصغر عنصر في H_min).
- نضيفه في الكومة المناسبة، وبعدين نعدل الحجم عشان يتحقق الشرط (H_max حجمها = H_min حجمها أو H_max أكبر بواحد).

الجزء (B): إيجاد الوسيط (Finding the Median).
- لو عدد العناصر فردي (H_max أكبر): الوسيط هو `max_element` في H_max.
- لو عدد العناصر زوجي (الحجم متساوي): الوسيط هو متوسط أكبر عنصر في H_max وأصغر عنصر في H_min.
- التعقيد الزمني: O(1).

==========================================================================
3. Algorithm Explanations:
--------------------------
(A) Insertion Algorithm:
    1. If H_max is empty or e <= H_max.max_element(): Insert e into H_max.
       Else: Insert e into H_min.
    2. Re-balance the sizes:
       - If H_max.size() > H_min.size() + 1: Move H_max.max_element() to H_min.
       - If H_min.size() > H_max.size(): Move H_min.min_element() to H_max.

(B) Finding the Median Algorithm:
    1. If H_max.size() > H_min.size(): Return H_max.max_element().
    2. Else (sizes are equal): Return (H_max.max_element() + H_min.min_element()) / 2.0.
    Complexity: O(1) (Direct heap access).

==========================================================================
4. Code Implementation (MaxHeap + MinHeap + MedianMaintainingHeap):
-------------------------------------------------------------------
"""

class MaxHeap:
    """MaxHeap Implementation (Provided by user, complete)."""
    def __init__(self):
        self.H = [None]
        
    def size(self):
        return len(self.H)-1
    
    def __repr__(self):
        return str(self.H[1:])
        
    def satisfies_assertions(self):
        for i in range(2, len(self.H)):
            assert self.H[i] <= self.H[i//2], f'Maxheap property fails at position {i//2}, parent elt: {self.H[i//2]}, child elt: {self.H[i]}'
    
    def max_element(self):
        return self.H[1]
    
    def bubble_up(self, index):
        if index == 1:
            return
        parent_index = index // 2
        if self.H[parent_index] >= self.H[index]:
            return
        self.H[parent_index], self.H[index] = self.H[index], self.H[parent_index]
        self.bubble_up(parent_index)
            
    def bubble_down(self, index):
        left_child = 2 * index
        right_child = 2 * index + 1
        left_val = self.H[left_child] if left_child < len(self.H) else -float('inf')
        right_val = self.H[right_child] if right_child < len(self.H) else -float('inf')
        if self.H[index] >= max(left_val, right_val):
            return
        max_child_val, max_child_index = max((left_val, left_child), (right_val, right_child))
        self.H[index], self.H[max_child_index] = self.H[max_child_index], self.H[index]
        self.bubble_down(max_child_index)
    
    def insert(self, elt):
        self.H.append(elt)
        self.bubble_up(len(self.H) - 1)
        
    def delete_max(self):
        if self.size() == 0:
            return
        self.H[1], self.H[-1] = self.H[-1], self.H[1]
        max_val = self.H.pop()
        if self.size() > 0:
            self.bubble_down(1)
        return max_val


class MinHeap:
    """MinHeap Implementation (Based on previous problems)."""
    def __init__(self):
        self.H = [None]
 
    def size(self):
        return len(self.H)-1
    
    def __repr__(self):
        return str(self.H[1:])
        
    def satisfies_assertions(self):
        for i in range(2, len(self.H)):
            assert self.H[i] >= self.H[i//2], f'Min heap property fails at position {i//2}, parent elt: {self.H[i//2]}, child elt: {self.H[i]}'
    
    def min_element(self):
        return self.H[1]

    def bubble_up(self, index):
        if index == 1: 
            return 
        parent_index = index // 2
        if self.H[parent_index] < self.H[index]:
            return 
        self.H[parent_index], self.H[index] = self.H[index], self.H[parent_index]
        self.bubble_up(parent_index)
    
    def bubble_down(self, index):
        lchild_index = 2 * index
        rchild_index = 2 * index + 1
        lchild_value = self.H[lchild_index] if lchild_index < len(self.H) else float('inf')
        rchild_value = self.H[rchild_index] if rchild_index < len(self.H) else float('inf')
        if self.H[index] <= min(lchild_value, rchild_value):
            return 
        min_child_value, min_child_index = min((lchild_value, lchild_index), (rchild_value, rchild_index))
        self.H[index], self.H[min_child_index] = self.H[min_child_index], self.H[index]
        self.bubble_down(min_child_index)
        
    def insert(self, elt):
        self.H.append(elt)
        self.bubble_up(len(self.H) - 1)
        
    def delete_min(self):
        if self.size() == 0:
            return
        self.H[1], self.H[-1] = self.H[-1], self.H[1]
        min_val = self.H.pop()
        if self.size() > 0:
            self.bubble_down(1)
        return min_val


class MedianMaintainingHeap:
    """Maintains the median using two heaps (MaxHeap for lower half, MinHeap for upper half)."""
    
    def __init__(self):
        self.H_max = MaxHeap() # Stores the smaller half
        self.H_min = MinHeap() # Stores the larger half
        
    def size(self):
        return self.H_max.size() + self.H_min.size()
    
    def satisfies_assertions(self):
        # Check max element of H_max is <= min element of H_min
        if self.H_max.size() > 0 and self.H_min.size() > 0:
            assert self.H_max.max_element() <= self.H_min.min_element(), "Max element of H_max > Min element of H_min"
        
    def insert(self, elt):
        # Part (A): Algorithm for insertion
        # 1. Determine where to insert
        if self.H_max.size() == 0 or elt <= self.H_max.max_element():
            self.H_max.insert(elt)
        else:
            self.H_min.insert(elt)
        
        # 2. Rebalance to maintain the size invariant
        # If H_max has two more elements than H_min, move max from H_max to H_min
        if self.H_max.size() > self.H_min.size() + 1:
            moved_element = self.H_max.delete_max()
            self.H_min.insert(moved_element)
        # If H_min has more elements than H_max, move min from H_min to H_max
        elif self.H_min.size() > self.H_max.size():
            moved_element = self.H_min.delete_min()
            self.H_max.insert(moved_element)
            
    # Part (B): Algorithm for finding the median
    def median(self):
        # If total size is odd, median is the max of H_max
        if self.H_max.size() > self.H_min.size():
            return self.H_max.max_element()
        # If total size is even, median is the average of max(H_max) and min(H_min)
        else: 
            return (self.H_max.max_element() + self.H_min.min_element()) / 2.0

"""
==========================================================================
5. Time Complexity Analysis:
----------------------------
- Insertion: O(log n)
    - Each heap operation (insert, delete_max, delete_min) is O(log n).
    - Number of operations per insertion is constant (1 insertion + possible 1 move).
- Find Median: O(1)
    - Simply returns the root of one or both heaps.
==========================================================================
"""

# ------------------- Test Cases -------------------

if __name__ == "__main__":
    m = MedianMaintainingHeap()
    
    print('Test 1: Inserting 5, 2, 4, -1, 7')
    m.insert(5)
    print(f'\t Insert 5: H_max = {m.H_max}, H_min = {m.H_min}, Median = {m.median()}')
    assert m.median() == 5, "Test 1 median failed"
    m.insert(2)
    print(f'\t Insert 2: H_max = {m.H_max}, H_min = {m.H_min}, Median = {m.median()}')
    # After [2, 5], median is (2+5)/2 = 3.5
    assert m.median() == 3.5, "Test 2 median failed"
    m.insert(4)
    print(f'\t Insert 4: H_max = {m.H_max}, H_min = {m.H_min}, Median = {m.median()}')
    # After [2, 4, 5], median is 4 (the middle element)
    assert m.median() == 4, "Test 3 median failed"
    m.insert(-1)
    print(f'\t Insert -1: H_max = {m.H_max}, H_min = {m.H_min}, Median = {m.median()}')
    # After [-1, 2, 4, 5], median is (2+4)/2 = 3.0
    assert m.median() == 3.0, "Test 4 median failed"
    m.insert(7)
    print(f'\t Insert 7: H_max = {m.H_max}, H_min = {m.H_min}, Median = {m.median()}')
    # After [-1, 2, 4, 5, 7], median is 4 (the middle element)
    assert m.median() == 4, "Test 5 median failed"
    
    # Test edge case: Insert same element multiple times
    print('Test 2: Inserting 1, 1, 1')
    m2 = MedianMaintainingHeap()
    m2.insert(1)
    m2.insert(1)
    m2.insert(1)
    assert m2.median() == 1, "Edge case median failed"
    
    print('All tests passed - 15 points!')
