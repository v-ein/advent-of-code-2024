from itertools import zip_longest
from typing import Dict, List, Set, Tuple
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

# Region search would probably look *much* better if DSU was used, but I don't
# remember much about DSU off top of my head.
map.insert(0, empty_line)

merges: Set[Tuple[int, int]] = set()
regions: List[Tuple[int, int]] = []

area = 0
peri = 0
prev_reg_ids = [-1] * width
for y in range(1, len(map)):
    line = map[y]
    # First split the line into regions
    line_reg_ids = []
    for a, b, p in zip_longest(line, line[1:], perimeter[y-1]):
        # OMG how inefficient this must be
        area += 1
        peri += p
        line_reg_ids.append(len(regions))
        if a != b:
            regions.append((area, peri))
            area = 0
            peri = 0
    # Now see what should be merged with other regions
    for a, b, prev_id, cur_id in zip(line, map[y-1], line_reg_ids, prev_reg_ids):
        if a == b:
            merges.add((prev_id, cur_id))
    prev_reg_ids = line_reg_ids

# Go merge the regions
renames: Dict[int, int] = {}    # this is outright stupid, but let's see if it works
for id2, id1 in merges:
    while id2 in renames:
        id2 = renames[id2]
    while id1 in renames:
        id1 = renames[id1]

    # It can be that both initial id1 and id2 have already been merged into the
    # same "root" node - in this case we'll just skip this merge
    if id1 != id2:
        renames[id2] = id1
        a1, p1 = regions[id1]
        a2, p2 = regions[id2]
        regions[id1] = (a1 + a2, p1 + p2)
        regions[id2] = (0, 0)

total = sum([a*p for a, p in regions])
print(total)
