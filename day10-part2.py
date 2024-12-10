from puzzle_input import puzzle_input


map = puzzle_input.strip()
width = map.index("\n")
map = map.replace("\n", "")
height = len(map) // width

ratings = [[0]*width for i in range(height)]

for i in range(9, 0, -1):
    level = str(i)
    lower_level = str(i - 1)
    pos = map.find(level)
    while pos >= 0:
        y, x = divmod(pos, width)
        base_score = ratings[y][x] if i < 9 else 1
        if base_score > 0:
            for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                nx = x + dx
                ny = y + dy
                if 0 <= nx < width and 0 <= ny < height and map[nx + width*ny] == lower_level:
                    ratings[ny][nx] += base_score

        pos = map.find(level, pos + 1)

# Now go collect all the ratings for level 0
pos = map.find("0")
total = 0
while pos >= 0:
    y, x = divmod(pos, width)
    total += ratings[y][x]
    pos = map.find("0", pos + 1)

print(total)
