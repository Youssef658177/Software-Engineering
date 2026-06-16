"""
Solving Image Maze (With Solution) - English & Arabic Explanation
==================================================================

1. Problem Statement (English):
-------------------------------
Given a maze as an image with a start and end point, we would like to write code to solve the maze.

An image is a 2D matrix of pixels. Each pixel has a color (Red, Green, Blue). We view the image as a graph where each pixel is a vertex, and edges connect a pixel to its neighbor.

The weight of an edge is the squared Euclidean distance between pixel values + 0.1.

We wish to find the shortest weight path from source pixel (i0, j0) to destination pixel (i1, j1) using Dijkstra's algorithm.

We must generate vertices and edges on-the-fly to handle large images (1000x1000 pixels = 1 million vertices).

==================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب حل متاهة (Maze) من صورة.

- نتعامل مع كل بكسل كعقدة (Vertex).
- الوزن بين أي بكسلين متجاورين = 0.1 + (مجموع مربعات الفروق بين قيم RGB الخاصة بهما).
- نستخدم خوارزمية Dijkstra مع `PriorityQueue` مخصص (لا نستخدم مكتبة `heapq` افتراضية) لإيجاد المسار الأقل تكلفة.
- لنتجنب استهلاك الذاكرة، لا نقوم ببناء مصفوفة الجوار كاملة، بل نقوم بتوليد جيران كل عقدة عند الحاجة.

==================================================================
3. Code Implementation:
-----------------------
"""
import math
import cv2
import matplotlib.pyplot as plt

# ====================== Vertex Class ======================
class Vertex:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.d = float('inf')
        self.processed = False
        self.idx_in_priority_queue = -1
        self.pi = None

    def reset(self):
        self.d = float('inf')
        self.processed = False
        self.idx_in_priority_queue = -1
        self.pi = None

# ====================== PriorityQueue Class ======================
class PriorityQueue:
    def __init__(self):
        self.q = [None]

    def insert(self, v):
        n = len(self.q)
        self.q.append(v)
        v.idx_in_priority_queue = n
        self.bubble_up(n)

    def swap(self, i, j):
        tmp = self.q[i]
        self.q[i] = self.q[j]
        self.q[i].idx_in_priority_queue = i
        self.q[j] = tmp
        self.q[j].idx_in_priority_queue = j

    def bubble_up(self, j):
        if j == 1:
            return
        val = self.q[j].d
        parent_idx = j // 2
        parent_val = self.q[parent_idx].d
        if val < parent_val:
            self.swap(j, parent_idx)
            self.bubble_up(parent_idx)

    def bubble_down(self, j):
        n = len(self.q)
        left_child_idx = 2 * j
        right_child_idx = 2 * j + 1
        if left_child_idx >= n:
            return
        if right_child_idx >= n:
            child_idx = left_child_idx
            child_d = self.q[left_child_idx].d
        else:
            (child_d, child_idx) = min((self.q[left_child_idx].d, left_child_idx),
                                       (self.q[right_child_idx].d, right_child_idx))
        if self.q[j].d > child_d:
            self.swap(j, child_idx)
            self.bubble_down(child_idx)

    def get_and_delete_min(self):
        n = len(self.q)
        v = self.q[1]
        if n > 2:
            self.q[1] = self.q[n-1]
            self.q[n-1].idx_in_priority_queue = 1
            del self.q[n-1]
            self.bubble_down(1)
        else:
            del self.q[1]
        return v

    def is_empty(self):
        return len(self.q) == 1

    def update_vertex_weight(self, v):
        j = v.idx_in_priority_queue
        self.bubble_down(j)
        self.bubble_up(j)

# ====================== Helper Functions ======================
def fixPixelValues(px):
    return [float(px[0]), float(px[1]), float(px[2])]

def drawPath(img, path, pThick=2):
    v = path[0]
    x0, y0 = v[0], v[1]
    for v in path:
        x, y = v[0], v[1]
        cv2.line(img, (x, y), (x0, y0), (255, 0, 0), pThick)
        x0, y0 = x, y

