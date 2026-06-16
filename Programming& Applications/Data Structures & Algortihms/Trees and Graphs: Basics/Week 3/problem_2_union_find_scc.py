"""
Problem 2: Use union-find data-structures to compute strongly connected components (English & Arabic Explanation)
==================================================================================================================
1. Problem Statement (English):
-------------------------------
We will now explore finding maximal strongly connected components of an undirected graph using union find data structures. The undirected graph just consists of a list of edges with weights.

We will associate a non-negative weight w_{i,j} for each undirected edge (i, j). We associate some extra data with vertices that will come in handy later.

2A: Use union-find data-structures to compute strongly connected components.
We will consider only those edges (i, j) whose weights are less than or equal to a threshold W provided by the user. Edges with weights above this threshold are not considered.

Design an algorithm to compute all the maximal strongly connected components for all edges with threshold W using the union-find data structure. What is the running time of your algorithm?

================================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب حساب المكونات المتصلة بقوة (SCCs) في رسم بياني غير موجه باستخدام Union-Find مع مراعاة عتبة (Threshold) للوزن.

الفكرة الأساسية:
1. نقوم بتهيئة `DisjointForests` (Union-Find) بعدد الرؤوس في الرسم البياني.
2. نمر على جميع الحواف في الرسم البياني.
3. إذا كان وزن الحافة `w` أقل من أو يساوي العتبة `W`، نقوم بدمج الرأسين `i` و `j` معًا باستخدام `union`.
4. النتيجة النهائية هي مجموعة من المكونات المتصلة (SCCs)، كل منها عبارة عن مجموعة من الرؤوس المترابطة.

التعقيد الزمني: `O(m * α(n))` حيث `m` عدد الحواف، `n` عدد الرؤوس، و `α(n)` هو معكوس دالة أكيرمان (ثابت تقريبًا). لأن دالة `find` و `union` تعملان في وقت `O(α(n))` مع ضغط المسار (Path Compression) والاتحاد حسب الرتبة (Union by Rank).

================================================================================
3. Code Implementation:
-----------------------
"""

class UndirectedGraph:
    # n is the number of vertices
    # we will label the vertices from 0 to self.n -1
    # We simply store the edges in a list.
    def __init__(self, n):
        assert n >= 1, 'You are creating an empty graph -- disallowed'
        self.n = n
        self.edges = []
        self.vertex_data = [None] * self.n

    def set_vertex_data(self, j, dat):
        assert 0 <= j < self.n
        self.vertex_data[j] = dat

    def get_vertex_data(self, j):
        assert 0 <= j < self.n
        return self.vertex_data[j]

    def add_edge(self, i, j, wij):
        assert 0 <= i < self.n
        assert 0 <= j < self.n
        assert i != j
        # Make sure to add edge from i to j with weight wij
        self.edges.append((i, j, wij))

    def sort_edges(self):
        # sort edges in ascending order of weights.
        self.edges = sorted(self.edges, key=lambda edg_data: edg_data[2])


# (DisjointForests class from previous problem - included for completeness)
class DisjointForests:
    def __init__(self, n):
        assert n >= 1, ' Empty disjoint forest is disallowed'
        self.n = n
        self.parents = [None] * n
        self.rank = [None] * n

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

    def find(self, j):
        assert 0 <= j < self.n
        assert self.parents[j] is not None, 'You are calling find on an element that is not part of the family yet. Please call make_set first.'
        if self.parents[j] != j:
            self.parents[j] = self.find(self.parents[j])
        return self.parents[j]

    def union(self, j1, j2):
        assert 0 <= j1 < self.n
        assert 0 <= j2 < self.n
        assert self.parents[j1] is not None
        assert self.parents[j2] is not None
        r1 = self.find(j1)
        r2 = self.find(j2)

        if r1 == r2:
            return

        if self.rank[r1] < self.rank[r2]:
            self.parents[r1] = r2
        else:
            self.parents[r2] = r1
            if self.rank[r1] == self.rank[r2]:
                self.rank[r1] += 1


def compute_scc(g, W):
    # create a disjoint forest with as many elements as number of vertices
    d = DisjointForests(g.n)

    # 1. Initialize every vertex as its own set
    for i in range(g.n):
        d.make_set(i)

    # 2. Iterate through all edges
    for (i, j, wij) in g.edges:
        # 3. Union vertices if the edge weight is <= W
        if wij <= W:
            d.union(i, j)

    # extract a set of sets from d
    return d.dictionary_of_sets()

"""
================================================================================
4. Time Complexity Analysis:
----------------------------
- Creating DisjointForests: O(n)
- Initializing each vertex: O(n)
- Iterating over all m edges: O(m)
- For each edge, union operation takes O(α(n)) amortized.
- Total time complexity: O(n + m * α(n)) ≈ O(m * α(n))
================================================================================
"""

# ------------------- Test Cases -------------------

if __name__ == "__main__":
    g3 = UndirectedGraph(8)
    g3.add_edge(0, 1, 0.5)
    g3.add_edge(0, 2, 1.0)
    g3.add_edge(0, 4, 0.5)
    g3.add_edge(2, 3, 1.5)
    g3.add_edge(2, 4, 2.0)
    g3.add_edge(3, 4, 1.5)
    g3.add_edge(5, 6, 2.0)
    g3.add_edge(5, 7, 2.0)

    res = compute_scc(g3, 2.0)
    print('SCCs with threshold 2.0 computed by your code are:')
    assert len(res) == 2, f'Expected 2 SCCs but got {len(res)}'
    for (k, s) in res.items():
        print(s)

    # Let us check that your code returns what we expect.
    for (k, s) in res.items():
        if k in [0, 1, 2, 3, 4]:
            assert s == set([0, 1, 2, 3, 4]), '{0,1,2,3,4} should be an SCC'
        if k in [5, 6, 7]:
            assert s == set([5, 6, 7]), '{5,6,7} should be an SCC'

    print('SCCs with threshold 1.5')
    res2 = compute_scc(g3, 1.5)  # This cuts off edges 2,4 and 5, 6, 7
    for (k, s) in res2.items():
        print(s)
    assert len(res2) == 4, f'Expected 4 SCCs but got {len(res2)}'

    for (k, s) in res2.items():
        if k in [0, 1, 2, 3, 4]:
            assert s == set([0, 1, 2, 3, 4]), '{0,1,2,3,4} should be an SCC'
        if k in [5]:
            assert s == set([5]), '{5} should be an SCC with just a single node.'
        if k in [6]:
            assert s == set([6]), '{6} should be an SCC with just a single node.'
        if k in [7]:
            assert s == set([7]), '{7} should be an SCC with just a single node.'

    print('All tests passed: 10 points')
