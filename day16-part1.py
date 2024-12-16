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


print(min_path)
