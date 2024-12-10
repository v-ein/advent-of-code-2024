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
        dx = x2 - x1
        dy = y2 - y1
        nx, ny = x2, y2
        while 0 <= nx < width and 0 <= ny < height:
            antinodes.add((nx, ny))
            nx += dx
            ny += dy

print(len(antinodes))
