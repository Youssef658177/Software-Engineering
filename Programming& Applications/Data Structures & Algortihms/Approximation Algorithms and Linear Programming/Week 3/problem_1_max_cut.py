"""
Problem 1: Max-Cut Problem (Greedy Balanced Cut) - English & Arabic Explanation
================================================================================
1. Problem Statement (English):
-------------------------------
We will guide you through the design of a factor-2 approximation algorithm for the Max-Cut problem. You are given an undirected graph G with n vertices and m edges.

The Max-Cut problem asks you to partition the vertices into two subsets S+ and S- such that the total number of edges crossing the cut is as large as possible.

In this problem, we implement a Greedy Algorithm for Max-Cut.
A vertex is said to be "Imbalanced" if it has strictly more edges to other nodes within its partition than edges crossing the cut.
The greedy algorithm starts from an arbitrary partition and repeatedly moves any imbalanced vertex to the other partition until no imbalanced vertices remain. The final cut guarantees that every vertex has at least half its incident edges crossing the cut.

================================================================================
2. Explanation (Arabic):
------------------------
المسألة تتعلق بمشكلة "Max-Cut"، حيث نريد تقسيم الرؤوس في رسم بياني إلى مجموعتين بحيث يكون عدد الحواف المقطوعة (التي تربط بين الرأسين من مجموعتين مختلفتين) هو الأكبر.

الحل المطلوب هو خوارزمية جشعة:
1. نبدأ بتقسيم أولي عشوائي (أو تقسيم النصف الأول في S1 والنصف الثاني في S2).
2. نبحث عن رأس "غير متوازن" (Imbalanced vertex). الرأس غير متوازن يعني أن عدد الحواف التي تربطه برؤوس في مجموعته الخاصة أكبر من عدد الحواف التي تعبر القطع. 
3. إذا وجدنا رأساً غير متوازن، نقوم بنقله إلى المجموعة الأخرى (عكس حالته الحالية).
4. نكرر هذه العملية حتى يصبح جميع الرؤوس متوازنة.
5. الخوارزمية تضمن أن كل رأس لديه على الأقل نصف حوافه تعبر القطع.

================================================================================
3. Code Implementation:
-----------------------
"""

import networkx as nx
from matplotlib import pyplot as plt 

# ------------------- Helper: Draw Graph -------------------
def draw_graph(n, edge_list, node_set_flag, set1_color='lightblue', set2_color='red'):
    # Get the list of nodes in various sets and edges that are cut and uncut
    set1_nodes = [i for i in range(1, n+1) if node_set_flag[i-1] == True]
    set2_nodes = [i for i in range(1, n+1) if node_set_flag[i-1] == False]
    edge_list_not_cut = [(i,j) for (i,j) in edge_list if node_set_flag[i-1] == node_set_flag[j-1] ]
    edge_list_cut = [(i,j) for (i,j) in edge_list if node_set_flag[i-1] != node_set_flag[j-1] ]
    
    # Draw the graph
    G = nx.Graph()
    G.add_edges_from(edge_list)
    pos = nx.spring_layout(G, seed=1234)
    plt.figure()
    nx.draw_networkx_nodes(G, pos, nodelist=set1_nodes, node_color=set1_color)
    if len(set2_nodes) >= 1:
        nx.draw_networkx_nodes(G, pos, nodelist=set2_nodes, node_color=set2_color, alpha=0.5)
    
    labels = {i:i for i in range(1, n+1)}
    nx.draw_networkx_labels(G, pos,  labels=labels)
    
    nx.draw_networkx_edges(G, pos, width=2, edgelist = edge_list_not_cut)
    nx.draw_networkx_edges(G, pos, width=2, edgelist = edge_list_cut, edge_color='red')
    plt.show()

