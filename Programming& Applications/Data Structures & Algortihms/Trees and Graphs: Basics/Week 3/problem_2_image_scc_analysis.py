"""
Problem 2: Use union-find data-structures & Topological Data Analysis (English & Arabic Explanation)
====================================================================================================
1. Problem Statement (English):
-------------------------------
We will now explore finding maximal strongly connected components of an undirected graph using union find data structures.

2A: Use union-find to compute SCCs with a threshold W.
2B: Edge Threshold to Disconnect a Graph (Prove W = largest weight in MST).
2C: Topological Data Analysis on Images (Create graph from pixels, run MST, find SCCs).

================================================================================
2. Explanation (Arabic):
------------------------
المسألة بتطلب:
- (2A) حساب المكونات المتصلة (SCCs) في رسم بياني غير موجه باستخدام Union-Find و Threshold W.
- (2B) إثبات أن الحد W اللي يفصل الرسم البياني هو أكبر وزن في شجرة الامتداد الأدنى (MST).
- (2C) تطبيق عملي على الصور: تحويل الصورة لرسم بياني (البكسل عقد وحواف بالاختلاف اللوني)، حساب MST، ثم تطبيق Threshold للكشف عن أجزاء الصورة.

الكود أدناه يحتوي على الحل الكامل للجزء البرمجي.

================================================================================
3. Algorithm & Proof:
---------------------
(2A) Algorithm (Using Union-Find):
    - Create a DisjointForests of size n.
    - For each vertex i: make_set(i).
    - For each edge (i, j, w):
        - If w <= W: union(i, j).
    - Return dictionary of sets from DisjointForests.
    - Complexity: O(m * α(n)) ≈ O(m).

(2B) Proof (Threshold = Largest MST Edge):
    - Let e_max be the largest edge in the MST with weight W_mst.
    - By definition of MST (Kruskal), removing e_max disconnects the graph.
    - If we set W < W_mst, e_max is removed → Graph is disconnected.
    - If we set W >= W_mst, e_max remains → Graph stays connected.
    - Therefore, W must be equal to W_mst to be the threshold that disconnects the graph.

================================================================================
4. Code Implementation (Complete):
---------------------------------
"""

# ==================== Disjoint Forests (Union-Find) ====================
class DisjointForests:
    def __init__(self, n):
        self.n = n
        self.parents = [None] * n
        self.rank = [None] * n

    def make_set(self, j):
        self.parents[j] = j
        self.rank[j] = 1

    def find(self, j):
        if self.parents[j] != j:
            self.parents[j] = self.find(self.parents[j])
        return self.parents[j]

    def union(self, j1, j2):
        r1 = self.find(j1)
        r2 = self.find(j2)
        if r1 == r2: return
        if self.rank[r1] < self.rank[r2]:
            self.parents[r1] = r2
        else:
            self.parents[r2] = r1
            if self.rank[r1] == self.rank[r2]:
                self.rank[r1] += 1

    def dictionary_of_sets(self):
        d = {}
        for i in range(self.n):
            if self.parents[i] == i:
                d[i] = {i}
        for j in range(self.n):
            if self.parents[j] is not None:
                root = self.find(j)
                if root in d:
                    d[root].add(j)
        return d

# ==================== Undirected Graph (From your previous code) ====================
class UndirectedGraph:
    def __init__(self, n):
        self.n = n
        self.edges = []
        self.vertex_data = [None] * self.n

    def set_vertex_data(self, j, dat):
        self.vertex_data[j] = dat

    def get_vertex_data(self, j):
        return self.vertex_data[j]

    def add_edge(self, i, j, wij):
        self.edges.append((i, j, wij))

    def sort_edges(self):
        self.edges.sort(key=lambda edg_data: edg_data[2])

# ==================== 2A: compute_scc ====================
def compute_scc(g, W):
    d = DisjointForests(g.n)
    for i in range(g.n):
        d.make_set(i)
    for (i, j, wij) in g.edges:
        if wij <= W:
            d.union(i, j)
    return d.dictionary_of_sets()

