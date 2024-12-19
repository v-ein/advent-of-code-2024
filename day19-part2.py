from bisect import bisect_right
from typing import Dict
from puzzle_input import puzzle_input


tstr, dstr = puzzle_input.strip().split("\n\n")
towels = tstr.replace(" ", "").split(",")
designs = dstr.splitlines()

# Ideally we'd need to build a tree but let's see if a plain sorted list works
# in reasonable time.
towels.sort()

# On long enough designs, computing the hash is faster than the exponential time
# of recursively checking sub-designs.
ways: Dict[str, int] = {}

def count_ways(design: str):
    if not design:
        return 1
    if design in ways:
        return ways[design]

    min_key = design[0]
    start = bisect_right(towels, design)
    cur_ways = 0
    for i in range(start - 1, -1, -1):
        key = towels[i]
        if key < min_key:
            break
        if design.startswith(key):
            cur_ways += count_ways(design[len(key):])

    ways[design] = cur_ways
    return cur_ways


total = sum([count_ways(design) for design in designs])
print(total)
