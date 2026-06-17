"""
Problem 1: Solving CNF Satisfiability Problem (English & Arabic Explanation)
=============================================================================
1. Problem Statement (English):
-------------------------------
We will first explore algorithms for solving the CNF Satisfiability problem.

The CNF SAT Problem:
You are given n Boolean variables x1, ..., xn that can take values true/false. You are also given a boolean formula in a special form called conjunctive normal form (CNF).
- The formula is the "and" (∧) of m clauses.
- Each clause is the "or" (∨) of k literals.
- Each literal is a variable xi or its logical negation ¬xi.

Example (CNF Formula):
Let n = 4 variables and 3 clauses as shown below:
C1: x1 or x2 or (not x4)
C2: (not x2 or not x3) or x1
C3: (not x1) or (not x2) or (not x3)

The SAT problem asks if there is a truth assignment for the variables that satisfies the entire formula.

Question 1: Find a truth assignment that satisfies the formula in the example above.

================================================================
2. Explanation (Arabic):
------------------------
المسألة تتعلق بـ "مسألة الإرضاء المنطقي" (SAT) للصيغ التي تكون على الشكل العادي الإقراني (CNF).
- الصيغة عبارة عن "و" (AND) لمجموعة من البنود (Clauses).
- كل بند عبارة عن "أو" (OR) لمجموعة من الحروف (Literals).
- الحرف قد يكون متغيراً `xi` أو نفيه `-xi`.

الكود المرفق يستخدم خوارزمية **DPLL (Davis-Putnam-Logemann-Loveland)** بنسختها الأساسية (البحث التراجعي/Backtracking):
1. تقوم الخوارزمية بتعيين قيمة (True/False) لمتغير `j`.
2. تقوم بتقييم الصيغة الحالية (باستخدام `formula.evaluate`).
3. إذا كانت الصيغة صحيحة، ترجع الحل.
4. إذا كانت الصيغة خاطئة، ترجع وتجرب القيمة المعاكسة للمتغير.
5. تكرر العملية لكل المتغيرات من 1 إلى `n` (عدد المتغيرات).

================================================================
3. Code Implementation:
-----------------------
"""

# ---------- SATInstance class ----------
class SATInstance:
    def __init__(self, n, clauses):
        self.n = n          # number of variables (1..n)
        self.clauses = clauses  # list of lists of literals (positive/negative integers)
    
    def add_clause(self, clause):
        self.clauses.append(clause)
    
    def evaluate(self, truth_assign):
        """
        Evaluate the formula under the (possibly partial) truth assignment.
        truth_assign : dict mapping variable (1..n) to bool (True/False)
        Returns:
             1  if all clauses are satisfied
            -1  if any clause is falsified
             0  otherwise (undetermined)
        """
        all_satisfied = True
        for clause in self.clauses:
            clause_satisfied = False
            clause_falsified = True  # assume all literals are falsified until proven otherwise
            for lit in clause:
                var = abs(lit)
                if var in truth_assign:
                    val = truth_assign[var]
                    if (lit > 0 and val) or (lit < 0 and not val):
                        # literal true → clause satisfied
                        clause_satisfied = True
                        clause_falsified = False
                        break
                    else:
                        # literal false
                        pass
                else:
                    # variable not assigned → clause is not falsified yet
                    clause_falsified = False
            if clause_satisfied:
                continue
            if clause_falsified:
                return -1  # formula falsified
            all_satisfied = False
        return 1 if all_satisfied else 0

# ---------- Helper functions ----------
def extend_truth_assignment(truth_assign, j, b):
    truth_assign[j] = b
    return truth_assign
    
def forget_var_in_truth_assign(truth_assign, j):
    if j in truth_assign:
        del truth_assign[j]
    return truth_assign

