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
- المطلوب: إيجاد إسناد (Truth Assignment) للمتغيرات (true أو false) يجعل الصيغة بأكملها صحيحة.

**إجابة Question 1 (حل المثال الموجود في الصورة):**
لتحقيق الصيغة: 
(x1 ∨ x2 ∨ ¬x4) ∧ (x1 ∨ ¬x2 ∨ ¬x3) ∧ (¬x1 ∨ ¬x2 ∨ ¬x3)

يمكننا اختيار الإسناد التالي:
x1 = True, x2 = False, x3 = False, x4 = False

التحقق:
- البند 1: True ∨ False ∨ True = True
- البند 2: True ∨ True ∨ True = True
- البند 3: False ∨ True ∨ True = True
بما أن جميع البنود صحيحة، فإن الصيغة محققة بالكامل.

================================================================
3. Code Implementation:
-----------------------
"""

class SATInstance:
    # Constructor: provide n the number of variables and
    # an initial list of clauses.
    # Note that variable numbers will go from 1 to n inclusive.
    # we can add clauses using the add_clause method.
    def __init__(self, n, clauses):
        self.n = n
        self.m = len(clauses)
        self.clauses = clauses
        assert self.is_valid()
    
    # is_valid
    # Check if all clauses are correct.
    # literals in each clause must be between 1 and n or -n and -1 
    def is_valid(self):
        assert self.n >= 1
        assert self.m >= 0
        for c in self.clauses:
            for l in c:
                assert (1 <= l and l <= self.n) or (-self.n <= l and l <= -1)
        return True
    
    # add_clause
    # Add a new clause to the list of clauses
    def add_clause(self, c):
        #check the clause we are adding.
        for l in c:
            assert (1 <= l and l <= self.n) or (-self.n <= l and l <= -1)
        self.clauses.append(c)
    
    ## Function: evaluate_literal
    # Evaluate a literal against a partial truth assignment
    # return 0 if the partial truth assignment does not have the variable corresponding to the literal
    # return 1 if the partial truth assignment has the variable and the literal is true
    # return -1 if the partial truth assignment has the variable and the literal is false
    def evaluate_literal(self, partial_truth_assignment, literal):
        var = abs(literal) # literal may be negated. First remove any negation using abs
        if var not in partial_truth_assignment:
            return 0
        v = partial_truth_assignment[var]
        if literal > 0: # Literal is positive (e.g., x1)
            return 1 if v else -1
        else: # Literal is negative (e.g., -x1)
            return -1 if v else 1
    
    ## Function: evaluate
    # See description above: partial_truth_assignment is a dictionary from 1 .. n to true/false.
    # since it is partial, we may have variables with no truth assignments.
    # use evaluate_literal function as a useful primitive
    # return +1 if the formula is already satisfied under partial_truth_assignment: i.e, all clauses are true
    # return 0 if formula is indeterminate under partial_truth_assignment, all clauses are true or unresolved and at least one clause is unresolved.
    # return -1 if formula is already violated under partial_truth_assignment, i.e, at least one clause is false
    def evaluate(self, partial_truth_assignment):
        unresolved_exists = False
        
        for clause in self.clauses:
            clause_status = -1  
            for literal in clause:
                lit_val = self.evaluate_literal(partial_truth_assignment, literal)
                
                if lit_val == 1:
                    clause_status = 1
                    break  
                
                if lit_val == 0:
                    clause_status = 0
            
            if clause_status == -1:
                return -1
            
            if clause_status == 0:
                unresolved_exists = True
        
        if unresolved_exists:
            return 0
        
        return 1

"""
================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: O(m * k) where m is the number of clauses and k is the average number of literals per clause.
  In the worst case, k can be as large as n (the number of variables), making the complexity O(m * n).
  The evaluate function iterates through all clauses and their literals until a clause is satisfied or determined to be false.

- Space Complexity: O(n + m)
  - O(n) to store the number of variables.
  - O(m) to store the list of clauses.
================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    print('-test1-')
    f1 = SATInstance(4, [ [ 1, 2, -4], [-2, -3, 1], [-1, -2, -3] ])
    t1 = {1:True, 2:False}
    e1 = f1.evaluate(t1)
    assert e1 == 1, f'Expected that f1 is satisfied by t1 but your code returns: {e1}'

    print('-test2-')
    t2 = {1:False, 2: False}
    e2 = f1.evaluate(t2)
    assert e2 == 0, f'Expected that f1 is indeterminate under t2. Your code returns: {e2}'

    print('-test3-')
    f2 = SATInstance(5, [[1,2,-5],[-4,-2,-1], [1, 3, 5], [-1, -5, -2], [1, 2, -4]])
    t3 = {1:True}
    e3 = f2.evaluate(t3)
    assert e3 == 0, f'Expected that f2 is indeterminate under t3. Your code returns {e3}' 

    print('-test4-')
    t4 = {1: True, 2: False}
    e4 = f2.evaluate(t4)
    assert e4 == 1, f'Expected that f2 is satisfied by t4. Your code returns {e4}'

    print('-test5-')
    t5 = {1: False, 3: False, 5:False}
    e5 = f2.evaluate(t5)
    assert e5 == -1, f'Expected that f2 is violated by t5. Your code returns {e5}'
    
    print('All tests passed: 10 points!')
