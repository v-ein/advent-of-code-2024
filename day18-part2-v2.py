from scipy.cluster.hierarchy import DisjointSet

from puzzle_input import puzzle_input


width = height = 71
max_fall = 1024

falling_bytes = [
    [int(s) for s in line.split(",")]
        for line in puzzle_input.strip().splitlines()
]

walls = DisjointSet(["bottom-left", "top-right"])

for fx, fy in falling_bytes:
    walls.add((fx, fy))
    for y in range(fy - 1, fy + 2):
        for x in range(fx - 1, fx + 2):
            if (x, y) != (fx, fy):
                if x < 0 or y >= height:
                    walls.merge((fx, fy), "bottom-left")
                elif y < 0 or x >= width:
                    walls.merge((fx, fy), "top-right")
                elif (x, y) in walls:
                    walls.merge((fx, fy), (x, y))

    if walls.connected("bottom-left", "top-right"):
        print(f"Blocked at {fx},{fy}")
        break

else:
    print("Bad luck!")
