"""
Part 1: Implement Binary Search Tree (English & Arabic Explanation)
===================================================================
1. Problem Statement (English):
-------------------------------
We will begin by implementing binary search tree data structure in python.
Implement a BST with the following operations:
- __init__ (constructor)
- get_leftmost_descendant
- search
- insert
- height
- delete

===================================================================
2. Explanation (Arabic):
------------------------
الشجرة الثنائية للبحث (BST) هي هيكل بيانات يسمح بتخزين البيانات بشكل مرتب.
كل عقدة (Node) تحتوي على مفتاح (Key)، ومؤشرين للابن الأيسر والابن الأيمن، ومؤشر للأب (Parent).
الخصائص الأساسية للـ BST:
- كل المفاتيح في الشجرة الفرعية اليسرى < مفتاح العقدة الحالية.
- كل المفاتيح في الشجرة الفرعية اليمنى > مفتاح العقدة الحالية.
- لا نسمح بتكرار المفاتيح.

===================================================================
3. Code Implementation:
-----------------------
"""

class Node:
    # Implement a node of the binary search tree.
    # Constructor for a node with key and a given parent
    # parent can be None for a root node.
    def __init__(self, key, parent = None):
        self.key = key
        self.parent = parent
        self.left = None # We will set left and right child to None
        self.right = None
        # Make sure that the parent's left/right pointer
        # will point to the newly created node.
        if parent != None:
            if key < parent.key:
                assert(parent.left == None), 'parent already has a left child -- unable to create node'
                parent.left = self
            else:
                assert key > parent.key, 'key is same as parent.key. We do not allow duplicate keys in a BST since it breaks some of the algorithms.'
                assert(parent.right == None ), 'parent already has a right child -- unable to create node'
                parent.right = self

    # Utility function that keeps traversing left until it finds
    # the leftmost descendant
    def get_leftmost_descendant(self):
        if self.left != None:
            return self.left.get_leftmost_descendant()
        else:
            return self

    # TODO: Complete the search algorithm below
    # You can call search recursively on left or right child
    # as appropriate.
    # If search succeeds: return a tuple True and the node in the tree
    # with the key we are searching for.
    # Also note that if the search fails to find the key
    # you should return a tuple False and the node which would
    # be the parent if we were to insert the key subsequently.
    def search(self, key):
        if self.key == key:
            return (True, self)
        # your code here
        elif key < self.key:
            if self.left is not None:
                return self.left.search(key)
            else:
                return (False, self)
        else: # key > self.key
            if self.right is not None:
                return self.right.search(key)
            else:
                return (False, self)


    # TODO: Complete the insert algorithm below
    # To insert first search for it and find out
    # the parent whose child the currently inserted key will be.
    # Create a new node with that key and insert.
    # return None if key already exists in the tree.
    # return the new node corresponding to the inserted key otherwise.
    def insert(self, key):
        # your code here
        (found, node) = self.search(key)
        if found:
            return None
        # Create new node with the parent returned by search
        new_node = Node(key, node)
        return new_node


    # TODO: Complete algorithm to compute height of the tree
    # height of a node whose children are both None is defined
    # to be 1.
    # height of any other node is 1 + maximum of the height
    # of its children.
    # Return a number that is th eheight.
    def height(self):
        # your code here
        left_height = self.left.height() if self.left else 0
        right_height = self.right.height() if self.right else 0
        return 1 + max(left_height, right_height)


    # TODO: Write an algorithm to delete a key in the tree.
    # First, find the node in the tree with the key.
    # Recommend drawing pictures to visualize these cases below before
    # programming.
    # Case 1: both children of the node are None
    #   -- in this case, deletion is easy: simply find out if the node with key is its
    #      parent's left/right child and set the corr. child to None in the parent node.
    # Case 2: one of the child is None and the other is not.
    #   -- replace the node with its only child. In other words,
    #      modify the parent of the child to be the to be deleted node's parent.
    #      also change the parent's left/right child appropriately.
    # Case 3: both children of the parent are not None.
    #    -- first find its successor (go one step right and all the way to the left).
    #    -- function get_leftmost_descendant may be helpful here.
    #    -- replace the key of the node by its successor.
    #    -- delete the successor node.
    # return: no return value specified

    def delete(self, key):
        (found, node_to_delete) = self.search(key)
        assert(found == True), f"key to be deleted:{key}- does not exist in the tree"
        # your code here

        # Case 1: Both children are None
        if node_to_delete.left is None and node_to_delete.right is None:
            parent = node_to_delete.parent
            if parent:
                if parent.left == node_to_delete:
                    parent.left = None
                else:
                    parent.right = None

        # Case 2: One child is None
        elif node_to_delete.left is None:
            child = node_to_delete.right
            parent = node_to_delete.parent
            child.parent = parent
            if parent:
                if parent.left == node_to_delete:
                    parent.left = child
                else:
                    parent.right = child
        elif node_to_delete.right is None:
            child = node_to_delete.left
            parent = node_to_delete.parent
            child.parent = parent
            if parent:
                if parent.left == node_to_delete:
                    parent.left = child
                else:
                    parent.right = child

        # Case 3: Both children are not None
        else:
            # Find successor: one step right then all the way left
            successor = node_to_delete.right.get_leftmost_descendant()
            # Replace the key of the node with its successor's key
            node_to_delete.key = successor.key
            # Delete the successor node
            # The successor has NO left child (by definition), but may have a right child.
            parent_s = successor.parent
            child_s = successor.right
            if parent_s:
                if parent_s.left == successor:
                    parent_s.left = child_s
                else:
                    parent_s.right = child_s
                if child_s:
                    child_s.parent = parent_s

