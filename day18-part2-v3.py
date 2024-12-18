from scipy.cluster.hierarchy import DisjointSet

from puzzle_input import puzzle_input


width = height = 71
max_fall = 1024

falling_bytes = [
    [int(s) for s in line.split(",")]
        for line in puzzle_input.strip().splitlines()
]

bl_edges = [(x, height) for x in range(width)] + [(-1, y) for y in range(height)]
tr_edges = [(x, -1) for x in range(width)] + [(width, y) for y in range(height)]

walls = DisjointSet(bl_edges + tr_edges)

for p1, p2 in zip(bl_edges, bl_edges[1:]):
    walls.merge(p1, p2)

for p1, p2 in zip(tr_edges, tr_edges[1:]):
    walls.merge(p1, p2)


for fx, fy in falling_bytes:
    walls.add((fx, fy))
    for y in range(fy - 1, fy + 2):
        for x in range(fx - 1, fx + 2):
            if (x, y) in walls:
                walls.merge((fx, fy), (x, y))

    if walls.connected((-1, 0), (0, -1)):
        print(f"Blocked at {fx},{fy}")
        break

else:
    print("Bad luck!")
