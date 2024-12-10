from puzzle_input import puzzle_input


map = puzzle_input.strip()
width = map.index("\n")
map = map.replace("\n", "")
height = len(map) // width

def get_trail_ends(x, y, cur_level, final_level=9):
    if (0 <= x < width and 0 <= y < height and map[x + width*y] == str(cur_level)):
        if cur_level == final_level:
            return {(x, y)}
        ends = set()
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            ends |= get_trail_ends(x + dx, y + dy, cur_level + 1, final_level)
        return ends

    return set()

# Now go collect all the scores for level 0
pos = map.find("0")
total = 0
while pos >= 0:
    y, x = divmod(pos, width)
    total += len(get_trail_ends(x, y, 0, 9))
    pos = map.find("0", pos + 1)

print(total)
