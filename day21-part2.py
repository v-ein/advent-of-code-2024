import itertools
from puzzle_input import puzzle_input


door_codes = puzzle_input.strip().splitlines()

door_kbd = """
789
456
123
.0A
""".strip()

robot_kbd = """
.^A
<v>
""".strip()

robot_cnt = 26


# First of all build all optimal paths between keys on a robot keyboard
def find_robo_path(f, t):
    if f == t:
        return "A"
    # Yeah not very optimal but the API reads better :)
    fpos = robot_kbd.index(f)
    tpos = robot_kbd.index(t)
    fy, fx = divmod(fpos, 4)
    ty, tx = divmod(tpos, 4)
    xpath = ("<" if tx < fx else ">") * abs(tx - fx)
    ypath = ("^" if ty < fy else "v") * abs(ty - fy)

    # On the robot keyboard, most diagonal movement can only be done one way.
    # It can be shown that the choice between two movements only happen in the right
    # part of the keyboard (^A / v>), and in that case we should move by X first
    # if moving from column 3 to column 2, and by Y first if moving in the other
    # direction.
    # So we only prefer Y when moving from top row to the left column or when
    # moving from column 2 to somewhere.
    # Ideally we should be calculating these paths and choosing the optimal ones.

    return (ypath + xpath + "A") if (fy == 0 and tx == 0 or fx == 1) else (xpath + ypath + "A")


robo_paths = {f + t: find_robo_path(f, t) for f, t in itertools.product("<v>^A", repeat=2)}
robo_costs = {ft: 1 for ft in robo_paths}


def calc_cost(path):
    return sum([robo_costs[f + t] for f, t in zip("A" + path, path)])


for i in range(robot_cnt - 1):
    robo_costs = {ft: calc_cost(robo_paths[ft]) for ft in robo_costs}


def build_path(code):
    total = 0
    for f, t in zip("A" + code, code):
        fpos = door_kbd.index(f)
        tpos = door_kbd.index(t)
        fy, fx = divmod(fpos, 4)
        ty, tx = divmod(tpos, 4)
        # For diagonal moves, there are two possible paths from f to t: by x first
        # or by y first.  However, in certain cases one of the paths is blocked by
        # the gap on the keyboard.
        xpath = ("<" if tx < fx else ">") * abs(tx - fx)
        ypath = ("^" if ty < fy else "v") * abs(ty - fy)
        p1 = xpath + ypath + "A"
        p2 = ypath + xpath + "A"
        if p1 != p2:
            # Is one of them blocked?
            bad_y = door_kbd.index(".") // 4
            if fx == 0 and ty == bad_y:
                # We can only start horizontally - p1 is the only path
                p2 = p1
            elif tx == 0 and fy == bad_y:
                # We can only end horizontally - p2 is the only path
                p1 = p2
        
        cost = calc_cost(p1)
        if p2 != p1:
            cost = min(cost, calc_cost(p2))
        total += cost

    return total


def calc_complexity(code: str):
    num = int(code.lstrip("0").rstrip("A"))
    cost = build_path(code)
    return num * cost


total = sum([calc_complexity(code) for code in door_codes])
print(total)
