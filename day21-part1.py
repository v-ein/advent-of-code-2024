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

robot_cnt = 3

def build_path(code, kbd=door_kbd, level=robot_cnt):
    # Level == 0 is the user himself; to enter the code he needs to just type it
    # on the keyboard.
    if level <= 0:
        return code
    path = ""
    for f, t in zip("A" + code, code):
        fpos = kbd.index(f)
        tpos = kbd.index(t)
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
            bad_y = kbd.index(".") // 4
            if fx == 0 and ty == bad_y:
                # We can only start horizontally - p1 is the only path
                p2 = p1
            elif tx == 0 and fy == bad_y:
                # We can only end horizontally - p2 is the only path
                p1 = p2
        
        p1 = build_path(p1, robot_kbd, level - 1)
        if p2 != p1:
            p2 = build_path(p2, robot_kbd, level - 1)
            if len(p2) < len(p1):
                p1 = p2
        path += p1

    return path


dir_map = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1),
}

# For debugging
def show_moves(code, level=robot_cnt):
    keys = [code]
    for i in range(level):
        kbd = door_kbd if i == level - 1 else robot_kbd
        out = ""
        y, x = divmod(kbd.index("A"), 4)
        for c in code:
            if c == "A":
                out += kbd[y*4 + x]
            else:
                dx, dy = dir_map[c]
                x += dx
                y += dy
                assert 0 <= x < 3 and 0 <= y <= len(kbd) // 4
        code = out
        keys.append(code)

    def split(key: str, out):
        pos = 0
        pieces = []
        for o in out:
            start = pos
            for i in range(len(o)):
                pos = key.index("A", pos) + 1
            pieces.append(key[start:pos])
        return pieces
    
    split_keys = [list(keys[level])]
    for i in range(level - 1, -1, -1):
        split_keys.insert(0, split(keys[i], split_keys[0]))

    widths = [len(piece) + 3 for piece in split_keys[0]]
    formatted = ["".join([piece.ljust(w) for w, piece in zip(widths, split_key)]) for split_key in split_keys]

    return formatted


def calc_complexity(code: str):
    num = int(code.lstrip("0").rstrip("A"))
    path = build_path(code)
    return num * len(path)


total = sum([calc_complexity(code) for code in door_codes])
print(total)
