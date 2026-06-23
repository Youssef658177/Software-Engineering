"""
Problem Set 4 - Problem 1: B-Tree Insertion with Lending Scheme (English & Arabic Explanation)
===============================================================================================
1. Problem Statement (English):
-------------------------------
We will revisit the insertion algorithm for B-Trees. Recall that the insertion algorithm presented in class was rather simple. If a node is full, we split it into two. If needed, we will insert a new key into the parent. This process goes up the tree.

For this problem, we would like to implement the "lending scheme" similar to the "borrowing scheme" for key deletion. The key idea is that if a node is over-full (has 2d + 1 keys) as a result of an insertion, we perform the following steps:
1. Check if the node has a right sibling and it has < 2d keys. If so, shift the rightmost key up to the parent node and the key from the parent node as the leftmost key of the right sibling.
2. Check if the node has a left sibling and it has < 2d keys. If so, shift the leftmost key up to the parent node and the key from the parent node as the rightmost key of the left sibling.
3. If both conditions fail, split the node into two according to the median and insert a parent at the leaf.

The advantages are:
(a) Efficiency (fewer key exchanges).
(b) Balance (splitting only happens when the node and its siblings are at capacity).

===============================================================================================
2. Explanation (Arabic):
------------------------
في هذه المسألة، نعدل خوارزمية الإدراج في شجرة B-Tree باستخدام تقنية "الإعارة" (Lending Scheme).
عندما تصبح عقدة ممتلئة (عدد مفاتيحها = `2d + 1`) بعد إدراج مفتاح جديد، بدلاً من تقسيمها (Split) فوراً، نقوم بالآتي:

1. **محاولة الإعارة لليمين:** إذا كان للعقدة "شقيق أيمن" (Right Sibling) وعدد مفاتيحه أقل من `2d`، نقوم بنقل أكبر مفتاح في العقدة الحالية إلى العقدة الأب (كبديل للمفتاح الفاصل)، وننزل المفتاح الفاصل من الأب ليكون أول مفتاح في الشقيق الأيمن. (مع نقل المؤشرات المناسبة إذا لم تكن عقدة ورقية).
2. **محاولة الإعارة لليسار:** إذا لم ينجح الشرط الأول، نتحقق من وجود "شقيق أيسر" (Left Sibling) به مساحة. نقوم بنقل أصغر مفتاح في العقدة الحالية للأب، وننزل المفتاح الفاصل من الأب ليكون آخر مفتاح في الشقيق الأيسر.
3. **التقسيم (Split):** إذا فشلت الحالتان (أي أن كلا الشقيقين ممتلئين أيضاً)، نلجأ للتقسيم التقليدي للعقدة إلى قسمين ورفع المفتاح الأوسط للأب.

الكود التالي يطبق هذه الخوارزمية بالكامل، مع اختبارات تتحقق من صحة التوزيع.

===============================================================================================
3. Code Implementation:
-----------------------
"""

import networkx as nx
from matplotlib import pyplot as plt

# ------------------- Part 1: Base Node Class -------------------
class BTreeNodeBase(object):
    def __init__(self, keys = [], ptrs = [], is_root=False, d = 10):
        self.keys = list(keys)
        self.d = d
        self.pointers = list(ptrs)
        self.is_root = is_root
        self.parent = None
        
    def is_leaf(self):
        return len(self.pointers) == 0
    
    def set_parent(self, parent_node, idx):
        assert parent_node != None
        assert 0 <= idx < len(parent_node.pointers)
        assert parent_node.pointers[idx] == self
        self.parent = (parent_node, idx)
    
    def find_key_internal(self, k):
        n = len(self.keys)
        if n == 0:
            return None
        i = 0
        while i < n and self.keys[i] < k:
            i = i + 1
        if i < n and self.keys[i] == k:
            return (self, i)
        else:
            if self.is_leaf():
                return None
            else:
                return self.pointers[i].find_key_internal(k)
            
    def find_key(self, k):
        assert self.is_root
        res = self.find_key_internal(k)
        return True if res != None else False 
    
    def find_successor(self, idx):
        assert idx >= 0 and idx < len(self.keys)
        assert not self.is_leaf()
        child = self.pointers[idx+1]
        while not child.is_leaf():
            child = child.pointers[0]
        return (child.keys[0], child)
    
    def __str__(self):
        return str(self.keys)
    
    def make_networkx_graph(self, G, node_id, parent_id, label_dict):
        node_label = str(self.keys)
        if self.parent != None:
            node_label =  "C"+str(self.parent[1]) + ": " + node_label
        else:
            node_label = "R: "+ node_label
        G.add_node(node_id, label=node_label)
        label_dict[node_id] = node_label
        if parent_id >= 0:
            G.add_edge(parent_id, node_id)
        n = len(self.pointers)
        new_id = node_id+1
        for i in range(n):
            new_id = self.pointers[i].make_networkx_graph(G, new_id, node_id, label_dict)
        return new_id + 1
    
    def rep_ok(self):
        n = len(self.keys)
        p = len(self.pointers)
        d = self.d
        assert p == 0 or p == n + 1
        for i in range(1, n):
            assert self.keys[i] > self.keys[i-1]
        if self.is_root:
            assert self.parent == None
            assert 0 <= n <= 2 * d
            self.check_height_properties()
        else:
            assert self.parent != None
            assert d <= n <= 2 * d
        if p >= 1:
            for (j, child_node) in enumerate(self.pointers):
                assert child_node.parent == (self, j)
                assert child_node.d == self.d
                assert not child_node.is_root
                child_node.rep_ok()
    
    def check_height_properties(self):
        if self.is_leaf():
            return 0
        else:
            depths= [child.check_height_properties() for child in self.pointers]
            assert all(di == depths[0] for di in depths)
            return 1 + depths[0]
        
    def create_new_instance(self, keys, ptrs, is_root, d):
        return BTreeNodeBase(keys, ptrs, is_root, d)