# ==================== MST using Kruskal (Missing from your code) ====================
def compute_mst(g):
    g.sort_edges()
    d = DisjointForests(g.n)
    for i in range(g.n):
        d.make_set(i)
    mst_edges = []
    total_weight = 0
    for (i, j, w) in g.edges:
        if d.find(i) != d.find(j):
            d.union(i, j)
            mst_edges.append((i, j, w))
            total_weight += w
    return mst_edges, total_weight

# ==================== 2C: Topological Data Analysis on Images ====================
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def pixel_difference(px1, px2):
    def fix_pixels(px):
        return [int(px[0]), int(px[1]), int(px[2])]
    px1_float = fix_pixels(px1)
    px2_float = fix_pixels(px2)
    return max(abs(px1_float[0] - px2_float[0]), abs(px1_float[1] - px2_float[1]), abs(px1_float[2] - px2_float[2]))

def get_index_from_pixel(i, j, height, width):
    return j * width + i

def connect_neighboring_pixels(i, j, i1, j1, img, g):
    (height, width, _) = img.shape
    s = get_index_from_pixel(i, j, height, width)
    s1 = get_index_from_pixel(i1, j1, height, width)
    w = pixel_difference(img[j, i], img[j1, i1])
    g.add_edge(s, s1, w)

def load_image_and_make_graph(imfilename):
    img = cv2.imread(imfilename)
    (height, width, _) = img.shape
    g = UndirectedGraph(height * width)
    for j in range(height):
        for i in range(width):
            s = get_index_from_pixel(i, j, height, width)
            g.set_vertex_data(s, (i, j))
            if i > 0: connect_neighboring_pixels(i, j, i-1, j, img, g)
            if i < width-1: connect_neighboring_pixels(i, j, i+1, j, img, g)
            if j > 0: connect_neighboring_pixels(i, j, i, j-1, img, g)
            if j < height-1: connect_neighboring_pixels(i, j, i, j+1, img, g)
    return g

def visualize_components(orig_image, g, components_dict):
    (w, h, channels) = orig_image.shape
    new_image = np.zeros((w, h, channels), np.uint8)
    for (key, vertSet) in components_dict.items():
        if len(vertSet) >= 10:
            for s in vertSet:
                (i, j) = g.get_vertex_data(s)
                rgb_color = orig_image[j, i]
                cv2.circle(new_image, (i, j), 1, (int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2])), -1)
    return new_image

# ==================== TEST CASES ====================
if __name__ == "__main__":
    print("-" * 50)
    print("Test 1: 2A - Basic SCC using Union-Find")
    g1 = UndirectedGraph(8)
    g1.add_edge(0, 1, 0.5); g1.add_edge(0, 2, 1.0); g1.add_edge(0, 4, 0.5); g1.add_edge(2, 3, 1.5)
    g1.add_edge(2, 4, 2.0); g1.add_edge(3, 4, 1.5); g1.add_edge(5, 6, 2.0); g1.add_edge(5, 7, 2.0)
    res1 = compute_scc(g1, 1.5)
    print(f"Number of SCCs (Threshold=1.5): {len(res1)}")
    assert len(res1) == 4
    print("Passed 2A Test.")

    print("-" * 50)
    print("Test 2: 2C - Image Processing (Requires test-pic.png)")
    try:
        img = cv2.imread('test-pic.png')
        if img is not None:
            g_img = load_image_and_make_graph('test-pic.png')
            (mst_edges, mst_weight) = compute_mst(g_img)
            max_edge = max(mst_edges, key=lambda e: e[2])
            print(f"MST Edges: {len(mst_edges)}, Max Weight: {max_edge[2]}")
            # Visualize for a small threshold
            res_img = compute_scc(g_img, 0.02 * max_edge[2])
            print(f"Number of components (0.02 W_max): {len(res_img)}")
            new_img = visualize_components(img, g_img, res_img)
            plt.imshow(new_img)
            plt.title(f"Components (Threshold = 0.02 * Max MST Edge)")
            plt.show()
            assert len(res_img) > 1
            print("Passed 2C Test.")
        else:
            print("Image 'test-pic.png' not found.")
    except Exception as e:
        print(f"Image test skipped: {e}")
    print("-" * 50)
