from puzzle_input import puzzle_input


width = height = 71
max_fall = 1024

falling_bytes = [
    [int(s) for s in line.split(",")]
        for line in puzzle_input.strip().splitlines()[:max_fall]
]

sy, sx = (0, 0)
ey, ex = (width - 1, height - 1)

dirs = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]

map = [["."] * width for y in range(height)]
for x, y in falling_bytes:
    map[y][x] = "#"


wave = set()
wave.add((sx, sy))

path_len = 0

while wave:
    new_wave = set()
    for (x, y) in wave:
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and map[ny][nx] == ".":
                map[ny][nx] = "O"
                new_wave.add((nx, ny))
    path_len += 1
    wave = new_wave
    if (ex, ey) in wave:
        break

print(path_len)
