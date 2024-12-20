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


x, y = sx, sy
# (-1, -1) is a fake tile that we'll remove later - we need it so that we can safely
# refer to route[-2] all the time.
route = [(-1, -1), (sx, sy)]

while (x, y) != (ex, ey):
    for dx, dy in dirs:
        nx = x + dx
        ny = y + dy
        if map[ny][nx] != "#" and (nx, ny) != route[-2]:
            x, y = nx, ny
            break
    else:
        assert False, f"Got into a dead end at {x, y}."
    route.append((x, y))

del route[0]

cheat_count = 0
# While technically we could check shortcuts from every route point to every other point,
# it doesn't make sense to check points being fewer than (threshold+2) steps apart from
# each other.  They will never give us savings higher than the threshold.
min_dist = threshold + 2

for ei, (ex, ey) in enumerate(route[min_dist:]):
    for si, (sx, sy) in enumerate(route[:ei + 1]):
        cutoff_len = abs(ex - sx) + abs(ey - sy)
        if cutoff_len <= cheat_time:
            save = min_dist + ei - si - cutoff_len
            if save >= threshold:
                cheat_count += 1


print(cheat_count)
