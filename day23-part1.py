from typing import Dict, Set
from puzzle_input import puzzle_input


couples = [tuple(line.split("-")) for line in puzzle_input.strip().splitlines()]

connections: Dict[str, Set[str]] = {}

nets = set()

for a, b in couples:
    if a in connections and b in connections:
        common = connections[a] & connections[b]
        for c in common:
            if a[0] == "t" or b[0] == "t" or c[0] == "t":
                nets.add((a, b, c))

    if a not in connections:
        connections[a] = set()
    connections[a].add(b)

    if b not in connections:
        connections[b] = set()
    connections[b].add(a)

print(len(nets))
