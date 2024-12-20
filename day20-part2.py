from puzzle_input import puzzle_input


threshold = 100
cheat_time = 20


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

# This piece was mostly copy-pasted from part 1, even though we now store the route
# in a separate list of coordinates, and don't have any use for the "times" map.
WALL = -1
times = [[WALL] * width for y in range(height)]


x, y = sx, sy
path_len = 0
times[y][x] = path_len
route = [(sx, sy)]
while (x, y) != (ex, ey):
    for dx, dy in dirs:
        nx = x + dx
        ny = y + dy
        if map[ny][nx] != "#" and times[ny][nx] == WALL:
            x, y = nx, ny
            break
    else:
        assert False, f"Got into a dead end at {x, y}."
    path_len += 1
    times[ny][nx] = path_len
    route.append((nx, ny))


cheat_count = 0

r_route = list(reversed(route))

for si, (sx, sy) in enumerate(route):
    for ei, (ex, ey) in enumerate(r_route):
        ei = len(route) - ei - 1
        max_save = ei - si - 2
        if max_save < threshold:
            break
        cutoff_len = (abs(ex - sx) + abs(ey - sy))
        if cutoff_len <= cheat_time:
            save = (ei - si) - cutoff_len
            if save >= threshold:
                cheat_count += 1


print(cheat_count)
