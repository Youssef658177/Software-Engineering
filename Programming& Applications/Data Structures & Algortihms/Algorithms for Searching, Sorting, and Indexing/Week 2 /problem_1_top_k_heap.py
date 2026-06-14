"""
Problem 1: Least-k Elements Datastructure (English & Arabic Explanation)
========================================================================
1. Problem Statement (English):
-------------------------------
We saw how min-heaps can efficiently allow us to query the least element in a heap (array). 
We would like to modify minheaps in this exercise to design a data structure to maintain the
least k elements for a given k >= 1.

Our design is to hold two arrays:
  (a) a sorted array A of k elements that forms our least k elements; and
  (b) a minheap H with the remaining n - k elements.

Our data structure will itself be a pair of arrays (A, H) with the following property:
  - H must be a minheap
  - A must be sorted of size k
  - Every element of A must be smaller than every element of H

The key operations to implement in this assignment include:
  - insert a new element into the data-structure
  - delete an existing element from the data-structure

==========================================================================
2. Explanation (Arabic):
------------------------
المسألة بتطلب تصميم هيكل بيانات للحفاظ على أصغر k عنصر. الفكرة هي استخدام مصفوفتين:
1. مصفوفة A (مرتبة تصاعدياً): فيها أصغر k عنصر.
2. Min-Heap H: فيه باقي العناصر (الأكبر من عناصر A).

الشرط الأساسي: أي عنصر في A لازم يكون أصغر من أو يساوي أي عنصر في H.

المطلوب تنفيذه (في هذا الكود):
- `insert(el)`: إدخال عنصر جديد مع الحفاظ على الخصائص.
- `delete_top_k(j)`: حذف العنصر j (حيث j=0 يعني أصغر عنصر في A).

==========================================================================
3. Code Implementation (MinHeap + TopKHeap):
---------------------------------------------
"""

