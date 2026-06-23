"""
Problem 2: Suffix Links for Suffix Trie (English & Arabic Explanation)
=======================================================================
1. Problem Statement (English):
-------------------------------
The inefficient algorithm for suffix trie construction did not construct suffix links. Suffix links are very important for algorithms such as finding the longest common substrings between two strings.

Recall the notion of suffix links:
- Every internal node `n` of the trie has a unique path from the root.
- The suffix link of an internal node `n` points to the longest proper suffix of the string represented by `n` that is also a node in the trie.

In this problem, we ask you to find an efficient algorithm for constructing suffix links in a suffix trie without expanding the whole trie with naive construction.
- The suffix link for the root is itself.
- Suppose for a node `n`, its suffix link for its parent node `p` is known. The idea is to traverse the tree using DFS and compute the suffix link for `n` based on `p`'s suffix link and the edge character.

=======================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب إنشاء روابط اللواحق (Suffix Links) داخل شجرة اللواحف (Suffix Trie) لتسريع البحث والتحليل النصي.

**الإجابات النظرية للأسئلة (A, B, C, D) الموجودة في الصور:**
(A) **Case-1: Parent is the root.**
إذا كانت العقدة `n` متصلة بالجذر `r` عبر حافة تمثل النص `s[lo..hi]`، فإن الرابط اللاحق `suff(n)` يمثله النص `s[lo+1..hi]` (أي نزع الحرف الأول فقط). 
(B) **Case-2: Parent is not the root.**
لإيجاد الرابط اللاحق `s(n)` للعقدة `n` انطلاقاً من الرابط اللاحق للأب `s(p)`، يجب علينا اجتياز نفس النص الموجود على الحافة من `p` إلى `n` (وهو `s[lo..hi]`) بدءاً من العقدة `s(p)`.
(C) **الرابط اللاحق لـ n8 في شجرة "BANANA$".**
العقدة `n8` متصلة بالجذر `n0` عبر حافة `"A"`. باستخدام قاعدة (A)، السلسلة المتبقية بعد نزع الحرف الأول هي `""` (فارغة). الرابط اللاحق للسلسلة الفارغة هو الجذر نفسه. **إذن الرابط اللاحق لـ n8 هو n0 (الجذر).**
(D) **الرابط اللاحق لـ n4 في شجرة "BANANA$".**
في شجرة `"BANANA$"`، العقدة `n4` تمثل السلسلة `"ANA"`. الرابط اللاحق لـ `"ANA"` يجب أن يكون العقدة التي تمثل أطول لاحقة موجودة في الشجرة، وهي `"NA"`. العقدة `n3` هي التي تمثل `"NA"`. **إذن الرابط اللاحق لـ n4 هو n3.**

=======================================================================
3. Code Implementation:
-----------------------
"""

import networkx as nx
from matplotlib import pyplot as plt

# ------------------- Base Trie Classes -------------------
class SuffixTrieNode:
    def __init__(self, node_id, orig_str):
        self.orig_str = orig_str
        self.outgoing_edges = {}
        self.suffix_link = None
        self.id = node_id
        self.depth = 0
        self.parent = None
        
    def is_root(self):
        return self.id == 0
        
    def get_edge(self, char):
        return self.outgoing_edges.get(char)
        
    def is_leaf(self):
        return False
    
    def add_suffix_link(self, node):
        self.suffix_link = node
        
    def add_outgoing_edge(self, new_edge):
        edge_init_char = new_edge.get_char_at(0)
        assert edge_init_char not in self.outgoing_edges
        assert new_edge.src.id == self.id
        self.outgoing_edges[edge_init_char] = new_edge
        new_edge.dest.parent = new_edge.src
        if not new_edge.is_leaf_edge():
            new_edge.dest.depth = self.depth + new_edge.length()
        
class SuffixTrieLeaf:
    def __init__(self, node_id, orig_str, suffix_start_pos):
        self.orig_str = orig_str
        self.id = node_id
        self.suffix_start_pos = suffix_start_pos
        self.parent = None
        
    def is_leaf(self):
        return True
    