# ------------------- Part 2: Insertion with Lending Scheme -------------------
class BTreeNodeWithInsert(BTreeNodeBase):
    
    def __init__(self, keys = [], ptrs = [], is_root=False, d = 10):
        super().__init__(keys, ptrs, is_root, d)
        
    def create_new_instance(self, keys, ptrs, is_root, d):
        return BTreeNodeWithInsert(keys, ptrs, is_root, d)
    
    def insert(self, new_key):
        assert self.is_root
        res = self.insert_helper(new_key)
        if res != None:
            (mid_key, n1, n2) = res
            self.is_root = False
            new_root = self.create_new_instance([mid_key], [n1, n2], True, self.d)
            n1.set_parent(new_root, 0)
            n2.set_parent(new_root, 1)
            return new_root
        else:
            return self
    
    def insert_helper(self, new_key):
        if self.is_leaf():
            self.insert_key_into_list(new_key)
            n = len(self.keys)
            if n <= 2 * self.d:
                return None
            else:
                return self.handle_full_node()
        else:
            i = 0
            n = len(self.keys)
            while i < n and self.keys[i] < new_key:
                i = i + 1
            if i < n and self.keys[i] == new_key:
                return None
            else:
                res = self.pointers[i].insert_helper(new_key)
                if res != None:
                    (mid_key, node_left, node_right) = res
                    self.insert_key_and_ptr(mid_key, node_left, node_right, i)
                    if len(self.keys) == 2 * self.d + 1:
                        return self.handle_full_node()
            
    def insert_key_into_list(self, new_key):
        assert self.is_leaf()
        assert new_key not in self.keys
        self.keys.append(new_key)
        i = len(self.keys) - 1
        while i >= 1 and self.keys[i] < self.keys[i-1]:
            self.keys[i-1], self.keys[i] = self.keys[i], self.keys[i-1]
            i = i-1
            
    def insert_key_and_ptr(self, mid_key, node_left, node_right, i):
        n = len(self.keys)
        assert i >= 0 and i <= n
        node_left.set_parent(self, i)
        assert self.pointers[i] == node_left 
        new_key, new_child = mid_key, node_right
        for j in range(i, n):
            self.keys[j], new_key = new_key, self.keys[j]
            self.pointers[j+1], new_child = new_child, self.pointers[j+1]
            self.pointers[j+1].set_parent(self, j+1)
        self.keys.append(new_key)
        self.pointers.append(new_child)
        new_child.set_parent(self, n+1)
        
    def fix_parent_pointers_for_children(self):
        for (j, child_node) in enumerate(self.pointers):
            child_node.set_parent(self, j)
        
    def split_node_into_two(self):
        assert len(self.keys) == 2 * self.d + 1
        d = self.d
        med_key = self.keys[d]
        new_keys = list(self.keys[d+1:])
        self.keys = list(self.keys[:d])
        if self.is_leaf():
            new_ptrs = []
        else:
            new_ptrs = list(self.pointers[d+1:])
            self.pointers = list(self.pointers[:d+1])
        new_node = self.create_new_instance(new_keys, new_ptrs, False, d)
        new_node.fix_parent_pointers_for_children()
        return (med_key, self, new_node)
    
    def handle_full_node(self, debug=True):
        """
        Core logic of the Lending Scheme.
        1. Try to lend a key to the Right Sibling.
        2. Try to lend a key to the Left Sibling.
        3. If both are full, Split the node.
        """
        assert len(self.keys) == 2 * self.d + 1
        d = self.d
        
        # Case: Root is full, must split
        if self.parent == None:
            return self.split_node_into_two()
            
        (parent_node, parent_idx) = self.parent
        
        # 1. Lend to Right Sibling
        if parent_idx + 1 < len(parent_node.pointers):
            right_sibling = parent_node.pointers[parent_idx + 1]
            if len(right_sibling.keys) < 2 * d:
                # Move parent key down to left of right sibling
                parent_key = parent_node.keys[parent_idx]
                right_sibling.keys.insert(0, parent_key)
                # Move rightmost key of current node up to parent
                moved_up_key = self.keys.pop()
                parent_node.keys[parent_idx] = moved_up_key
                # Move pointer if internal
                if not self.is_leaf():
                    moved_ptr = self.pointers.pop()
                    right_sibling.pointers.insert(0, moved_ptr)
                # Fix parents
                self.fix_parent_pointers_for_children()
                right_sibling.fix_parent_pointers_for_children()
                return None

        # 2. Lend to Left Sibling
        if parent_idx - 1 >= 0:
            left_sibling = parent_node.pointers[parent_idx - 1]
            if len(left_sibling.keys) < 2 * d:
                # Move parent key down to right of left sibling
                parent_key = parent_node.keys[parent_idx - 1]
                left_sibling.keys.append(parent_key)
                # Move leftmost key of current node up to parent
                moved_up_key = self.keys.pop(0)
                parent_node.keys[parent_idx - 1] = moved_up_key
                # Move pointer if internal
                if not self.is_leaf():
                    moved_ptr = self.pointers.pop(0)
                    left_sibling.pointers.append(moved_ptr)
                # Fix parents
                self.fix_parent_pointers_for_children()
                left_sibling.fix_parent_pointers_for_children()
                return None
                
        # 3. No available siblings, perform Split
        return self.split_node_into_two()


