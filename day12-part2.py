from itertools import zip_longest
import re
from typing import Dict, List, Set, Tuple
from puzzle_input import puzzle_input


map = puzzle_input.splitlines()
map = [" " + line + " " for line in map]
width = len(map[0])
empty_line = " " * width
map.insert(0, empty_line)
map.append(empty_line)

fences = [[0] * width for i in range(len(map))]

# Horizontal fences - we run along the edge between two lines, adding 1 to those
# locations where a fence around a region starts.  For convenience, we blank out
# internal areas - this seems to be easier than to additionally check that we
# exit such an area (maybe not, it was just what came to my mind).
for line_a, line_b, fence_a, fence_b in zip(map, map[1:], fences, fences[1:]):
    pa, pb = " ", " "
    for x, (a, b) in enumerate(zip(line_a, line_b)):
        if a == b:
            a, b = " ", " "
        if a != pa:
            if a != b:
                fence_a[x] += 1
            pa = a
        if b != pb:
            if a != b:
                fence_b[x] += 1
            pb = b


# Vertical fences - similar to horizontal but going in vertical direction :),
# trying to process columns in parallel.
prev_a = prev_b = map[0]
for line, fence in zip(map[1:], fences[1:]):
    for x, (pa, pb, a, b) in enumerate(zip(prev_a, prev_b[1:], line, line[1:])):
        if a != b:
            if a != pa:
                fence[x] += 1
            if b != pb:
                fence[x + 1] += 1

    # This regex magic does the same blanking out of internal regions as the condition
    # a == b does for horizontal fences.
    prev_a = re.sub(r"(.)\1+", (lambda m: m[1].rjust(len(m[0]))), line)
    prev_b = re.sub(r"(.)\1+", (lambda m: m[1].ljust(len(m[0]))), line)


# Just for convenience, cut off those spaces we added earlier (but keep line 0 on
# the map - we need it for padding in the for-loop below).
map = [line[1:-1] for line in map[:-1]]
fences = [line[1:-1] for line in fences[1:-1]]

# Region search would probably look *much* better if DSU was used, but I don't
# remember much about DSU off top of my head.
merges: Set[Tuple[int, int]] = set()
regions: List[Tuple[int, int]] = []

area = 0
peri = 0
prev_reg_ids = [-1] * width
for line, prev_line, fence in zip(map[1:], map, fences):
    # First split the line into regions
    line_reg_ids = []
    for a, b, p in zip_longest(line, line[1:], fence):
        # OMG how inefficient this must be
        area += 1
        peri += p
        line_reg_ids.append(len(regions))
        if a != b:
            regions.append((area, peri))
            area = 0
            peri = 0
    # Now see what should be merged with other regions
    for a, b, prev_id, cur_id in zip(line, prev_line, line_reg_ids, prev_reg_ids):
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