class SuffixTrieEdge:
    def __init__(self, orig_str, src_node, dest_node, lo, hi):
        self.orig_str = orig_str
        self.lo = lo
        self.hi = hi
        self.src = src_node
        self.dest = dest_node
        
    def is_leaf_edge(self):
        return self.hi == -1
    
    def length(self):
        if self.hi == -1:
            return -1
        return self.hi - self.lo + 1
    
    def get_char_at(self, offs):
        return self.orig_str[self.lo + offs]
    
    def reset_hi_and_dest(self, new_dest, new_hi):
        self.hi = new_hi
        new_dest.parent = self.src
        new_dest.depth = self.src.depth + self.length()
        self.dest = new_dest

class TrieAddress:
    def __init__(self, node, edge=None, offs=0):
        self.node = node
        self.edge = edge
        self.offs = offs
        
    def traverse_next(self, c):
        if self.edge == None:
            new_edge = self.node.get_edge(c)
            if new_edge == None: return None
            if new_edge.is_leaf_edge() or new_edge.length() > 1:
                return TrieAddress(self.node, new_edge, 1)
            return TrieAddress(new_edge.dest, None, 0)
        else:
            edge = self.edge
            if edge.lo + self.offs < len(edge.orig_str) and edge.get_char_at(self.offs) == c:
                if edge.is_leaf_edge() or self.offs < edge.length() - 1:
                    return TrieAddress(self.node, self.edge, self.offs + 1)
                return TrieAddress(edge.dest, None, 0)
            return None
            
    def create_new_edge_at(self, orig_str, i, node_id):
        c = orig_str[i]
        node = self.node
        edge = self.edge
        offs = self.offs
        if edge == None:
            new_leaf = SuffixTrieLeaf(node_id, orig_str, i - node.depth)
            new_edge = SuffixTrieEdge(orig_str, node, new_leaf, i, -1)
            node.add_outgoing_edge(new_edge)
            return (node, new_leaf, False)
        else:
            node1 = SuffixTrieNode(node_id, orig_str)
            src_node = edge.src
            dest_node = edge.dest
            lo, hi = edge.lo, edge.hi
            edge.reset_hi_and_dest(node1, lo + offs - 1)
            new_edge_1 = SuffixTrieEdge(orig_str, node1, dest_node, lo + offs, hi)
            node1.add_outgoing_edge(new_edge_1)
            new_leaf = SuffixTrieLeaf(node_id + 1, orig_str, i - node1.depth)
            new_edge_2 = SuffixTrieEdge(orig_str, node1, new_leaf, i, -1)
            node1.add_outgoing_edge(new_edge_2)
            return (node1, new_leaf, True)

# ------------------- Construction Functions -------------------
def make_suffix_trie_simple(orig_str):
    root = SuffixTrieNode(0, orig_str)
    node_list = [root]
    for j in range(len(orig_str)):
        addr = TrieAddress(root)
        for i in range(j, len(orig_str)):
            addr1 = addr.traverse_next(orig_str[i])
            if addr1 == None:
                next_node, leaf_node, newly_created = addr.create_new_edge_at(orig_str, i, len(node_list))
                node_list.append(leaf_node)
                if newly_created: node_list.append(next_node)
                break
            addr = addr1
    return root

# ------------------- Core Logic: Add Suffix Links -------------------
def get_suffix_link_for_dest_node(edge):
    p = edge.src
    n = edge.dest
    assert p.suffix_link != None
    assert not edge.is_leaf_edge()
    
    orig_str = edge.orig_str
    lo = edge.lo
    hi = edge.hi
    
    # 1. Start from the suffix link of the parent
    curr_node = p.suffix_link
    curr_lo = lo
    target_len = hi - lo + 1
    
    # 2. Special Case: If the parent is the root
    if p.suffix_link == p:  # check if parent is root (root links to itself)
        curr_lo += 1
        target_len -= 1
        
        # If the edge consists of a single character, suffix is empty string -> root
        if target_len == 0:
            return p
            
    # 3. Skip-count traversal (Walk down the tree)
    while target_len > 0:
        first_char = orig_str[curr_lo]
        next_edge = curr_node.outgoing_edges[first_char]
        edge_len = next_edge.hi - next_edge.lo + 1
        
        if target_len >= edge_len:
            curr_node = next_edge.dest
            curr_lo += edge_len
            target_len -= edge_len
        else:
            # This should not happen for internal nodes as we always land on explicit nodes
            raise ValueError("Suffix link target falls inside an edge.")
            
    return curr_node

