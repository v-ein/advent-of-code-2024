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

WALL = -1
times = [[WALL] * width for y in range(height)]


x, y = sx, sy
path_len = 0
times[y][x] = path_len
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


threshold = 100
cheat_count = 0

for y, line in enumerate(map[1:-1]):
    for x, c in enumerate(line[1:-1]):
        if c == "#":
            trk = [times[y + dy + 1][x + dx + 1] for dx, dy in dirs]
            trk = [t for t in trk if t != WALL]
            if len(trk) >= 2:
                save = max(trk) - min(trk) - 2
                if save >= threshold:
                    cheat_count += 1

print(cheat_count)
