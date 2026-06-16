"""
Problem 1: Disjoint Forests (Union-Find Data Structure)
=======================================================
1. Problem Statement (English):
-------------------------------
We will first complete an implementation of a union-find data structure with rank compression.

Implement the following functions for a Disjoint Forests class:
- `make_set(j)`: Create a new set containing element `j`.
- `find(j)`: Find the representative (root) of the set containing `j` with path compression.
- `union(j1, j2)`: Union the sets containing `j1` and `j2` using union by rank.

Constraints:
- `n` is the number of elements (0 to n-1).
- `make_set` must be called for each element before any union/find operation on it.

================================================================
2. Explanation (Arabic):
------------------------
هيكل البيانات Union-Find (Disjoint Forests) يستخدم لإدارة مجموعات منفصلة بكفاءة عالية. العمليات الأساسية هي:
- `make_set`: إنشاء مجموعة جديدة تحتوي على عنصر واحد.
- `find`: العثور على ممثل (جذر) المجموعة التي ينتمي إليها عنصر معين، مع تطبيق "ضغط المسار" (Path Compression) لجعل الاستعلامات المستقبلية أسرع.
- `union`: دمج مجموعتين معاً باستخدام استراتيجية "الاتحاد حسب الرتبة" (Union by Rank) للحفاظ على الشجرة متوازنة.

الكود المرفق يقوم بتنفيذ هذه العمليات واختبارها.

================================================================
3. Code Implementation:
-----------------------
"""

class DisjointForests:
    def __init__(self, n):
        assert n >= 1, 'Empty disjoint forest is disallowed'
        self.n = n
        self.parents = [None] * n
        self.rank = [None] * n

    # Function: dictionary_of_sets
    # Convert the disjoint forest structure into a dictionary d
    # wherein d has an entry for each representative i
    # d[i] maps to each elements which belongs to the tree corresponding to i
    # in the disjoint forest.
    def dictionary_of_sets(self):
        d = {}
        for i in range(self.n):
            if self.is_representative(i):
                d[i] = set([i])
        for j in range(self.n):
            if self.parents[j] is not None:
                root = self.find(j)
                assert root in d
                d[root].add(j)
        return d

    def make_set(self, j):
        assert 0 <= j < self.n
        assert self.parents[j] is None, 'You are calling make_set on an element multiple times -- not allowed.'
        self.parents[j] = j
        self.rank[j] = 1

    def is_representative(self, j):
        return self.parents[j] == j

    def get_rank(self, j):
        return self.rank[j]

    # Function: find
    # Implement the find algorithm for a node j in the set.
    # Repeatedly traverse the parent pointer until we reach a root.
    # Implement the "path compression" strategy by making all
    # nodes along path from j to the root point directly to the root.
    def find(self, j):
        assert 0 <= j < self.n
        assert self.parents[j] is not None, 'You are calling find on an element that is not part of the family yet. Please call make_set first.'
        # Path compression
        if self.parents[j] != j:
            self.parents[j] = self.find(self.parents[j])
        return self.parents[j]

    # Function : union
    # Compute union of j1 and j2
    # First do a find to get to the representatives of j1 and j2.
    # If they are not the same, then
    # implement union using the rank strategy I.e., lower rank root becomes
    # child of the higher ranked root.
    # break ties by making the first argument j1's root the parent.
    def union(self, j1, j2):
        assert 0 <= j1 < self.n
        assert 0 <= j2 < self.n
        assert self.parents[j1] is not None
        assert self.parents[j2] is not None
        # Find the roots (representatives) of j1 and j2
        r1 = self.find(j1)
        r2 = self.find(j2)

        # If they are already in the same set, do nothing
        if r1 == r2:
            return

        # Union by rank: attach the lower rank tree under the higher rank tree
        if self.rank[r1] < self.rank[r2]:
            self.parents[r1] = r2
        else:
            self.parents[r2] = r1
            # If ranks are equal, the new root's rank increases by 1
            if self.rank[r1] == self.rank[r2]:
                self.rank[r1] += 1

"""
================================================================
4. Time Complexity Analysis:
----------------------------
- `make_set`: O(1)
- `find`: O(α(n)) amortized, where α is the inverse Ackermann function (practically constant).
- `union`: O(α(n)) amortized.
- `dictionary_of_sets`: O(n α(n))

================================================================
5. Test Cases:
--------------
"""
if __name__ == "__main__":
    d = DisjointForests(10)
    for i in range(10):
        d.make_set(i)

    for i in range(10):
        assert d.find(i) == i, f'Failed: Find on {i} must return {i} back'

    d.union(0, 1)
    d.union(2, 3)
    assert d.find(0) == d.find(1), '0 and 1 have been union-ed together'
    assert d.find(2) == d.find(3), '2 and 3 have been union-ed together'
    assert d.find(0) != d.find(3), '0 and 3 should be in different trees'
    assert ((d.get_rank(0) == 2 and d.get_rank(1) == 1) or
            (d.get_rank(1) == 2 and d.get_rank(0) == 1)), 'one of the nodes 0 or 1 must have rank 2'
    assert ((d.get_rank(2) == 2 and d.get_rank(3) == 1) or
            (d.get_rank(3) == 2 and d.get_rank(2) == 1)), 'one of the nodes 2 or 3 must have rank 2'

    d.union(3, 4)
    assert d.find(2) == d.find(4), '2 and 4 must be in the same set in the family.'

    d.union(5, 7)
    d.union(6, 8)
    d.union(3, 7)
    d.union(0, 6)

    assert d.find(6) == d.find(1), '1 and 6 must be in the same set in the family'
    assert d.find(7) == d.find(4), '7 and 4 must be in the same set in the family'
    print('All tests passed: 10 points.')