# ---------- DPLL algorithm ----------
def dpll_algorithm(formula, partial_truth_assign, j):
    print("j is " + str(j))
    assert 1 <= j and j <= formula.n
    assert j not in partial_truth_assign
    
    # Evaluate current partial assignment
    val = formula.evaluate(partial_truth_assign)
    if val == 1:          # formula satisfied
        return True, partial_truth_assign
    if val == -1:         # formula falsified
        return False, None
    
    # Try assigning j = True
    extend_truth_assignment(partial_truth_assign, j, True)
    if j == formula.n:
        if formula.evaluate(partial_truth_assign) == 1:
            return True, partial_truth_assign
    else:
        res, final = dpll_algorithm(formula, partial_truth_assign, j+1)
        if res:
            return True, final
    forget_var_in_truth_assign(partial_truth_assign, j)
    
    # Try assigning j = False
    extend_truth_assignment(partial_truth_assign, j, False)
    if j == formula.n:
        if formula.evaluate(partial_truth_assign) == 1:
            return True, partial_truth_assign
    else:
        res, final = dpll_algorithm(formula, partial_truth_assign, j+1)
        if res:
            return True, final
    forget_var_in_truth_assign(partial_truth_assign, j)
    
    return False, None

def solve_formula(formula):
    return dpll_algorithm(formula, {}, 1)

"""
================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: O(2^n) in the worst-case scenario, where n is the number of variables.
  Since the algorithm uses backtracking DFS without advanced heuristics like Unit Propagation, it effectively explores the entire binary decision tree (True/False for each variable).

- Space Complexity: O(n)
  - O(n) for the recursion stack depth.
  - O(n) for the `partial_truth_assign` dictionary.
================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    print('-- formula 1 --')
    f1 = SATInstance(4, [ [ 1, 2, -4], [-2, -3, 1], [-1, -2, -3] ])
    (e, t) = solve_formula(f1)
    print(e, t)
    assert e, 'f1 should be satisfiable'
    assert t != None, 'does not return a truth assignment'
    assert f1.evaluate(t) == 1, 'Truth assignment does not evaluate to expected value of true'

    print('-- formula 2 -- ')
    f2 = SATInstance(5, [[1,2,-5],[-4,-2,-1], [1, 3, 5], [-1, -5, -2], [1, 2, -4]])
    (e2, t2) = solve_formula(f2)
    print(e2, t2)
    assert e2, 'f2 must be satisfiable'
    assert t2 != None, 'does not return a truth assignment'
    assert f2.evaluate(t2) == 1, 'Truth assignment does not evaluate to expected value of true'

    print('--formula 3 --')
    f3 = SATInstance(5, [[1, 2, -5, -4], [1, 2, -5, 4], [-1], [-2,-5], [5]])
    (e3, t3) = solve_formula(f3)
    print(e3, t3)
    assert not e3, 'f3 is unsatisfiable'
    assert t3 == None

    print('--formula 4--')
    f4 = SATInstance(10, [
      [-1, -5, -4, 8],
      [1, 5, 8, 2],
       [2, 1, 3, 9],
        [-2, 4, 5, 6, -7],
        [-1, 2, -1, 7, 8],
        [2, -3, 1, 4, 9 ],
        [1, 10],
        [-10],
        [1, 5, 8, 3, 10]
    ])

    (e4, t4) = solve_formula(f4)
    print(e4, t4)
    assert e4, 'f4 must be satisfiable'
    assert t4 != None, 'does not return a truth assignment'
    assert f4.evaluate(t4) == 1, 'Truth assignment does not evaluate to expected value of true'

    print('--formula 5--')
    f5 = SATInstance(16,[
         [1, 2], [-2 , -4],[3, 4], [-4, -5], [5, -6], [6, -7], [6, 7], [7, -16],
         [8, -9],[8, -14], [9, 10], [9, -10], [-10, -11], [10, 12], [11, 12], [13, 14],
         [14, -15], [15, 16]])
    (e5, t5) = solve_formula(f5)
    print(e5, t5)
    assert e5, 'f5 is satisfiable'
    assert t5 != None
    assert f5.evaluate(t5) == 1, 'Truth assignment does not evaluate to expected value of true'

    print('All tests passed: 20 points')
