from copy import deepcopy
from enum import Enum
from typing import List, Tuple

from puzzle_input import puzzle_input


directions = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
]
footsteps = "^>v<"

puzzle_input = puzzle_input.strip()
# This looks pretty inefficient but who promised runtime efficiency? :)
# Remember, here I'm trying to save on development time, not run time.
map = [ list(line) for line in puzzle_input.split() ]

start_pos = puzzle_input.index("^")
# +1 compensates for "\n" in puzzle_input
y, x = divmod(start_pos, len(map[0]) + 1)
dir_idx = 0


# Just a debugging helper
def lookaround():
    w = 10
    h = 5
    return ["".join(l[x-w:x+w+1]) for l in map[y-h:y+h+1]]


# This is a rather dump way of solving it, but it's easy to implement.  Yes, it's
# very inefficient, in fact it's so slow that I added a "progressbar" :).
Ending = Enum("Ending", "NORMAL EXHAUSTED LOOP")
def route(map: List[List[str]], x: int, y: int, dir_idx: int, obstr_step: int) -> Tuple[Ending, int, Tuple[int, int]]:
    step = -1
    map = deepcopy(map)
    map[y][x] = "."
    obstr_pos = (0, 0)

    while True:
        step += 1

        dx, dy = directions[dir_idx]
        # Next position
        new_x = x + dx
        new_y = y + dy

        # Can we go there?
        if not (0 <= new_y < len(map) and 0 <= new_x < len(map[new_y])):
            return (Ending.EXHAUSTED if step < obstr_step else Ending.NORMAL, step, (0, 0))

        if step == obstr_step:
            if map[new_y][new_x] != ".":
                return (Ending.NORMAL, step, (0, 0))
            map[new_y][new_x] = "#"
            obstr_pos = (new_x, new_y)

        if map[new_y][new_x] == "#":
            # Note: this does not account for the case where we close ourselves
            # in a single cell - but it cannot actually happen other than at the
            # starting point (and our input data removes such a chance).
            dir_idx = (dir_idx + 1) % len(directions)
        else:
            # Check if we're stepping into a loop
            if map[y][x] == footsteps[dir_idx]:
                return (Ending.LOOP, step, obstr_pos)

            map[y][x] = footsteps[dir_idx]
            x, y = new_x, new_y


ending, total_steps, coords = route(map, x, y, 0, -1)

obstructions = set()
percent_bound = -1

for obstr_step in range(total_steps):
    percent = obstr_step*100 // total_steps
    if percent >= percent_bound:
        percent_bound = percent + 5
        print(f"{percent}% completed")

    ending, steps, coords = route(map, x, y, 0, obstr_step)
    # just in case...
    if ending == Ending.EXHAUSTED:
        break
    if ending == Ending.LOOP:
        obstructions.add(coords)

print(len(obstructions))
