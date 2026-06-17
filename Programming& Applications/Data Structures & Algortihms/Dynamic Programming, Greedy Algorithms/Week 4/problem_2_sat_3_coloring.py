"""
Problem 2: Use SAT solver to solve 3-coloring problem (English & Arabic Explanation)
=====================================================================================
1. Problem Statement (English):
-------------------------------
The 3-color problem asks given an undirected graph G, whether it can be colored with 3 or fewer colors. I.e., assign each vertex of the graph one of three colors, say Red, Blue, Green such that vertices connected by an edge should not have the same color.

Part A: Given a graph G and a proposed 3-coloring represented as a map from vertices to colors {1, 2, 3}, check that it is a valid three coloring of the graph.

Part B: Using the SAT solver (DPLL algorithm) implemented in the previous assignment, encode the 3-coloring problem into CNF form and solve it to find a valid coloring if one exists.

=====================================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب حل مشكلة تلوين الرسم البياني بـ 3 ألوان (3-Coloring) باستخدام خوارزمية SAT (DPLL).

**كيفية تحويل التلوين إلى SAT:**
لدينا n رأس، و 3 ألوان. نستخدم `n * 3` متغير منطقي. المتغير `x_{v, c}` يعني أن الرأس `v` لونه `c`.
1. **كل رأس لابد أن يأخذ لوناً واحداً على الأقل:** 
   `(x_{v,1} OR x_{v,2} OR x_{v,3})`
2. **كل رأس لا يمكن أن يأخذ لونين في نفس الوقت:** 
   `(NOT x_{v,1} OR NOT x_{v,2})` (وهكذا لكل زوج من الألوان).
3. **الرؤوس المتصلة بحافة لا يمكن أن تأخذ نفس اللون:**
   لأي حافة `(u, v)`، نمنع تطابق ألوانهما. مثلاً: `(NOT x_{u,1} OR NOT x_{v,1})`.

بعد ذلك، نستخدم `dpll_algorithm` لإيجاد إسناد للمتغيرات يحقق كل هذه البنود، ونترجم الإسناد إلى قاموس ألوان.

=====================================================================================
3. Code Implementation (Full Solution):
-----------------------
"""

# ---------- SATInstance & DPLL Algorithm (Imported from previous problem) ----------
class SATInstance:
    def __init__(self, n, clauses):
        self.n = n          # number of variables (1..n)
        self.clauses = clauses  # list of lists of literals (positive/negative integers)
    
    def add_clause(self, clause):
        self.clauses.append(clause)
    
    def evaluate(self, truth_assign):
        all_satisfied = True
        for clause in self.clauses:
            clause_satisfied = False
            clause_falsified = True
            for lit in clause:
                var = abs(lit)
                if var in truth_assign:
                    val = truth_assign[var]
                    if (lit > 0 and val) or (lit < 0 and not val):
                        clause_satisfied = True
                        clause_falsified = False
                        break
                else:
                    clause_falsified = False
            if clause_satisfied:
                continue
            if clause_falsified:
                return -1
            all_satisfied = False
        return 1 if all_satisfied else 0

def extend_truth_assignment(truth_assign, j, b):
    truth_assign[j] = b
    return truth_assign
    
def forget_var_in_truth_assign(truth_assign, j):
    if j in truth_assign:
        del truth_assign[j]
    return truth_assign

def dpll_algorithm(formula, partial_truth_assign, j):
    # Evaluate current partial assignment
    val = formula.evaluate(partial_truth_assign)
    if val == 1:          # formula satisfied
        return True, partial_truth_assign
    if val == -1:         # formula falsified
        return False, None
    if j > formula.n:     # No more variables to assign
        return False, None
    
    # Try assigning j = True
    extend_truth_assignment(partial_truth_assign, j, True)
    res, final = dpll_algorithm(formula, partial_truth_assign, j+1)
    if res:
        return True, final
    forget_var_in_truth_assign(partial_truth_assign, j)
    
    # Try assigning j = False
    extend_truth_assignment(partial_truth_assign, j, False)
    res, final = dpll_algorithm(formula, partial_truth_assign, j+1)
    if res:
        return True, final
    forget_var_in_truth_assign(partial_truth_assign, j)
    
    return False, None

def solve_formula(formula):
    return dpll_algorithm(formula, {}, 1)

# ---------- Part A: UndirectedGraph and Color Check ----------
class UndirectedGraph:
    # n_verts: number of vertices of the graph
    #   vertices are labeled from 0... n-1
    # adj_list: an adjacency list represented as a list of lists.
    def __init__(self, n_verts, adj_list=None):
        self.n = n_verts
        if adj_list is None:
            adj_list = [ [] for _ in range(self.n)]
        else:
            assert len(adj_list) == n_verts
            for lst in adj_list:
                for elt in lst:
                    assert 0 <= elt < self.n
        self.adj_list = adj_list
    
    def add_edge(self, i, j):
        assert 0 <= i < self.n
        assert 0 <= j < self.n
        assert i != j
        self.adj_list[i].append(j)
        self.adj_list[j].append(i)
        
    def get_list_of_edges(self):
        return [ (i, j) for i in range(self.n) for j in self.adj_list[i] if i < j ]

