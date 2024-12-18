from puzzle_input import puzzle_input


width = height = 71
max_fall = 1024

falling_bytes = [
    [int(s) for s in line.split(",")]
        for line in puzzle_input.strip().splitlines()
]

def show_map():
    return ["".join(line) for line in map]

map = [["."] * width for y in range(height)]
for x, y in falling_bytes[:max_fall]:
    map[y][x] = "#"


# While we could just repeat the search algo from part 1 and after each falling
# byte see if can find the path, let's do it differently this time - just for fun.
# We'll check if the falling byte forms a wall that touches both top/right edges
# and bottom/left edges - this will effectively block the path.
# An implementation using DSU would probably be even better, we'd just add the
# falling byte to a connected set and eventually the set would touch the edges
# of the map.
for fx, fy in falling_bytes[max_fall:]:
    map[fy][fx] = "#"
    wall = set()
    wave = set()
    wave.add((fx, fy))
    touches_bl = False
    touches_tr = False
    while wave:
        new_wave = set()
        for x, y in wave:
            touches_bl = touches_bl or x == 0 or y == height - 1
            touches_tr = touches_tr or y == 0 or x == width - 1
            wall.add((x, y))
            for ny in range(y - 1, y + 2):
                for nx in range(x - 1, x + 2):
                    if ((nx, ny) not in wall and
                        0 <= nx < width and 0 <= ny < height and
                        map[ny][nx] == "#"):
                        # Found one more wall element
                        new_wave.add((nx, ny))
        wave = new_wave

    if touches_bl and touches_tr:
        print(f"Blocked at {fx},{fy}")
        break

else:
    print("Bad luck!")