# --- Test Cases (from problem) ---
if __name__ == "__main__":
    print("Running basic tests...")
    t1 = Node(25, None)
    t2 = Node(12, t1)
    t3 = Node(18, t2)
    t4 = Node(40, t1)

    assert(t1.left == t2), 'test 1 failed'
    assert(t2.parent == t1),  'test 2 failed'
    assert(t2.right == t3), 'test 3 failed'
    assert (t3.parent == t2), 'test 4 failed'
    assert(t1.right == t4), 'test 5 failed'
    assert(t4.left == None), 'test 6 failed'
    assert(t4.right == None), 'test 7 failed'

    (b, found_node) = t1.search(18)
    assert b and found_node.key == 18, 'test 8 failed'
    (b, found_node) = t1.search(25)
    assert b and found_node.key == 25, 'test 9 failed'
    (b, found_node) = t1.search(26)
    assert(not b), 'test 10 failed'
    assert(found_node.key == 40), 'test 11 failed'

    ins_node = t1.insert(26)
    assert ins_node.key == 26, ' test 12 failed '
    assert ins_node.parent == t4,  ' test 13 failed '
    assert t4.left == ins_node,  ' test 14 failed '

    ins_node2 = t1.insert(33)
    assert ins_node2.key == 33, 'test 15 failed'
    assert ins_node2.parent == ins_node, 'test 16 failed'
    assert ins_node.right == ins_node2, 'test 17 failed'

    assert t1.height() == 4, 'test 18 failed'
    assert t4.height() == 3, 'test 19 failed'
    assert t2.height() == 2, 'test 20 failed'

    print("Success: 15 points.")

    print("\nRunning deletion tests...")
    # Recreate the tree for deletion tests
    t1 = Node(16, None)
    lst = [18,25,10, 14, 8, 22, 17, 12]
    for elt in lst:
        t1.insert(elt)

    t1.delete(8)
    (b8,n8) = t1.search(8)
    assert not b8, 'Test A: deletion fails to delete node.'
    (b,n) = t1.search(10)
    assert( b) , 'Test B failed: search does not work'
    assert n.left == None, 'Test C failed: Node 8 was not properly deleted.'

    assert n.right != None, 'Test D failed: node 10 should have right child 14'
    assert n.right.key == 14, 'Test E failed: node 10 should have right child 14'

    t1.delete(14)
    (b14, n14) = t1.search(14)
    assert not b14, 'Test F: Deletion of node 14 failed -- it still exists in the tree.'
    (b,n) = t1.search(10)
    assert n.right != None , 'Test G failed: deletion of node 14 not handled correctly'
    assert n.right.key == 12, f'Test H failed: deletion of node 14 not handled correctly: {n.right.key}'

    t1.delete(18)
    (b18, n18) = t1.search(18)
    assert not b18, 'Test I: Deletion of node 18 failed'
    assert t1.right.key == 22 , ' Test J: Replacement of node with successor failed.'
    assert t1.right.right.left == None, ' Test K: replacement of node with successor failed -- you did not delete the successor leaf properly?'

    print('-- All tests passed: 15 points!--')