# ====================== DirectedGraphFromImage ======================
class DirectedGraphFromImage:
    def __init__(self, img):
        self.img = img
        self.coords2vertex = {}

    def get_vertex_from_coords(self, i, j):
        if (i, j) in self.coords2vertex:
            return self.coords2vertex[(i, j)]
        v = Vertex(i, j)
        self.coords2vertex[(i, j)] = v
        return v

    def get_list_of_neighbors(self, vert):
        i = vert.x
        j = vert.y
        height, width, _ = self.img.shape
        lst = []
        if i > 0:
            v = self.get_vertex_from_coords(i-1, j)
            px1 = fixPixelValues(self.img[j, i])
            px2 = fixPixelValues(self.img[j, i-1])
            w = 0.1 + (px1[0] - px2[0])**2 + (px1[1] - px2[1])**2 + (px1[2] - px2[2])**2
            lst.append((v, w))
        if j > 0:
            v = self.get_vertex_from_coords(i, j-1)
            px1 = fixPixelValues(self.img[j, i])
            px2 = fixPixelValues(self.img[j-1, i])
            w = 0.1 + (px1[0] - px2[0])**2 + (px1[1] - px2[1])**2 + (px1[2] - px2[2])**2
            lst.append((v, w))
        if i < width - 1:
            v = self.get_vertex_from_coords(i+1, j)
            px1 = fixPixelValues(self.img[j, i])
            px2 = fixPixelValues(self.img[j, i+1])
            w = 0.1 + (px1[0] - px2[0])**2 + (px1[1] - px2[1])**2 + (px1[2] - px2[2])**2
            lst.append((v, w))
        if j < height - 1:
            v = self.get_vertex_from_coords(i, j+1)
            px1 = fixPixelValues(self.img[j, i])
            px2 = fixPixelValues(self.img[j+1, i])
            w = 0.1 + (px1[0] - px2[0])**2 + (px1[1] - px2[1])**2 + (px1[2] - px2[2])**2
            lst.append((v, w))
        return lst

# ====================== Dijkstra Implementation (computeShortestPath) ======================
def computeShortestPath(graph, source_coordinates, dest_coordinates):
    src_x, src_y = source_coordinates
    source = graph.get_vertex_from_coords(src_x, src_y)

    dest_x, dest_y = dest_coordinates
    dest = graph.get_vertex_from_coords(dest_x, dest_y)

    pq = PriorityQueue()
    source.d = 0
    pq.insert(source)

    while not pq.is_empty():
        u = pq.get_and_delete_min()
        if u.processed:
            continue
        u.processed = True
        if u == dest:
            break
        for v, w in graph.get_list_of_neighbors(u):
            if v.processed:
                continue
            new_dist = u.d + w
            if new_dist < v.d:
                v.d = new_dist
                v.pi = u
                if v.idx_in_priority_queue == -1:
                    pq.insert(v)
                else:
                    pq.update_vertex_weight(v)

    path = []
    curr = dest
    while curr is not None:
        path.append((curr.x, curr.y))
        curr = curr.pi
    path.reverse()
    return (path, dest.d)

# ====================== Tests (Problem 1 - Dummy Graph) ======================
class DummyGraphClass:
    def __init__(self, adj_list, verts):
        self.verts = verts
        self.adj_list = adj_list

    def get_vertex_from_coords(self, i, j):
        assert (i, j) in self.verts
        return self.verts[(i, j)]

    def get_list_of_neighbors(self, vert):
        coords = (vert.x, vert.y)
        if coords in self.adj_list:
            return self.adj_list[(vert.x, vert.y)]
        else:
            return []