def add_all_suffix_links(root):
    root.add_suffix_link(root) # Root links to itself
    worklist = []
    
    for _, edge in root.outgoing_edges.items():
        if not edge.is_leaf_edge():
            worklist.append(edge)
            
    while worklist:
        edge = worklist.pop()
        n = edge.dest
        s_n = get_suffix_link_for_dest_node(edge)
        n.add_suffix_link(s_n)
        
        for _, next_edge in n.outgoing_edges.items():
            if not next_edge.is_leaf_edge():
                worklist.append(next_edge)

# ------------------- Verification & Visualization -------------------
def check_suffix_links(root):
    worklist = [root]
    all_nodes = [root]
    d = {0: ""}
    while worklist:
        n = worklist.pop()
        str_n = d[n.id]
        for _, e in n.outgoing_edges.items():
            if not e.is_leaf_edge():
                str_e = str_n + e.orig_str[e.lo:e.hi+1]
                d[e.dest.id] = str_e
                worklist.append(e.dest)
                all_nodes.append(e.dest)
    for n in all_nodes:
        assert n.suffix_link != None
        s_n = n.suffix_link
        s1, s2 = d[n.id], d[s_n.id]
        assert s1[1:] == s2, f'Node {n.id} string {s1} mismatch suffix {s2}'
    print("All suffix links validated successfully!")

def draw_networkx_graph(root, end=-1):
    G = nx.DiGraph()
    node_labels = {}
    edge_str_label = {}
    suffix_links = []
    leaf_nodes = []
    internal_nodes = []
    
    worklist = [root]
    while worklist:
        node = worklist.pop()
        G.add_node(node.id)
        if node.is_leaf():
            leaf_nodes.append(node.id)
            node_labels[node.id] = f"l{node.id}"
            continue
        internal_nodes.append(node.id)
        node_labels[node.id] = f"n{node.id}"
        if node.suffix_link:
            suffix_links.append((node.id, node.suffix_link.id))
        for _, edge in node.outgoing_edges.items():
            G.add_edge(edge.src.id, edge.dest.id)
            edge_str_label[(edge.src.id, edge.dest.id)] = edge.get_sub_str(end)
            worklist.append(edge.dest)
            
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    nx.draw_networkx_nodes(G, pos, nodelist=internal_nodes, node_shape="s", node_color="lightcyan")
    nx.draw_networkx_nodes(G, pos, nodelist=leaf_nodes, node_shape="s", node_color="lightgreen")
    nx.draw_networkx_edges(G, pos, width=2.0)
    nx.draw_networkx_labels(G, pos, labels=node_labels)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_str_label, font_color='blue', rotate=False)
    nx.draw_networkx_edges(G, pos, edgelist=suffix_links, style='dashed', edge_color='r', connectionstyle='arc3,rad=0.2')
    plt.axis("off")
    plt.show()

"""
=======================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Constructing the Suffix Trie (Naively): O(n^2) time, O(n^2) space in worst case.
- Building Suffix Links (add_all_suffix_links): O(n) time.
  Because the `add_all_suffix_links` function performs a single Depth-First or Breadth-First traversal over the internal nodes.
  For each node, finding the suffix link via `get_suffix_link_for_dest_node` takes amortized O(1) time by jumping down the tree using the known lengths of edges.
=======================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    print("--- Test 1: ALFALFA$ ---")
    root1 = make_suffix_trie_simple("ALFALFA$")
    add_all_suffix_links(root1)
    check_suffix_links(root1)
    draw_networkx_graph(root1)

    print("\n--- Test 2: BANANA$ ---")
    root2 = make_suffix_trie_simple("BANANA$")
    add_all_suffix_links(root2)
    check_suffix_links(root2)
    draw_networkx_graph(root2)

    print("\n--- Test 3: mamamia$ ---")
    root3 = make_suffix_trie_simple("mamamia$")
    add_all_suffix_links(root3)
    check_suffix_links(root3)
    draw_networkx_graph(root3)

    print("\nAll Tests Passed Successfully!")
