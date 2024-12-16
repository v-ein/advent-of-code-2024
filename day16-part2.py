from typing import Set, Tuple
from puzzle_input import puzzle_input


map_str = puzzle_input.strip()
width = map_str.index("\n")

sy, sx = divmod(map_str.index("S"), width + 1)
ey, ex = divmod(map_str.index("E"), width + 1)

map = map_str.splitlines()
height = len(map)

visited = [[[c == "#"]*4 for c in line] for line in map]

UNVISITED = -1
weights = [[[UNVISITED]*4 for x in range(width)] for y in range(height)]

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

# We start at direction 0
weights[sy][sx][0] = 0

wave = set()
wave.add((sx, sy, 0))

min_path = -1

# Many thanks to Edsger Dijkstra for this piece of classics
while wave:
    # Find an unvisited node with the least weight
    mx, my, mz = next(iter(wave))
    min_w = weights[my][mx][mz]
    for x, y, z in wave:
        cur_w = weights[y][x][z]
        if cur_w < min_w:
            min_w = cur_w
            mx, my, mz = x, y, z

    # See if we've finally reached the end node.  If we continue from this point,
    # all the paths will be longer than min_w, meaning we'll never come back
    # to (mx, my) with a shorter path.
    if (mx, my) == (ex, ey):
        min_path = min_w
        break

    # Now re-evaluate the node's neighbours.  From a node with direction z, we can
    # go straight to the node with the same z (for the cost of 1 point), turn left
    # to (z-1) for 1001 points, or turn right to (z+1) for 1001 points.  We could
    # also go backwards, but what's the point, we've already visited the node behind us.
    for dz, cost in ((-1, 1001), (0, 1), (1, 1001)):
        nz = (mz + dz) % len(dirs)
        dx, dy = dirs[nz]
        nx = mx + dx
        ny = my + dy
        if not (0 <= nx < width and 0 <= ny < height) or visited[ny][nx][nz]:
            continue
        old_w = weights[ny][nx][nz]
        new_w = min_w + cost
        if old_w == UNVISITED:
            wave.add((nx, ny, nz))
            weights[ny][nx][nz] = new_w
        else:
            weights[ny][nx][nz] = min(old_w, new_w)

    # Finally mark the node as visited and never check it again
    visited[my][mx][mz] = True
    wave.remove((mx, my, mz))


# Now go back through the maze and find out what the best paths are.

# We could have also used a "visited" style map for path_nodes.
path_nodes: Set[Tuple[int, int, int]] = set()
backwave = [(ex, ey, ez) for ez, w in enumerate(weights[ey][ex]) if w == min_path]

# Debug helpers
def show_map():
    cur_map = [list(line) for line in map]
    for (x, y, z) in path_nodes:
        cur_map[y][x] = "O"
    for (x, y, z) in backwave:
        cur_map[y][x] = "W"
    return ["".join(line) for line in cur_map]

def show_map_dbg():
    return [line.replace(".", " ").replace("O", ".") for line in show_map()]

def print_map():
    print("\n".join(show_map()))


while backwave:
    x, y, z = backwave.pop()
    if (x, y, z) in path_nodes:
        # No need to process it again
        continue
    path_nodes.add((x, y, z))
    w = weights[y][x][z]
    # Hit the starting point?
    if w == 0:
        continue
    # Calc coords of the previous tile
    dx, dy = dirs[z]
    px, py = x - dx, y - dy
    # Go check the neighbours and see from where we could have come to this point
    for dz, cost in ((-1, 1001), (0, 1), (1, 1001)):
        pz = (z - dz) % len(dirs)
        pw = weights[py][px][pz]
        if pw != UNVISITED and pw + cost == w:
            backwave.append((px, py, pz))


best_points = {(x, y) for x, y, z in path_nodes}

print(len(best_points))