class MinHeap:
    def __init__(self):
        self.H = [None]
 
    def size(self):
        return len(self.H)-1
    
    def __repr__(self):
        return str(self.H[1:])
        
    def satisfies_assertions(self):
        for i in range(2, len(self.H)):
            assert self.H[i] >= self.H[i//2],  f'Min heap property fails at position {i//2}, parent elt: {self.H[i//2]}, child elt: {self.H[i]}'
    
    def min_element(self):
        return self.H[1]

    def bubble_up(self, index):
        assert index >= 1
        if index == 1: 
            return 
        parent_index = index // 2
        if self.H[parent_index] < self.H[index]:
            return 
        else:
            self.H[parent_index], self.H[index] = self.H[index], self.H[parent_index]
            self.bubble_up(parent_index)
    
    def bubble_down(self, index):
        assert index >= 1 and index < len(self.H)
        lchild_index = 2 * index
        rchild_index = 2 * index + 1
        lchild_value = self.H[lchild_index] if lchild_index < len(self.H) else float('inf')
        rchild_value = self.H[rchild_index] if rchild_index < len(self.H) else float('inf')
        if self.H[index] <= min(lchild_value, rchild_value):
            return 
        min_child_value, min_child_index = min ((lchild_value, lchild_index), (rchild_value, rchild_index))
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


class TopKHeap:
    """Maintain the smallest k elements using A (sorted list) and H (min-heap)."""
    
    def __init__(self, k):
        self.k = k
        self.A = []
        self.H = MinHeap()
        
    def size(self): 
        return len(self.A) + (self.H.size())
    
    def get_jth_element(self, j):
        assert 0 <= j < self.k-1
        assert j < self.size()
        return self.A[j]
    
    def satisfies_assertions(self):
        # is self.A sorted
        for i in range(len(self.A) - 1):
            assert self.A[i] <= self.A[i+1], f'Array A fails to be sorted at position {i}, {self.A[i], self.A[i+1]}'
        # is self.H a heap (check min-heap property)
        self.H.satisfies_assertions()
        # is every element of self.A less than or equal to each element of self.H
        if self.H.size() > 0:
            for i in range(len(self.A)):
                assert self.A[i] <= self.H.min_element(), f'Array element A[{i}] = {self.A[i]} is larger than min heap element {self.H.min_element()}'
        
    # Helper function to insert into A
    def insert_into_A(self, elt):
        """Insert elt into A when size < k. A is kept sorted."""
        self.A.append(elt)
        j = len(self.A) - 1
        while (j >= 1 and self.A[j] < self.A[j-1]):
            (self.A[j], self.A[j-1]) = (self.A[j-1], self.A[j])
            j = j - 1 
        return
    
    # Main insert function
    def insert(self, elt):
        size = self.size()
        # If we have fewer than k elements, handle that in a special manner
        if size < self.k:
            self.insert_into_A(elt)
            return 
        
        # If the element is less than the largest element in A, it belongs to A
        if elt < self.A[-1]:
            # Evict the largest element in A to H
            largest_A = self.A.pop()
            self.H.insert(largest_A)
            
            # Insert elt into A maintaining sorted order
            self.A.append(elt)
            i = len(self.A) - 1
            while i > 0 and self.A[i] < self.A[i-1]:
                self.A[i], self.A[i-1] = self.A[i-1], self.A[i]
                i -= 1
        else:
            # Otherwise, it belongs to H
            self.H.insert(elt)
        
    # Delete top k -- delete an element from the array A
    # In particular delete the j^{th} element where j = 0 means the least element.
    # j must be in range 0 to self.k-1
    def delete_top_k(self, j):
        k = self.k
        assert self.size() > k # we need not handle the case when size is less than or equal to k
        assert j >= 0
        assert j < self.k
        
        # Remove the j-th element from sorted Array A
        self.A.pop(j)
        
        # Pop the minimum element from H (since A must have k elements)
        min_elt_H = self.H.min_element()
        self.H.delete_min()
        
        # Insert min_elt_H into A maintaining sorted order
        self.A.append(min_elt_H)
        i = len(self.A) - 1
        while i > 0 and self.A[i] < self.A[i-1]:
            self.A[i], self.A[i-1] = self.A[i-1], self.A[i]
            i -= 1

"""
==========================================================================
4. Time Complexity Analysis:
----------------------------
- insert():
    - Best case (elt belongs to H): O(log (n-k))
    - Worst case (elt belongs to A and is new minimum): O(k + log (n-k)) 
      -> O(k) for shifting/reinserting in A, and O(log (n-k)) for heap operation.
- delete_top_k():
    - O(k + log (n-k))
      -> O(k) for removing from A and reinserting from H, O(log (n-k)) for heap delete.
==========================================================================
"""

# ------------------- Test Cases -------------------

if __name__ == "__main__":
    h = TopKHeap(5)
    # Force the array A
    h.A = [-10, -9, -8, -4, 0]
    # Force the heap to this heap
    for elt in [1, 4, 5, 6, 15, 22, 31, 7]:
        h.H.insert(elt)
    
    print('Initial data structure: ')
    print('\t A = ', h.A)
    print('\t H = ', h.H)
    
    # Insert an element -2
    print('Test 1: Inserting element -2')
    h.insert(-2)
    print('\t A = ', h.A)
    print('\t H = ', h.H)
    # After insertion h.A should be [-10, -9, -8, -4, -2]
    # After insertion h.H should be [None, 0, 1, 5, 4, 15, 22, 31, 7, 6]
    assert h.A == [-10,-9,-8,-4,-2]
    assert h.H.min_element() == 0 , 'Minimum element of the heap is no longer 0'
    h.satisfies_assertions()
    
    print('Test2: Inserting element -11')
    h.insert(-11)
    print('\t A = ', h.A)
    print('\t H = ', h.H)
    assert h.A == [-11, -10, -9, -8, -4]
    assert h.H.min_element() == -2
    h.satisfies_assertions()
    
    print('Test 3 delete_top_k(3)')
    h.delete_top_k(3)
    print('\t A = ', h.A)
    print('\t H = ', h.H)
    h.satisfies_assertions()
    assert h.A == [-11,-10,-9,-4,-2]
    assert h.H.min_element() == 0
    h.satisfies_assertions()
    
    print('Test 4 delete_top_k(4)')
    h.delete_top_k(4)
    print('\t A = ', h.A)
    print('\t H = ', h.H)
    assert h.A == [-11, -10, -9, -4, 0]
    h.satisfies_assertions()
    
    print('Test 5 delete_top_k(0)')
    h.delete_top_k(0)
    print('\t A = ', h.A)
    print('\t H = ', h.H)
    assert h.A == [-10, -9, -4, 0, 1]
    h.satisfies_assertions()
    
    print('Test 6 delete_top_k(1)')
    h.delete_top_k(1)
    print('\t A = ', h.A)
    print('\t H = ', h.H)
    assert h.A == [-10, -4, 0, 1, 4]
    h.satisfies_assertions()
    print('All tests passed - 15 points!')
