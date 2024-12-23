from typing import Dict, List, Set
from puzzle_input import puzzle_input

# This version uses less memory (probably half of that for v1), but requires
# some extra sorting steps.

couples = [tuple(line.split("-")) for line in puzzle_input.strip().splitlines()]

connections: Dict[str, Set[str]] = {}
comps: Set[str] = set()

for a, b in couples:
    if a < b:
        a, b = b, a
    if a not in connections:
        connections[a] = set()
        comps.add(a)
    connections[a].add(b)
    comps.add(b)


# Starting with sets each consisting of just one computer.
nets: List[Set[str]] = [set([k]) for k in comps]

for comp, connected in sorted(connections.items()):
    for net in nets:
        if connected.issuperset(net):
            # There will be a lot of duplicates in `nets` (a net of N computers
            # will finally have N duplicates in `nets`). However, with what little
            # data we have in the puzzle input we don't really care.
            net.add(comp)


largest = max(nets, key=len)
print(",".join(sorted(largest)))
