from puzzle_input import puzzle_input


map_text, moves, *_ = puzzle_input.strip().split("\n\n")
map_text = map_text.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")

map = [list(line) for line in map_text.splitlines()]
width = len(map[0])

robot_pos = map_text.index("@")
# +1 compensates for "\n"
ry, rx = divmod(robot_pos, width + 1)


def can_move_box(x, y, dx, dy):
    c = map[y][x]
    if c == ".":
        return True
    if c == "]":
        x -= 1

    if dx == 0:
        ny = y + dy
        c1 = map[ny][x]
        c2 = map[ny][x + 1]
        if c1 == "#" or c2 == "#":
            return False
        # To avoid checking one box twice and thus getting exponential cost
        if c1 == "[":
            return can_move_box(x, ny, dx, dy)
        return can_move_box(x, ny, dx, dy) and can_move_box(x + 1, ny, dx, dy)

    else:
        nx = x + dx + (1 if dx > 0 else 0)
        c = map[y][nx]
        if c == "#":
            return False
        if c == ".":
            return True
        return can_move_box(nx, y, dx, dy)


def move_box(x, y, dx, dy):
    c = map[y][x]
    if c == ".":
        return
    if c == "]":
        x -= 1

    map[y][x] = "."
    map[y][x + 1] = "."

    nx, ny = x + dx, y + dy
    move_box(nx, ny, dx, dy)
    move_box(nx + 1, ny, dx, dy)

    map[ny][nx] = "["
    map[ny][nx + 1] = "]"


def move_robot(x, y, dx, dy):
    nx, ny = x + dx, y + dy

    if map[ny][nx] == "#":
        return (x, y)

    if map[ny][nx] != ".":
        if not can_move_box(nx, ny, dx, dy):
            return (x, y)
        move_box(nx, ny, dx, dy)

    map[ny][nx] = map[y][x]
    map[y][x] = "."
    return (nx, ny)


dir_map = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1),
}

# Only needed for debugging
def show_map():
    return ["".join(line) for line in map]

for i, m in enumerate(moves):
    if m in dir_map:
        map[ry][rx] = m     # makes debugging easier
        dx, dy = dir_map[m]
        rx, ry = move_robot(rx, ry, dx, dy)


total = sum([x + 100 * y for y, line in enumerate(map) for x, c in enumerate(line) if c == "["])

print(total)
