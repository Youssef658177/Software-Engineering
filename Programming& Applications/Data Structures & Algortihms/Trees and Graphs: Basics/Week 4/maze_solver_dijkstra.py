"""
Solving Image Maze (With Solution) - English & Arabic Explanation
==================================================================
1. Problem Statement (English):
-------------------------------
Given a maze as an image with a start and end point, we would like to write code to solve the maze.

An image is a 2D matrix of pixels. Each pixel has a color (Red, Green, Blue).

We view the image as a graph where each pixel is a vertex and edges connect a pixel to its neighbor.
The weight of an edge should be very small if the pixel colors are similar (difference close to zero),
and large as the pixel colors diverge.

Given a source pixel (i0, j0) and destination pixel (i1, j1), we wish to find the shortest weight path
from source to destination using Dijkstra's algorithm.

Constraints:
- The graph is huge (1 million pixels for 1000x1000 image), so we must generate vertices and edges on-the-fly.
- We use OpenCV to load and manipulate the image.

==================================================================
2. Explanation (Arabic):
------------------------
المسألة بتطلب حل متاهة (Maze) مصورة باستخدام خوارزمية Dijkstra.

الفكرة الرئيسية:
1. نتعامل مع الصورة كرسم بياني: كل بكسل هو عقدة (Vertex)، والحواف تربط البكسل بجيرانه (فوق، تحت، يمين، يسار).
2. وزن الحافة بين بكسلين يعتمد على "مدى تشابه ألوانهما":
   - لو الألوان متشابهة جدًا (فرق صغير)، الوزن يكون صغير.
   - لو الألوان مختلفة (مثلاً جدار أسود وبكسل أبيض)، الوزن يكون كبير.
3. نستخدم خوارزمية Dijkstra للعثور على المسار الأقصر (أقل وزن) من نقطة البداية إلى نقطة النهاية.
4. تحدٍ رئيسي: الصورة كبيرة (ملايين البكسلات)، لذا لا نبنِي قائمة الجوار كاملة مسبقًا، بل نولّد الجيران عند الحاجة (On-the-fly).

==================================================================
3. Code Implementation (Complete Solution):
-------------------------------------------
"""
import heapq
import math
import cv2
import matplotlib.pyplot as plt

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # For Dijkstra
        self.dist = float('inf')
        self.visited = False
        self.previous = None

    def __lt__(self, other):
        return self.dist < other.dist

    def __repr__(self):
        return f'({self.x}, {self.y})'

class DirectedGraphFromImage:
    def __init__(self, img):
        self.img = img
        self.coords2vertex = {} # Dictionary mapping (x, y) to Vertex object

    def get_vertex_from_coords(self, i, j):
        if (i, j) in self.coords2vertex:
            return self.coords2vertex[(i, j)]
        v = Vertex(i, j)
        self.coords2vertex[(i, j)] = v
        return v

    def getEdgeWeight(self, u, v):
        # Fixed the indices - (y, x) for accessing img, but stored (x, y) in Vertex
        j0, i0 = u.y, u.x
        j1, i1 = v.y, v.x
        height, width, _ = self.img.shape
        # Important: index image as img[y, x]
        px1 = self.fixPixelValues(self.img[j0, i0])
        px2 = self.fixPixelValues(self.img[j1, i1])
        return 0.1 + (px1[0] - px2[0])**2 + (px1[1] - px2[1])**2 + (px1[2] - px2[2])**2

    def fixPixelValues(self, px):
        return [float(px[0]), float(px[1]), float(px[2])]

    def get_list_of_neighbors(self, vert):
        img = self.img
        i, j = vert.x, vert.y
        height, width, _ = img.shape
        lst = []
        # West
        if i > 0:
            v0 = self.get_vertex_from_coords(i-1, j)
            w0 = self.getEdgeWeight(vert, v0)
            lst.append((v0, w0))
        # South
        if j > 0:
            v1 = self.get_vertex_from_coords(i, j-1)
            w1 = self.getEdgeWeight(vert, v1)
            lst.append((v1, w1))
        # East
        if i < width - 1:
            v2 = self.get_vertex_from_coords(i+1, j)
            w2 = self.getEdgeWeight(vert, v2)
            lst.append((v2, w2))
        # North
        if j < height - 1:
            v3 = self.get_vertex_from_coords(i, j+1)
            w3 = self.getEdgeWeight(vert, v3)
            lst.append((v3, w3))
        return lst

def dijkstra(graph, start, end):
    """
    Dijkstra's algorithm on a graph generated on-the-fly.
    """
    start_vertex = graph.get_vertex_from_coords(start[0], start[1])
    end_vertex = graph.get_vertex_from_coords(end[0], end[1])

    start_vertex.dist = 0
    pq = [(0, start_vertex)]

    while pq:
        current_dist, current = heapq.heappop(pq)
        if current.visited:
            continue
        current.visited = True

        if current == end_vertex:
            break

        for neighbor, weight in graph.get_list_of_neighbors(current):
            if not neighbor.visited:
                new_dist = current_dist + weight
                if new_dist < neighbor.dist:
                    neighbor.dist = new_dist
                    neighbor.previous = current
                    heapq.heappush(pq, (new_dist, neighbor))

    # Reconstruct path
    path = []
    current = end_vertex
    while current:
        path.append((current.x, current.y))
        current = current.previous
    return path[::-1]

# ==================== TEST CASES & EXAMPLE ====================
if __name__ == "__main__":
    # Load the image
    img = cv2.imread('maze.png')
    if img is None:
        print("Error: Could not load 'maze.png'. Please make sure the file exists.")
    else:
        # Define start and end points (based on the circles in the example)
        # Start: Blue circle at (5, 5) -> Usually (x, y) format
        # End: Red circle at (5, 220) -> (x, y) format
        start = (5, 5)
        end = (5, 220)

        print("Building graph from image...")
        graph = DirectedGraphFromImage(img)

        print(f"Running Dijkstra from {start} to {end}...")
        try:
            path = dijkstra(graph, start, end)
            print(f"Path found! Length: {len(path)} pixels.")

            # Visualize the result
            img_result = cv2.imread('maze.png')
            drawPath(img_result, path) # Using the function defined in the prompt
            plt.imshow(img_result)
            plt.title("Solved Maze (Red Line = Path)")
            plt.show()

        except Exception as e:
            print(f"An error occurred: {e}")
