from typing import Dict
from puzzle_input import puzzle_input

stones = [int(x) for x in puzzle_input.split()]

def blink(stone):
    if stone == 0:
        return (1, -1)
    else:
        text = str(stone)
        if len(text) % 2 == 0:
            half = len(text) // 2
            return (int(text[:half]), int(text[half:]))
        else:
            return (stone * 2024, -1)


# If we do calculations straight by converting each stone separately in the `stones`
# list, the list will quickly grow into something of unmanageable length, leading to
# zillions of calculations on every blink.  However, the way stones are transformed,
# there are many repeating numbers within the same generation.  We just keep the distinct
# numbers and how many each of them can be found in the line of stones.  And, by the way,
# the order of stones does not affect calculations so we don't care whether it's a line
# or a triangle or a circle or just a pile.

pile = { stone: 1 for stone in stones }

for i in range(75):
    new_pile: Dict[int, int] = {}
    for stone, count in pile.items():
        a, b = blink(stone)
        new_pile[a] = new_pile.get(a, 0) + count
        if b >= 0:
            new_pile[b] = new_pile.get(b, 0) + count

    pile = new_pile

print(sum(pile.values()))