def is_three_coloring(graph, coloring):
    n = graph.n
    for i in range(n):
        if i not in coloring:
            return False
        if coloring[i] < 1 or coloring[i] > 3:
            return False
    for (i, j) in graph.get_list_of_edges():
        if coloring[i] == coloring[j]:
            return False
    return True

# ---------- Part B: SAT Encoding and Solver ----------
def translate_three_coloring(graph):
    n_boolean_vars = graph.n * 3  # 3 boolean variables for each vertex
    # Scheme: x_{i,j} (vertex i, color j) → variable 3*i + j  (1 <= j <= 3)
    s = SATInstance(n_boolean_vars, [])  # no clauses initially
    
    # For each vertex i
    for i in range(graph.n):
        # At least one color: (x_{i,1} ∨ x_{i,2} ∨ x_{i,3})
        clause_at_least_one = [3*i + j for j in range(1, 4)]
        s.add_clause(clause_at_least_one)
        
        # At most one color: for all pairs j < k, (¬x_{i,j} ∨ ¬x_{i,k})
        for j in range(1, 4):
            for k in range(j+1, 4):
                s.add_clause([-(3*i + j), -(3*i + k)])
    
    # For each edge (u,v) and each color j: ¬x_{u,j} ∨ ¬x_{v,j}
    for (u, v) in graph.get_list_of_edges():
        for j in range(1, 4):
            s.add_clause([-(3*u + j), -(3*v + j)])
    
    return s

def extract_graph_coloring_from_truth_assignment(graph, truth_assign):
    coloring = {}
    for i in range(graph.n):
        color = None
        for j in range(1, 4):
            var = 3*i + j
            if truth_assign.get(var, False):  # variable is True
                if color is not None:
                    # Multiple true colors for the same vertex – invalid assignment
                    return None
                color = j
        if color is None:
            # No color assigned to vertex i
            return None
        coloring[i] = color
    return coloring

def solve_three_coloring(graph):
    s = translate_three_coloring(graph)
    # print(s.clauses)  # (Optional) Print the CNF clauses for debugging
    res, truth_assign = solve_formula(s)
    if res:
        return extract_graph_coloring_from_truth_assignment(graph, truth_assign)
    else:
        return None

"""
=====================================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Translating to CNF: O(V + E) 
  (V is vertices, E is edges. We generate (V*3 + V*3 + E*3) clauses).
- DPLL SAT Solving (solve_three_coloring): O(2^n) worst-case time, where n is the number of variables (3 * V).
  However, with heuristics (unit propagation - not implemented in bare bones version), it performs much better.
- Space Complexity: O(V + E) to store the CNF clauses.
=====================================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    print('--- Test 0 ---')
    g0 = UndirectedGraph(3)
    g0.add_edge(0,1)
    g0.add_edge(1,2)
    g0.add_edge(0,2)
    coloring = solve_three_coloring(g0)
    print(coloring)
    assert coloring != None
    assert is_three_coloring(g0, coloring)
    print('Passed')

    print('-- Test 1 --')
    g1 = UndirectedGraph(4)
    g1.add_edge(0, 1)
    g1.add_edge(0, 2)
    g1.add_edge(0, 3)
    g1.add_edge(1, 2)
    g1.add_edge(1, 3)
    g1.add_edge(2, 3)
    coloring = solve_three_coloring(g1)
    assert coloring == None 
    print('Passed')

    print('--Test 2--')
    g2 = UndirectedGraph(6)
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    g2.add_edge(2, 3)
    g2.add_edge(3, 4)
    g2.add_edge(4, 5)
    g2.add_edge(0, 3)
    g2.add_edge(2, 4)
    coloring = solve_three_coloring(g2)
    print(coloring)
    assert coloring != None
    assert is_three_coloring(g2, coloring)
    print('Passed')

    print('-- Test 3 --')
    g2.add_edge(1,3)
    g2.add_edge(0, 2)
    coloring = solve_three_coloring(g2)
    print(coloring)
    assert coloring == None
    print('Passed')

    print('--- Test 4 ---')
    g1 = UndirectedGraph(5)
    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g1.add_edge(2, 0)
    g1.add_edge(1, 3)
    g1.add_edge(3, 4)
    g1.add_edge(1, 4)
    g1.add_edge(4, 0)
    coloring = solve_three_coloring(g1)
    print(coloring)
    assert is_three_coloring(g1, coloring) 
    print('Passed')

    print('-- Test 5 -- ')
    g2 = UndirectedGraph(7)
    g2.add_edge(2, 3)
    g2.add_edge(2, 1)
    g2.add_edge(2, 0)
    g2.add_edge(2, 4)
    g2.add_edge(3, 5)
    g2.add_edge(3, 6)
    g2.add_edge(5, 6)
    g2.add_edge(1, 0)
    g2.add_edge(1, 4)
    coloring = solve_three_coloring(g2)
    print(coloring)
    assert is_three_coloring(g2, coloring)
    print('Passed')

    print('--Test 6--')
    g2.add_edge(0, 4)
    coloring = solve_three_coloring(g2)
    assert coloring == None
    print('Passed')

    print('All test passed: 15 points!')
