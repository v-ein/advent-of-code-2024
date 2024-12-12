from scipy.cluster.hierarchy import DisjointSet

from puzzle_input import puzzle_input

map = puzzle_input.splitlines()

v_edges = [
    [ 1 if a != b else 0 for a, b in zip(" " + line, line + " ") ]
        for line in map
]

v_perimeter = [
    [ a + b for a, b in zip(line, line[1:]) ]
        for line in v_edges
]

width = len(map[0])
empty_line = " " * width

h_edges = [
    [ 1 if a != b else 0 for a, b in zip(line1, line2) ]
        for line1, line2 in zip([empty_line] + map, map + [empty_line])
]

h_perimeter = [
    [ a + b for a, b in zip(line1, line2) ]
        for line1, line2 in zip(h_edges, h_edges[1:])
]

perimeter = [
    [ h + v for h, v in zip(h_line, v_line)]
        for h_line, v_line in zip(h_perimeter, v_perimeter)
]


# Filling in regions - this version uses DSU (Disjoint-Set Union), probably in
# an inefficient way (in terms of CPU time) but implementation-wise it's pretty simple.
regions = DisjointSet([(x, y) for y in range(len(map)) for x in range(width)])

# First go horizontally, separately in every line
for y, line in enumerate(map):
    for x, (a, b) in enumerate(zip(line, line[1:])):
        if b == a:
            # Merge b into the region
            regions.merge((x, y), (x + 1, y))

# Now merge between the lines
for y, (line_a, line_b) in enumerate(zip(map, map[1:])):
    for x, (a, b) in enumerate(zip(line_a, line_b)):
        if b == a:
            # Merge b into the region
            regions.merge((x, y), (x, y + 1))

def calc_region_price(coords):
    return len(coords) * sum([perimeter[y][x] for x, y in coords])


total = sum([calc_region_price(region) for region in regions.subsets()])
print(total)
