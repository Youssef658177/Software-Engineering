"""
Problem 2: Use SAT solver to solve 3-coloring problem (English & Arabic Explanation)
=====================================================================================
1. Problem Statement (English):
-------------------------------
The 3-color problem asks given an undirected graph G, whether it can be colored with 3 or fewer colors. I.e., assign each vertex of the graph one of three colors, say Red, Blue, Green such that vertices connected by an edge should not have the same color.

Part A: Given a graph G and a proposed 3-coloring represented as a map from vertices to colors {1, 2, 3}, check that it is a valid three coloring of the graph.

Part B (Implicit): Using the SAT solver (DPLL algorithm) implemented in the previous assignment, encode the 3-coloring problem into CNF form and solve it to find a valid coloring if one exists.

=====================================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب حل مشكلة تلوين الرسم البياني بـ 3 ألوان (3-Coloring).
- الجزء A يقوم فقط بالتحقق من صحة تلوين مُقترح (الجزء الذي كتبته أنت).
- الجزء B (الأهم) يقوم بتحويل الرسم البياني إلى صيغة منطقية (CNF) يتم إدخالها إلى خوارزمية DPLL لإيجاد حل تلقائياً.

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


# ---------- Part B: SAT Encoder and DPLL Solver ----------
class SATInstance:
    def __init__(self, n, clauses):
        self.n = n          # number of variables (1..n)
        self.clauses = clauses  # list of lists of literals
    
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

def dpll_algorithm(formula, partial_truth_assign, j):
    val = formula.evaluate(partial_truth_assign)
    if val == 1: return True, partial_truth_assign
    if val == -1: return False, None
    if j > formula.n: return False, None
    
    # Assign j = True
    partial_truth_assign[j] = True
    res, final = dpll_algorithm(formula, partial_truth_assign, j+1)
    if res: return True, final
    del partial_truth_assign[j]
    
    # Assign j = False
    partial_truth_assign[j] = False
    res, final = dpll_algorithm(formula, partial_truth_assign, j+1)
    if res: return True, final
    del partial_truth_assign[j]
    
    return False, None

def solve_formula(formula):
    return dpll_algorithm(formula, {}, 1)

def solve_three_coloring(graph):
    """Finds a valid 3-coloring using DPLL if one exists, else returns None."""
    n = graph.n
    # Variables: x_{v, c} is represented by integer `v * 3 + c` (where c is 1, 2, 3)
    # Total variables = n * 3 (numbered 1 to n*3)
    num_vars = n * 3
    clauses = []
    
    # Constraint 1: Each vertex has at least one color
    for v in range(n):
        clauses.append([v * 3 + 1, v * 3 + 2, v * 3 + 3])
        
    # Constraint 2: Each vertex has at most one color (pairwise exclusion)
    for v in range(n):
        clauses.append([-(v * 3 + 1), -(v * 3 + 2)])
        clauses.append([-(v * 3 + 1), -(v * 3 + 3)])
        clauses.append([-(v * 3 + 2), -(v * 3 + 3)])
        
    # Constraint 3: Adjacent vertices have different colors
    for (u, v) in graph.get_list_of_edges():
        for c in range(1, 4):
            clauses.append([-(u * 3 + c), -(v * 3 + c)])
            
    sat_problem = SATInstance(num_vars, clauses)
    sat_status, assignment = solve_formula(sat_problem)
    
    if not sat_status:
        return None
    
    # Convert SAT variable assignment back to coloring dict
    coloring = {}
    for v in range(n):
        for c in range(1, 4):
            if assignment.get(v * 3 + c) == True:
                coloring[v] = c
                break
    return coloring

"""
=====================================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Checking validity (is_three_coloring): O(V + E).
- SAT Encoding: O(V * 3 + E * 3) clauses generated.
- DPLL Solving (solve_three_coloring): O(2^n) worst case, where n is the number of vertices. 
  However, in practice, DPLL performs much better. The 3-coloring problem is NP-Complete.
=====================================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    print('--- Test 1 ---')
    g1 = UndirectedGraph(5)
    g1.add_edge(0, 1); g1.add_edge(1, 2); g1.add_edge(2, 0)
    g1.add_edge(1, 3); g1.add_edge(3, 4); g1.add_edge(1, 4); g1.add_edge(4, 0)
    
    coloring1 = {0:1, 1:2, 2:3, 3:1, 4:3}
    assert is_three_coloring(g1, coloring1), 'Test 1 fail: Coloring should be valid.'

    print('--- Test 2 ---')
    g2 = UndirectedGraph(7)
    g2.add_edge(2, 3); g2.add_edge(2, 1); g2.add_edge(2, 0); g2.add_edge(2, 4)
    g2.add_edge(3, 5); g2.add_edge(3, 6); g2.add_edge(5, 6)
    g2.add_edge(1, 0); g2.add_edge(1, 4); g2.add_edge(0, 4)
    
    coloring2 = {2: 1, 3: 2, 4: 2, 0: 1, 1: 3, 5: 3, 6: 1}
    assert not is_three_coloring(g2, coloring2), 'Test 2 fail: Coloring should be invalid.'

    print('--- Test 3 ---')
    coloring3 = {2: 3, 3: 2, 4: 2, 0: 2, 1: 1, 5: 3, 6: 1}
    assert not is_three_coloring(g2, coloring3), 'Test 3 fail: Coloring should be invalid.'
    
    print('--- Test 4 (SAT Solver Test) ---')
    print("Using DPLL SAT solver to find a valid 3-coloring for g1...")
    sat_result = solve_three_coloring(g1)
    print(f"SAT Solver Result: {sat_result}")
    assert sat_result is not None, 'SAT Solver failed to find a valid coloring for g1.'
    assert is_three_coloring(g1, sat_result), 'SAT Solver returned an invalid coloring!'
    print("SAT Solver passed for g1.")
    
    print('All Tests Passed (10 points)!')
