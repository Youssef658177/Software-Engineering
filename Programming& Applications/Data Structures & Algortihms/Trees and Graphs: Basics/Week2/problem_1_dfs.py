"""
Problem 1: Program DFS for Undirected Graph Data Structure (English & Arabic Explanation)
==========================================================================================
1. Problem Statement (English):
-------------------------------
We will now program an undirected graph using the adjacency list representation in Python, along with some utility functions including a depth first search algorithm over undirected graphs.

(1A) Run through DFS for the example graph below:
    Graph: 5 vertices (0, 1, 2, 3, 4) with edges: (0,1), (0,2), (0,4), (2,3), (2,4), (3,4).
    Assume the DFS visit starts from node 0. Adjacent nodes are visited in ascending order.

    (a) Order in which nodes are visited.
    (b) Table of discovery and finish times.
    (c) DFS tree parent for each node.
    (d) Back edges discovered by DFS (non-trivial).

(1B) Complete the code for the `dfs_visit` function.
    - Use `DFSTimeCounter` to keep track of time.
    - Increment timer just before returning from `dfs_visit` and recording finish time.
    - Record back edges when an adjacent node is discovered but not finished.

==========================================================================================
2. Explanation (Arabic):
------------------------
هذه المسألة تطلب تنفيذ خوارزمية DFS على رسم بياني غير موجه، مع حساب أوقات الاكتشاف والانتهاء، وتحديد الحواف الخلفية.

الجزء النظري (1A) تم حله:
    (a) الترتيب: 0, 1, 2, 3, 4
    (b) الأوقات: (0:0,9), (1:1,2), (2:3,8), (3:4,5), (4:6,7)
    (c) الآباء: 0->None, 1->0, 2->0, 3->2, 4->3
    (d) الحواف الخلفية غير البديهية: (4,0) و (4,2)

الجزء البرمجي (1B) مكتمل واجتاز الاختبارات.

==========================================================================================
3. Code Implementation:
-----------------------
"""

class DFSTimeCounter:
    def __init__(self):
        self.count = 0
    
    def reset(self):
        self.count = 0
    
    def increment(self):
        self.count = self.count + 1
        
    def get(self):
        return self.count 
    
class UndirectedGraph:
    
    def __init__(self, n):
        self.n = n
        self.adj_list = [ set() for i in range(self.n) ]
        
    def add_edge(self, i, j):
        assert 0 <= i < self.n
        assert 0 <= j < self.n
        assert i != j
        self.adj_list[i].add(j)
        self.adj_list[j].add(i)
        
    def get_neighboring_vertices(self, i):
        assert 0 <= i < self.n
        return self.adj_list[i]
    
    # Function: dfs_visit (Complete Solution)
    def dfs_visit(self, i, dfs_timer, discovery_times, finish_times, 
                        dfs_tree_parent, dfs_back_edges):
        assert 0 <= i < self.n
        assert discovery_times[i] == None
        assert finish_times[i] == None
        
        # Step 1: Set discovery time for the current node
        discovery_times[i] = dfs_timer.get()
        dfs_timer.increment()
        
        # Step 2: Explore all neighbors in increasing order
        for neighbor in self.get_neighboring_vertices(i):
            # Case A: Neighbor has not been discovered yet
            if discovery_times[neighbor] == None:
                dfs_tree_parent[neighbor] = i
                self.dfs_visit(neighbor, dfs_timer, discovery_times, finish_times, 
                               dfs_tree_parent, dfs_back_edges)
            # Case B: Neighbor is discovered but not finished -> Back edge
            elif finish_times[neighbor] == None:
                dfs_back_edges.append((i, neighbor))
        
        # Step 3: Set finish time for the current node
        finish_times[i] = dfs_timer.get()     # Record finish time first
        dfs_timer.increment()                 # Then increment the counter
    
    # Function: dfs_traverse_graph
    def dfs_traverse_graph(self):
        dfs_timer = DFSTimeCounter()
        discovery_times = [None]*self.n
        finish_times = [None]*self.n
        dfs_tree_parents = [None]*self.n
        dfs_back_edges = []
        for i in range(self.n):
            if discovery_times[i] == None:
                self.dfs_visit(i, dfs_timer, discovery_times, finish_times, 
                               dfs_tree_parents, dfs_back_edges)
        # Clean up trivial back edges
        non_trivial_back_edges = [(i,j) for (i,j) in dfs_back_edges if dfs_tree_parents[i] != j]
        return (dfs_tree_parents, non_trivial_back_edges, discovery_times, finish_times)

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    g = UndirectedGraph(5)
    g.add_edge(0,1)
    g.add_edge(0,2)
    g.add_edge(0,4)
    g.add_edge(2,3)
    g.add_edge(2,4)
    g.add_edge(3,4)

    discovery_times = [None]*5
    finish_times = [None]*5
    dfs_tree_parents = [None]*5
    dfs_back_edges = []
    g.dfs_visit(0, DFSTimeCounter(), discovery_times, finish_times, dfs_tree_parents, dfs_back_edges )

    print('DFS visit discovery and finish times given by your code.')
    print('Node\t Discovery\t Finish')
    for i in range(5):
        print(f'{i} \t {discovery_times[i]}\t\t {finish_times[i]}')

    assert(discovery_times[0] == 0)
    assert(discovery_times[1] == 1)
    assert(finish_times[1] == 2)
    assert(discovery_times[2] == 3)
    assert(finish_times[2] == 8)
    assert(discovery_times[3] == 4)
    assert(finish_times[3] == 7)
    assert(discovery_times[4] == 5)
    assert(finish_times[4] == 6)

    print('Success -- discovery and finish times seem correct.')
    
    print('Node\t DFS-Tree-Parent')
    for i in range(5):
        print(f'{i} \t {dfs_tree_parents[i]}')

    assert(dfs_tree_parents[0] == None)
    assert(dfs_tree_parents[1] == 0)
    assert(dfs_tree_parents[2] == 0)
    assert(dfs_tree_parents[3] == 2)
    assert(dfs_tree_parents[4] == 3)

    print('Success-- DFS parents are set correctly.')
    
    non_trivial_back_edges = [(i,j) for (i,j) in dfs_back_edges if dfs_tree_parents[i] != j]
    print('Back edges are')
    for (i,j) in non_trivial_back_edges:
        print(f'{(i,j)}')
    
    assert len(non_trivial_back_edges) == 2
    assert (4,2) in non_trivial_back_edges
    assert (4,0) in non_trivial_back_edges

    print('Success -- 15 points!')
