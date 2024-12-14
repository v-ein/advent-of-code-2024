import re
from puzzle_input import puzzle_input

width = 101
height = 103

def move_robot(x, y, vx, vy):
    return ((x + vx) % width, (y + vy) % height, vx, vy)


def is_xmas_tree(coords):
    # Let's try to find the trunk. Supposing it's somewhere in the middle of the picture,
    # but for simplicity we'll search the entire width and see how it works.  The trunk
    # must be a contiguous vertical line, which means we can easily throw away pictures
    # where pixels are not grouped into massive vertical groups, say, height/4 pixels 
    # per a single X value.
    trunk_limit = height // 4

    vert_count = [0] * width
    for x, *_ in coords:
        vert_count[x] += 1
    if max(vert_count) < trunk_limit:
        # This picture can't have a vertical line trunk_limit pixels long
        return False

    # Now go and see whether there's really a solid vertical line in this picture
    max_len = 0
    for trunk_x, h in enumerate(vert_count):
        if h >= trunk_limit:
            # See if there's a dense line forming the trunk
            trunk_y = [y for x, y, *_ in coords if x == trunk_x]
            trunk_y.sort()
            trunk_len = 0
            for y1, y2 in zip(trunk_y, trunk_y[1:]):
                # We don't account for two robots being in the same (x, y) yet,
                # let's see how it works.
                if y2 == y1 + 1:
                    trunk_len += 1
                else:
                    max_len = max(max_len, trunk_len)
                    trunk_len = 0

    return max_len >= trunk_limit


def print_map(coords):
    map = [[0]*width for y in range(height)]
    for x, y, *_ in coords:
        map[y][x] += 1
    base_char = ord("A") - 1
    str_map = ["".join([" " if m == 0 else chr(base_char + min(26, m)) for m in line]) for line in map]
    print("\n".join(str_map))


robot_re = r"p=(\d+),\s*(\d+)\s*v=([+-]?\d+),\s*([+-]?\d+)"

# Parse the input into a list of ints
coords = [tuple(int(x) for x in m) for m in re.findall(robot_re, puzzle_input)]

for i in range(100000):
    if is_xmas_tree(coords):
        print_map(coords)
        print(f"Found after {i} seconds")
        break
    coords = [move_robot(*c) for c in coords]
else:
    print("Bad luck.")
