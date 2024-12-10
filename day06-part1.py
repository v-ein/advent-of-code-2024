from puzzle_input import puzzle_input


directions = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]

puzzle_input = puzzle_input.strip()
# This looks pretty inefficient but who promised runtime efficiency? :)
# Remember, here I'm trying to save on development time, not run time.
map = [ list(line) for line in puzzle_input.split() ]

start_pos = puzzle_input.index("^")
# +1 compensates for "\n" in puzzle_input
y, x = divmod(start_pos, len(map[0]) + 1)
dir_idx = 0

map[y][x] = "X"

while True:
    dx, dy = directions[dir_idx]
    new_x = x + dx
    new_y = y + dy
    if not (0 <= new_y < len(map) and 0 <= new_x < len(map[new_y])):
        break
    if map[new_y][new_x] == "#":
        dir_idx = (dir_idx + 1) % len(directions)
    else:
        x, y = new_x, new_y
        map[y][x] = "X"

visited_count = sum([line.count("X") for line in map])
print(visited_count)

# Just a debugging helper
def lookaround():
    w = 10
    h = 5
    return ["".join(l[x-w:x+w+1]) for l in map[y-h:y+h+1]]

