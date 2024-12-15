from puzzle_input import puzzle_input


map_text, moves, *_ = puzzle_input.strip().split("\n\n")

map = [list(line) for line in map_text.splitlines()]
width = len(map[0])

robot_pos = map_text.index("@")
# +1 compensates for "\n"
ry, rx = divmod(robot_pos, width + 1)

def move(x, y, dx, dy):
    nx, ny = x + dx, y + dy
    if map[ny][nx] == "#":
        return (x, y, False)
    if map[ny][nx] != "." and not move(nx, ny, dx, dy)[2]:
        return (x, y, False)
    map[ny][nx] = map[y][x]
    map[y][x] = "."
    return (nx, ny, True)


dir_map = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1),
}

for m in moves:
    if m in dir_map:
        dx, dy = dir_map[m]
        rx, ry, _ = move(rx, ry, dx, dy)


total = sum([x + 100 * y for y, line in enumerate(map) for x, c in enumerate(line) if c == "O"])

print(total)
