from bisect import bisect_right
from typing import Set
from puzzle_input import puzzle_input


tstr, dstr = puzzle_input.strip().split("\n\n")
towels = tstr.replace(" ", "").split(",")
designs = dstr.splitlines()

# Ideally we'd need to build a tree but let's see if a plain sorted list works
# in reasonable time.
towels.sort()

# On long enough designs, computing the hash is faster than the exponential time
# of recursively checking sub-designs.
impossible: Set[str] = set()

def is_possible(design: str):
    if not design:
        return True
    if design in impossible:
        return False
    min_key = design[0]
    start = bisect_right(towels, design)
    for i in range(start - 1, -1, -1):
        key = towels[i]
        if key < min_key:
            break
        if design.startswith(key) and is_possible(design[len(key):]):
            return True

    impossible.add(design)
    return False

total = len([design for design in designs if is_possible(design)])
print(total)
