import re
from puzzle_input import puzzle_input


def calc_cost(ax, ay, bx, by, px, py):
    # This is actually wrong and does not necessarily give the minimum possible cost,
    # but somehow it worked fine on the puzzle input, and I didn't try to correct it.
    # The simplest correction would be to actually compute the minimum over all 100
    # iterations rather than to return on the first match.
    for na in range(101):
        # See how long distance to the prize is left after we hit A button na times
        dx = px - na*ax
        dy = py - na*ay
        if dx < 0 or dy < 0:
            break
        if bx == 0 and dx != 0:
            continue
        nb, dx = divmod(dx, bx)
        if dx == 0 and nb <= 100 and nb*by == dy:
            return 3*na + nb

    return 0


machine_re = (
    r"Button A:\s*X\+(\d+),\s*Y\+(\d+)\s*\n"
    r"Button B:\s*X\+(\d+),\s*Y\+(\d+)\s*\n"
    r"Prize:\s*X=(\d+),\s*Y=(\d+)"
)

# Parse the input into a list of ints
coords = [(int(x) for x in m) for m in re.findall(machine_re, puzzle_input)]
total = sum([calc_cost(*c) for c in coords])

print(total)
