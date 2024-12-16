import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.csgraph import dijkstra
from puzzle_input import puzzle_input

map_str = puzzle_input.strip()
width = map_str.index("\n")

sy, sx = divmod(map_str.index("S"), width + 1)
ey, ex = divmod(map_str.index("E"), width + 1)

map = map_str.splitlines()
height = len(map)

dirs = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]

# z values:
# 0 - >
# 1 - v
# 2 - <
# 3 - ^

def node_id(x, y, z):
    return 4*(y*width + x) + z


# Building the graph
nodes_count = width*height*4
print(f"{nodes_count=}")
graph = lil_matrix((nodes_count, nodes_count), dtype=np.dtype(int))

print("Building the graph...")
for y, line in enumerate(map):
    for x, c in enumerate(line):
        if c != "#":
            for z, (dx, dy) in enumerate(dirs):
                px, py = x - dx, y - dy
                if 0 <= px < width and 0 <= py < height and map[py][px] != "#":
                    to_node = node_id(x, y, z)
                    for dz, cost in ((-1, 1001), (0, 1), (1, 1001)):
                        pz = (z - dz) % len(dirs)
                        from_node = node_id(px, py, pz)
                        graph[from_node, to_node] = cost


print("Finding the min path...")
dist_matrix = dijkstra(csgraph=graph, directed=True, indices=node_id(sx, sy, 0), return_predecessors=False, min_only=True)

end_dist = [dist_matrix[node_id(ex, ey, ez)] for ez in range(4)]

print(min(end_dist))
