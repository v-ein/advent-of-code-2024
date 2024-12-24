import re
from typing import Dict, List, Tuple
from puzzle_input import puzzle_input

puzzle_input = puzzle_input.strip()
inputs_str, gates_str = puzzle_input.split("\n\n")
inputs_raw = [line.split(": ") for line in inputs_str.splitlines()]

wires = {name: int(value) for name, value in inputs_raw}

gates: Dict[Tuple[str, str], List[Tuple[str, str]]] = {}
for m in re.findall(r"^(\S+)\s+(AND|OR|XOR)\s+(\S+)\s+->\s+(\S+)", gates_str, re.MULTILINE):
    a, b = m[0], m[2]
    if a > b:
        a, b = b, a
    # key = (a, b)
    if (a, b) not in gates:
        gates[(a, b)] = []
    gates[(a, b)].append((m[1], m[3]))


# The most brute-force thing ever
while gates:
    for (a, b), outs in gates.copy().items():
        if a in wires and b in wires:
            wa = wires[a]
            wb = wires[b]
            for op, out in outs:
                if op == "AND":
                    wires[out] = wa and wb
                elif op == "OR":
                    wires[out] = wa or wb
                elif op == "XOR":
                    wires[out] = wa ^ wb
            del gates[(a, b)]

out_value = 0
for name, value in wires.items():
    if name.startswith("z") and value != 0:
        bit_index = int(name[1:].lstrip("0"))
        out_value |= 1 << bit_index

print(out_value)
