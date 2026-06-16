"""
Problem 1: Program DFS for Undirected Graph Data Structure (Continued)
==========================================================================================
C1. Find the number of (maximal) strongly connected components in an undirected graph.

    Example: A graph has 3 maximal strongly connected components with vertices {0,1,2,3,4}, 
    {5,6}, and {7}. Return the number of components.

1C. Find the set of all nodes in the graph that belong to some cycle.

    Example: In the given graph, nodes {0,2,3,4} lie on some cycle. Return a set of these nodes.

==========================================================================================
2. Explanation (Arabic):
------------------------
**C1** - حساب عدد المكونات المتصلة (Connected Components) في الرسم البياني غير الموجه.
   الفكرة بسيطة: في شجرة DFS (التي ينتجها `dfs_traverse_graph`)، كل شجرة لها جذر واحد. وبما أن الرسم البياني غير موجه، فإن عدد الأشجار في غابة DFS يساوي عدد المكونات المتصلة. الجذر هو العقدة التي يكون أبها (`parent`) يساوي `None`.

**1C** - إيجاد جميع العقد التي تنتمي إلى دورة (Cycle).
   تعتمد الفكرة على الحواف الخلفية (Back Edges). الحافة الخلفية هي حافة بين عقدة `u` وعقدة `v`، حيث تم اكتشاف `v` قبل `u` ولم ينته وقتها بعد. إذا وجدنا حافة خلفية غير بديهية (أي ليست الحافة بين العقدة ووالدها المباشر)، فهذا يعني أن `u` و `v` وجميع العقد على المسار بينهما في شجرة DFS تشكل دورة. الخوارزمية تتبع مؤشرات الأبوة من `u` إلى `v` وتضيف كل العقد المارة بها.

==========================================================================================
3. Code Implementation:
-----------------------
"""

def num_connected_components(g):
    # g is an UndirectedGraph class
    parents, _, _, _ = g.dfs_traverse_graph()
    
    # The number of connected components is the number of roots in the DFS tree.
    # A root is a node with no parent (parent is None).
    count = 0
    for p in parents:
        if p is None:
            count += 1
    return count

def find_all_nodes_in_cycle(g):
    # g is an UndirectedGraph class
    set_of_nodes = set()
    
    # 1. Use the dfs_traverse_graph to get parents and non-trivial back edges
    parents, non_trivial_back_edges, _, _ = g.dfs_traverse_graph()
    
    # 2. Iterate over all non-trivial back edges
    for u, v in non_trivial_back_edges:
        # Add both endpoints of the back edge to the set
        set_of_nodes.add(u)
        set_of_nodes.add(v)
        
        # 3. Trace the path from u to v in the DFS tree
        current = u
        while current != v:
            current = parents[current]
            if current is not None:
                set_of_nodes.add(current)
            else:
                # Safety break (should not happen for a valid back edge)
                break
                
    return set_of_nodes

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    # Test C1: Number of Connected Components
    g = UndirectedGraph(5)
    g.add_edge(0,1)
    g.add_edge(0,2)
    g.add_edge(0,4)
    g.add_edge(2,3)
    g.add_edge(2,4)
    g.add_edge(3,4)
    assert num_connected_components(g) == 1, f'Test A failed'

    g2 = UndirectedGraph(7)
    g2.add_edge(0,1)
    g2.add_edge(0,2)
    g2.add_edge(0,4)
    g2.add_edge(2,3)
    g2.add_edge(2,4)
    g2.add_edge(3,4)
    g2.add_edge(5,6)
    assert num_connected_components(g2) == 2, f'Test B failed'

    g3 = UndirectedGraph(8)
    g3.add_edge(0,1)
    g3.add_edge(0,2)
    g3.add_edge(0,4)
    g3.add_edge(2,3)
    g3.add_edge(2,4)
    g3.add_edge(3,4)
    g3.add_edge(5,6)
    assert num_connected_components(g3) == 3, f'Test C failed'
    
    g3.add_edge(7,5)
    assert num_connected_components(g3) == 2, f'Test D failed'
    
    # Test 1C: Nodes in Cycle
    g_cycle = UndirectedGraph(8)
    g_cycle.add_edge(0,1)
    g_cycle.add_edge(0,2)
    g_cycle.add_edge(0,4)
    g_cycle.add_edge(2,3)
    g_cycle.add_edge(2,4)
    g_cycle.add_edge(3,4)
    g_cycle.add_edge(5,6)
    g_cycle.add_edge(5,7)
    
    s = find_all_nodes_in_cycle(g_cycle)
    print(f'Nodes in cycle: {s}')
    assert s == {0,2,3,4}, 'Fail: Set of nodes must be {0,2,3,4}.'

    g_cycle.add_edge(6,7)
    s1 = find_all_nodes_in_cycle(g_cycle)
    print(f'Nodes in cycle: {s1}')
    assert s1 == {0,2,3,4,5,6,7}, 'Fail: Set of nodes must be {0,2,3,4,5,6,7}.'

    print('All tests passed: 10 points!')
