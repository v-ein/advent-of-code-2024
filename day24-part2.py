import re
from typing import Dict, Tuple
from puzzle_input import puzzle_input


puzzle_input = puzzle_input.strip()
inputs_str, gates_str = puzzle_input.split("\n\n")

# We keep both forward and backward maps
gates: Dict[Tuple[str, str, str], str] = {}
outs: Dict[str, Tuple[str, str, str]] = {}
for m in re.findall(r"^(\S+)\s+(AND|OR|XOR)\s+(\S+)\s+->\s+(\S+)", gates_str, re.MULTILINE):
    a, b = m[0], m[2]
    if a > b:
        a, b = b, a

    gate = (a, b, m[1])
    outs[m[3]] = gate

    assert gate not in gates
    gates[gate] = m[3]


def bit_num(wire):
    return int(wire[1:].lstrip("0"))

max_wire = max(inputs_str.splitlines())
bits = bit_num(max_wire.split(":")[0]) + 1
assert len(gates) == 5*(bits - 1) + 2, "This program only supports schematics consisting of 5-gate adder blocks"


# First of all make sure x/y are not screwed up (per description, they shouldn't be
# swapped because gates *outputs* have been swapped, and x/y are pure inputs).
for i in range(bits):
    x = f"x{i:02}"
    y = f"y{i:02}"
    assert (x, y, "XOR") in gates
    assert (x, y, "AND") in gates


invalid_outs = set()

s = [""] * bits
p = [""] * bits

for i in range(bits):
    x = f"x{i:02}"
    y = f"y{i:02}"
    # We don't know yet if these s[i] and p[i] are valid
    s[i] = gates[(x, y, "XOR")]
    p[i] = gates[(x, y, "AND")]

if s[0] != "z00":
    invalid_outs.add(s[0])
    invalid_outs.add("z00")

sset = set(s)

# When talking about right-side and left-side AND and XOR gates, I'm referring to
# the classic circuit of a full adder block, consisting of two ANDs, two XORs, and
# one OR.  The elements connected directly to x/y are typically drawn on the left
# side of the schematic; the remaining AND/XOR are on the right side.
right_xors = { out: (a, b, op) for out, (a, b, op) in outs.items() if op == "XOR" and out not in sset }

for i in range(bits - 1, 0, -1):
    z = f"z{i:02}"
    if z not in right_xors:
        # Each of these will be accompanied by keys in right_xors that do not start with "z"
        invalid_outs.add(z)


for out in right_xors:
    if not out.startswith("z"):
        invalid_outs.add(out)

right_xor_inputs = set([a for a, b, op in right_xors.values()]) | set([b for a, b, op in right_xors.values()])
wrong_s = sset - right_xor_inputs
# s[0] is special: it connects directly to z00, not to another XOR
wrong_s ^= set([s[0]])
invalid_outs |= wrong_s

pset = set(p)

right_ands = { out: (a, b, op) for out, (a, b, op) in outs.items() if op == "AND" and out not in pset }
right_and_inputs = set([a for a, b, op in right_ands.values()]) | set([b for a, b, op in right_ands.values()])

ors = { out: (a, b, op) for out, (a, b, op) in outs.items() if op == "OR" }
or_inputs = set([a for a, b, op in ors.values()]) | set([b for a, b, op in ors.values()])

wrong_p = pset - or_inputs
# p[0] is special: it provides us the lowest carry bit directly, and therefore
# must not connect to any OR.
wrong_p ^= set([p[0]])
invalid_outs |= wrong_p

# On my data set, the right answer is actually obtained at this point.  Hope the subsequent
# checks do not break it :).

# Now, all ORs must be connected to right-side ANDs, except for the last OR, who
# provides us the most significant z bit.
wrong_c = ors.keys() - right_and_inputs
msb = f"z{bits:02}"
wrong_c ^= set([msb])
invalid_outs |= wrong_c

# All right-side ANDs must be connected to ORs
wrong_q = right_ands.keys() - or_inputs
invalid_outs |= wrong_q

# Now there still may be swaps between different adder blocks (e.g. between carry
# bits of two blocks), but we don't care since the checks above already provide us
# with the right answer.

print(",".join(sorted(invalid_outs)))
