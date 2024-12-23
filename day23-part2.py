from typing import Dict, List, Set
from puzzle_input import puzzle_input

couples = [tuple(line.split("-")) for line in puzzle_input.strip().splitlines()]

connections: Dict[str, Set[str]] = {}

for a, b in couples:
    if a not in connections:
        connections[a] = set()
    connections[a].add(b)

    if b not in connections:
        connections[b] = set()
    connections[b].add(a)


# Starting with sets each consisting of just one computer.
nets: List[Set[str]] = [set([k]) for k in connections]

for comp, connected in connections.items():
    for net in nets:
        if connected.issuperset(net):
            # There will be a lot of duplicates in `nets` (a net of N computers
            # will finally have N duplicates in `nets`). However, with what little
            # data we have in the puzzle input we don't really care.
            net.add(comp)


largest = max(nets, key=len)
print(",".join(sorted(largest)))
