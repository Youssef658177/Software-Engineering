"""
Problem 1: Least-k Elements Datastructure (English & Arabic Explanation)
========================================================================
1. Problem Statement (English):
-------------------------------
We saw how min-heaps can efficiently allow us to query the least element in a heap (array). 
We would like to modify minheaps in this exercise to design a data structure to maintain the
least k elements for a given k >= 1 with k being the minheap data-structure.

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
المسألة بتطلب تصميم هيكل بيانات للحفاظ على أصغر k عنصر من مجموعة بيانات كبيرة.
الفكرة هي استخدام مصفوفتين:
1. مصفوفة A: فيها أصغر k عنصر (مرتبة تصاعدياً).
2. Min-Heap H: فيه باقي العناصر (الأكبر).

الشرط الأساسي: أي عنصر في A لازم يكون أصغر من أي عنصر في H.

المطلوب:
- خوارزمية (A): إدخال عنصر جديد (مع وصف سيناريوهات الإدخال المختلفة).
- خوارزمية (B): حذف عنصر موجود (مع مراعاة الحالات المختلفة).

الكود اللي أنت أرسلته هو تنفيذ كامل لـ MinHeap (الجزء H)، وهو صحيح تماماً.

==========================================================================
3. Code Implementation (MinHeap - Your Code):
---------------------------------------------
"""
# ------------------- Code Implementation -------------------

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

    ## bubble_up function at index
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
    
    ## bubble_down function at index
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
        
    # Function: heap_insert (Your code)
    def insert(self, elt):
        # Add the element to the end of the heap
        self.H.append(elt)
        # Bubble up to maintain heap property
        self.bubble_up(len(self.H) - 1)
        
    # Function: heap_delete_min (Your code)
    def delete_min(self):
        # If heap is empty, return None
        if self.size() == 0:
            return
        # Swap the root (minimum) with the last element
        self.H[1], self.H[-1] = self.H[-1], self.H[1]
        # Remove the new last element (which is the original min)
        min_val = self.H.pop()
        # Bubble down the new root to restore heap property
        if self.size() > 0:
            self.bubble_down(1)
        return min_val

# ------------------- Test Cases -------------------

if __name__ == "__main__":
    h = MinHeap()
    print('Inserting: 5, 2, 4, -1 and 7 in that order.')
    h.insert(5)
    print(f'\t Heap = {h}')
    assert(h.min_element() == 5)
    h.insert(2)
    print(f'\t Heap = {h}')
    assert(h.min_element() == 2)
    h.insert(4)
    print(f'\t Heap = {h}')
    assert(h.min_element() == 2)
    h.insert(-1)
    print(f'\t Heap = {h}')
    assert(h.min_element() == -1)
    h.insert(7)
    print(f'\t Heap = {h}')
    assert(h.min_element() == -1)
    h.satisfies_assertions()

    print('Deleting minimum element')
    h.delete_min()
    print(f'\t Heap = {h}')
    assert(h.min_element() == 2)
    h.delete_min()
    print(f'\t Heap = {h}')
    assert(h.min_element() == 4)
    h.delete_min()
    print(f'\t Heap = {h}')
    assert(h.min_element() == 5)
    h.delete_min()
    print(f'\t Heap = {h}')
    assert(h.min_element() == 7)
    # Test delete_max on heap of size 1, should result in empty heap.
    h.delete_min()
    print(f'\t Heap = {h}')
    print('All tests passed: 10 points!')

"""
==========================================================================
4. Solutions for Conceptual Questions (Parts A & B):
----------------------------------------------------

**Design Insertion Algorithm (Part A):**
When inserting a new element `x` into the data structure:
1. Compare `x` with the largest element in `A` (i.e., `A[-1]` since `A` is sorted).
2. If `x <= A[-1]`: 
   - `x` should be in `A`. 
   - Insert `x` into `A` maintaining sorted order (O(k)).
   - The largest element of `A` (`A[-1]`) becomes the new element that may belong to `H`.
   - Remove `A[-1]` from `A` and `insert` it into `H` (O(log(n-k))).
3. If `x > A[-1]`: 
   - `x` should be in `H`. 
   - `insert` `x` directly into `H` (O(log(n-k))).

**Complexity:** O(k + log(n-k)) worst case. `k` for sorting `A` and `log(n-k)` for heap `H`.

**Design Deletion Algorithm (Part B):**
To delete an element at index `j` from `A`:
1. Remove element `A[j]` and shift elements left to fill the gap.
2. Now `A` has size `k-1`.
3. To restore the property that `A` has size `k`:
   - Take the minimum element from `H` (`H.min_element()`).
   - Insert it into the correct position in `A` (O(k)).
   - Delete the minimum element from `H` (O(log(n-k))).
==========================================================================
"""
