from itertools import permutations
import re
from typing import Dict, List, Tuple

from puzzle_input import puzzle_input


puzzle_input = puzzle_input.strip()

width = puzzle_input.index("\n")
map = puzzle_input.replace("\n", "")
height = len(map) // width

antennae: Dict[str, List[Tuple[int, int]]] = {}
for m in re.finditer(r"[^.]", map):
    freq = m[0]
    if not freq in antennae:
        antennae[freq] = []
    y, x = divmod(m.start(), width)
    antennae[freq].append((x, y))


antinodes = set()
for freq in antennae:
    for (x1, y1), (x2, y2) in permutations(antennae[freq], 2):
        # Basically node x = x2 + (x2-x1)
        nx = 2*x2 - x1
        ny = 2*y2 - y1
        if 0 <= nx < width and 0 <= ny < height:
            antinodes.add((nx, ny))

print(len(antinodes))
