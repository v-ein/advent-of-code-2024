from collections import namedtuple
import math
import re
from puzzle_input import puzzle_input


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


Grid = namedtuple("Grid", "start_a, max_a, step_a, start_b, max_b, step_b")

def find_grid(ax, bx, px):
    # Returns (start_a, max_a, step_a, start_b, max_b, step_b)
    # Note that the B grid goes downwards! (i.e. step_b is negative)
    gcd = math.gcd(ax, bx)
    step_a = bx//gcd

    # This can probably be solved mathematically but I decided to spend some CPU
    # time instead of spending my own time.
    for start_a in range(step_a):
        if (px - start_a*ax) % bx == 0:
            break
    else:
        # px can't be obtained as a sum (na*ax + nb*bx)
        return None

    start_b = (px - start_a*ax) // bx
    steps = (px - start_a*ax) // (abs(ax*bx) // gcd)
    max_a = start_a + steps * step_a
    step_b = -ax//gcd
    max_b = start_b + steps * step_b

    return Grid(start_a, max_a, step_a, start_b, max_b, step_b)


def validate_grid(grid, ax, bx, px):
    for na in range(grid.start_a, grid.max_a + 1, grid.step_a):
        assert (px - na*ax) % bx == 0, "Grid solutions are not all correct"

def calc_cost(ax, ay, bx, by, px, py):
    correction = 10000000000000
    px += correction
    py += correction

    assert ax > 0 and ay > 0 and bx > 0 and by > 0

    cost_a = 3
    cost_b = 1

    # On a single axis, for any solution (na, nb) we can get another solution by
    # adding (bx/gcd, -ax/gcd) to that pair.  This solution won't necessarily be
    # valid on the other axis, but here's an important observation: every
    # (bx/gcd, -ax/gcd) step will change the price by cost_a*bx/gcd - cost_b*ax/gcd,
    # which can either make it larger or smaller - *monotonically*! That is, if we
    # have multiple solutions, we'll only need to compare the first one and the last one.
    #
    # On a single axis (say, X), the na solutions thus form a grid with the step bx/gcdx and
    # an unknown (yet) starting point.  The starting point will be lower than bx/gcdx anyway.
    # On Y, solutions will also make a grid, and the two grids might match at some points,
    # with lcm(stepx, stepy) between the matches. For a match to exist, stepx and stepy must
    # be non-equal (or starting points must be equal).

    # I have a feeling that by abstracting out the operation of finding correspondence between
    # two grids, this code can be greatly simplified.  It's all about various grids, really.

    grid_x = find_grid(ax, bx, px)
    grid_y = find_grid(ay, by, py)
    if grid_x is None or grid_y is None:
        return 0

    # A quick test to make sure the X/Y grids really cross
    if grid_x.step_a == grid_y.step_a and (grid_x.start_a - grid_y.start_a) % grid_x.step_a != 0:
        return 0

    # Now find where the grids actually match on na
    stepx = grid_x.step_a
    stepy = grid_y.step_a
    match_step = lcm(stepx, stepy)
    for i in range(0, match_step, stepx):
        if (grid_x.start_a + i - grid_y.start_a) % grid_y.step_a == 0:
            break
    else:
        assert "Something wrong in the search for matches between the two grids"
    
    # Here goes our first candidate
    na1 = grid_x.start_a + i
    # total_matches is actually 1 lower than the total number of matches :),
    # but this suits our math well.
    total_matches = (grid_x.max_a - na1) // match_step

    # Now, while na1 is on both X and Y grids, and nb obtained from na1 for X/Y is also
    # on both grids, nb1 values for X and Y grids at this na1 point do not necessarily
    # match.  If we go to the next match between X/Y grids, nb1x will change by sbx step,
    # whereas nb1y will change by sby (see below).  At some point nb1x and nb1y will match,
    # and this will be our solution (the only solution).  Alternatively, if sbx and sby
    # are equal, there are either a set of total_matches solutions - or no solutions at all.

    nb1x = (px - na1*ax) // bx
    nb1y = (py - na1*ay) // by
    sbx = match_step * grid_x.step_b // grid_x.step_a
    assert sbx == match_step * grid_x.step_b / grid_x.step_a, "Somehow sbx is not a whole number"
    sby = match_step * grid_y.step_b // grid_y.step_a
    assert sby == match_step * grid_y.step_b / grid_y.step_a, "Somehow sby is not a whole number"

    if sbx != sby:
        # There's going to be only one point where the X/Y grids match on the nb value
        skip_matches, remainder = divmod(nb1y - nb1x, sbx - sby)
        if remainder != 0 or not 0 <= skip_matches <= total_matches:
            return 0
        na1 += skip_matches * match_step
        nb1x += skip_matches * sbx
        assert nb1x == nb1y + skip_matches * sby, "skip_matches doesn't look right"
        return cost_a*na1 + cost_b*nb1x

    elif nb1x != nb1y:
        # They will never match
        return 0
    
    else:
        # Any solution on X/Y grids will be fine; we need to choose the one with the lowest cost.
        nb1 = nb1x
        assert na1*ax + nb1*bx == px, "Ooops, got an invalid solution"
        assert na1*ay + nb1*by == py, "Ooops, got an invalid solution on Y"
        # And here is our last candidate.
        na2 = na1 + total_matches*match_step
        assert na2*ax <= px, "Hmmm... na2 too large?"
        nb2 = (px - na2*ax) // bx

        assert na2*ax + nb2*bx == px, "Ooops, got an invalid 2nd solution"
        assert na2*ay + nb2*by == py, "Ooops, got an invalid 2nd solution on Y"

        # Now choose which end provides us with the most profitable solution.  All the solutions
        # between (na1, nb1) and (na2, nb2) should be somewhere in the middle, not min or max.
        return min(cost_a*na1 + cost_b*nb1, cost_a*na2 + cost_b*nb2)



machine_re = (
    r"Button A:\s*X\+(\d+),\s*Y\+(\d+)\s*\n"
    r"Button B:\s*X\+(\d+),\s*Y\+(\d+)\s*\n"
    r"Prize:\s*X=(\d+),\s*Y=(\d+)"
)

# Parse the input into a list of ints
coords = [(int(x) for x in m) for m in re.findall(machine_re, puzzle_input)]
total = sum([calc_cost(*c) for c in coords])

print(total)