# ------------------- Part 3: Visualization Helper -------------------
def draw_btree_graph(n):
    G = nx.DiGraph()
    labels = {}
    n.make_networkx_graph(G, 0, -1, labels)
    try:
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    except:
        # Fallback if graphviz is not installed
        pos = nx.spring_layout(G)
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    nx.draw(G, pos=pos, with_labels=True, node_shape="s", font_size=8, labels=labels, node_color="none", bbox=dict(facecolor="cyan", edgecolor='black'))
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()


"""
===============================================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Insertion: O(log_d n) steps down the tree. 
  The `handle_full_node` operation, when lending works, is O(d). In the worst case (splitting), it is O(d). 
  Since d is a constant, the amortized time complexity of the insertion is O(log_d n).

- Space Complexity: O(n) to store the B-Tree nodes and their keys.
  The recursive stack depth is O(log_d n).
===============================================================================================
"""

# ------------------- Part 4: Test Cases -------------------
if __name__ == "__main__":
    # Test 1: Lend to Right Sibling
    lst1 = [1, 5, 2, 4, -4, -3, -7, 12]
    b1 = BTreeNodeWithInsert(d=2, is_root=True)
    for k in lst1:
        b1 = b1.insert(k)
    b1.rep_ok()
    print('Test 1 - Starting tree:')
    draw_btree_graph(b1)

    b1 = b1.insert(-8)
    b1.rep_ok()
    draw_btree_graph(b1)
    assert len(b1.keys) == 1
    assert b1.keys[0] == 1
    assert b1.pointers[0].keys == [-8,-7, -4, -3]
    assert b1.pointers[1].keys == [2,4,5, 12]
    print('Test 1: Lending to Right Sibling Passed!\n')


    # Test 2: Lend to Left Sibling
    lst2 = [1, 5, 2, 4, -4, 3, 7]
    b2 = BTreeNodeWithInsert(d=2, is_root=True)
    for k in lst2:
        b2 = b2.insert(k)
    b2.rep_ok()
    print('Test 2 - Starting tree:')
    draw_btree_graph(b2)

    b2 = b2.insert(8)
    b2.rep_ok()
    draw_btree_graph(b2)
    assert len(b2.keys) == 1
    assert b2.keys[0] == 3
    assert b2.pointers[0].keys == [-4, 1, 2]
    assert b2.pointers[1].keys == [4, 5, 7, 8]
    print('Test 2: Lending to Left Sibling Passed!\n')

    b2 = b2.insert(6)
    b2.rep_ok()
    draw_btree_graph(b2)
    assert len(b2.keys) == 1
    assert b2.keys[0] == 4
    assert b2.pointers[0].keys == [-4, 1, 2, 3]
    assert b2.pointers[1].keys == [5, 6, 7, 8]
    print('Test 2 (continued): Lending to Left Sibling Passed!\n')


    # Test 3: Stress Test with small `d`
    lst3 = [1, 5, 2, 4, 3, 9, 15, -5, 12, 18, 80, -25, 22, 31, -15, 14, 21, -24, 19]
    b3 = BTreeNodeWithInsert(d=1, is_root=True)
    for k in lst3:
        b3 = b3.insert(k)
    b3.rep_ok()
    draw_btree_graph(b3)
    
    for k in lst3:
        assert b3.find_key(k), f'Key {k} not found!'
    print('All Keys found correctly in Test 3')
    print('All Tests Passed Successfully!')