# ------------------- Core Greedy Algorithm -------------------
def find_balanced_cut(n, adj_list):
    """
    Greedy algorithm to find a cut (partition) where every vertex has at least half
    of its incident edges crossing the cut.
    
    Args:
        n: number of vertices
        adj_list: adjacency list as a list of sets (or lists) of neighbors.
        
    Returns:
        A list of booleans of length n: True -> S1, False -> S2.
    """
    # Initial cut: first half of vertices in S1 (True), rest in S2 (False)
    cut = [True if i < n/2 else False for i in range(n)]
    
    # Precompute degrees and number of crossing edges for each vertex
    degree = [len(neighbors) for neighbors in adj_list]
    cross = [0] * n
    for i in range(n):
        ci = cut[i]
        cross[i] = sum(1 for j in adj_list[i] if cut[j] != ci)
    
    # Greedy improvement loop
    while True:
        # Find any imbalanced vertex (2*cross < degree)
        v = -1
        for i in range(n):
            if 2 * cross[i] < degree[i]:
                v = i
                break
        if v == -1:           # all vertices balanced
            break
        
        old_side = cut[v]
        # Flip the vertex
        cut[v] = not old_side
        # Update its own crossing count: old non‑crossing edges become crossing and vice versa
        cross[v] = degree[v] - cross[v]
        
        # Update crossing counts for all neighbors
        for u in adj_list[v]:
            if old_side == cut[u]:
                # Edge (v,u) was non‑crossing, now crossing
                cross[u] += 1
            else:
                # Edge (v,u) was crossing, now non‑crossing
                cross[u] -= 1
                
    return cut

"""
================================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: 
    - Computing initial cross counts: O(n + m) where m is the number of edges.
    - The greedy loop can theoretically flip a vertex multiple times. However, 
      each flip strictly improves the cut size (max-cut value) by at least 1. 
      Since a cut can have at most m edges crossing it, the loop runs at most m times. 
      Each flip requires O(degree(v)) time to update neighbors. 
      Total complexity is O(m^2) in the worst-case theoretical bound, but in practice, 
      it runs much faster (near-linear) because each vertex is flipped only a few times.
- Space Complexity: O(n + m) to store the adjacency list, degree, and cross arrays.
================================================================================
"""

# ------------------- Helper Functions for Tests -------------------
def mk_adjacency_list(n, edge_list):
    adj_list = [set() for i in range(n)]
    for (i,j) in edge_list:
        adj_list[i].add(j)
        adj_list[j].add(i)
    return adj_list

def test_cut(n, adj_list, cut):
    num_edges_crossing_cut = [0]*n
    for (i, neighbors) in enumerate(adj_list):
        num_edges_crossing_cut[i] = sum([cut[i] != cut[j] for j in neighbors])
        # Ensure at least half of the edges are crossing the cut
        if 2 * num_edges_crossing_cut[i] < len(neighbors):
            assert False, f'Test Failed: In your cut, vertex {i} has {len(neighbors)} edges incident on it but only {num_edges_crossing_cut[i]} edges cross the cut'
    return

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    from random import randint

    # Test 1: Small Graph (5 points)
    n = 5
    edge_list =  [(0,1),(0,2),(0,3),(0,4), (1,2),(1,3),(2,4),(3,4)]
    adj_list = mk_adjacency_list(n, edge_list)
    print(f'Test 1 Adjacency list is {adj_list}')
    cut = find_balanced_cut(n, adj_list)
    test_cut(n, adj_list, cut)
    print('Test 1 Passed (5 points)')

    # Test 2: Medium Graph (5 points)
    n = 8
    edge_list = [ (0,1), (0,2), (0,3), (0,4), (0,5), (0,6),
                  (1, 2), (1,3), (1,4), (1,5), (1, 6), (1,7),
                  (2, 3), (2, 5), (2, 7), 
                  (3,4), (3, 6), (3, 7),
                  (4,6), (4, 6), (4, 7),
                  (5,6), (5,7),
                  (6,7)]
    adj_list = mk_adjacency_list(n, edge_list)
    print(f'Test 2 Adjacency list is {adj_list}')
    cut = find_balanced_cut(n, adj_list)
    test_cut(n, adj_list, cut)
    print('Test 2 Passed (5 points)')

    # Test 3: Large Random Graphs (15 points)
    def mk_random_graph(n, m):
        adj_list = [set() for i in range(n)]
        for k in range(m):
            i = randint(0, n-1)
            j = randint(0, n-1)
            if i == j: 
                continue
            adj_list[i].add(j)
            adj_list[j].add(i)
        return adj_list

    adj_list = mk_random_graph(100, 1000)
    cut = find_balanced_cut(100, adj_list)
    test_cut(100, adj_list, cut)

    adj_list = mk_random_graph(100, 1000)
    cut = find_balanced_cut(100, adj_list)
    test_cut(100, adj_list, cut)

    adj_list = mk_random_graph(250, 2500)
    cut = find_balanced_cut(250, adj_list)
    test_cut(250, adj_list, cut)

    adj_list = mk_random_graph(500, 10000)
    cut = find_balanced_cut(500, adj_list)
    test_cut(500, adj_list, cut)

    print('Test 3 Passed (15 points)')
    print('All Tests Passed Successfully!')