def run_dummy_tests():
    print("\nRunning Dummy Graph Tests...")
    verts = {(i, j): Vertex(i, j) for i in range(3) for j in range(3)}
    adj_list = {}

    def connect_nodes(src, dest, weight):
        v1 = src
        v2 = verts[dest]
        if v1 in adj_list:
            adj_list[v1].append((v2, weight))
        else:
            adj_list[v1] = [(v2, weight)]

    connect_nodes((0, 0), (0, 1), 1.0)
    connect_nodes((0, 0), (1, 0), 0.5)
    connect_nodes((1, 0), (0, 1), 0.5)
    connect_nodes((0, 1), (0, 0), 0.5)
    connect_nodes((1, 0), (1, 1), 0.5)
    connect_nodes((1, 1), (2, 2), 0.25)
    connect_nodes((1, 1), (1, 2), 0.5)
    connect_nodes((1, 1), (2, 1), 1.2)
    connect_nodes((2, 1), (2, 2), 0.25)
    connect_nodes((1, 2), (2, 2), 0.25)

    graph = DummyGraphClass(adj_list, verts)
    path, dist = computeShortestPath(graph, (0, 0), (2, 2))
    assert dist == 1.25, f'Shortest path distance must be 1.25, got {dist}'
    assert path == [(0, 0), (1, 0), (1, 1), (2, 2)]

    for (_, v) in verts.items(): v.reset()

    graph2 = DummyGraphClass(adj_list, verts)
    (path2, dist2) = computeShortestPath(graph2, (0, 0), (1, 2))
    assert dist2 == 1.5, f'Shortest path distance must be 1.5, got {dist2}'
    assert path2[0] == (0, 0)
    assert path2[-1] == (1, 2)

    for (_, v) in verts.items(): v.reset()

    connect_nodes((2, 2), (2, 1), 0.5)
    connect_nodes((2, 1), (1, 1), 1.0)
    connect_nodes((1, 1), (0, 1), 0.5)

    graph3 = DummyGraphClass(adj_list, verts)
    (path3, dist3) = computeShortestPath(graph3, (2, 2), (0, 0))
    assert dist3 == 2.5, f'Shortest path distance must be 2.5, got {dist3}'
    assert path3[0] == (2, 2)
    assert path3[-1] == (0, 0)

    print("All dummy tests passed: 15 points!")

# ====================== Real Image Tests ======================
def run_image_tests():
    print("\nRunning Image Tests...")

    # Maze 1
    img = cv2.imread('maze.png')
    if img is None:
        print("Skipping image tests because 'maze.png' is missing.")
        return

    graph = DirectedGraphFromImage(img)
    p, dist = computeShortestPath(graph, (5, 220), (5, 5))
    print(f"Dist 1: {dist}")
    assert dist <= 78.1, f'Expected shortest path distance <= 78.1, got {dist}'
    assert p[0] == (5, 220)
    assert p[-1] == (5, 5)
    print("Maze 1 passed: 10 points!")

    img_result = cv2.imread('maze.png')
    drawPath(img_result, p, 2)
    plt.imshow(img_result)
    plt.title("Maze 1 Solution")
    plt.show()  # Optional: comment out if running in CLI without display
    cv2.imwrite('maze-solution.png', img_result)

    # Maze 2
    img2 = cv2.imread('maze2.JPG')
    if img2 is None:
        print("Skipping 'maze2.JPG' test because file is missing.")
        return

    p2, dist2 = computeShortestPath(DirectedGraphFromImage(img2), (250, 470), (20, 100))
    print(f"Dist 2: {dist2}")
    assert dist2 <= 120.0, f'Expected shortest path distance <= 120.0, got {dist2}'
    assert p2[0] == (250, 470)
    assert p2[-1] == (20, 100)
    print("Maze 2 passed: 10 points!")

    img2_result = cv2.imread('maze2.JPG')
    drawPath(img2_result, p2)
    plt.imshow(img2_result)
    plt.title("Maze 2 Solution")
    plt.show()
    cv2.imwrite('maze2-solution.JPG', img2_result)

if __name__ == "__main__":
    run_dummy_tests()
    run_image_tests()
    print("\nAll tests passed!")
