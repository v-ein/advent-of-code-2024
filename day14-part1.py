import re
from puzzle_input import puzzle_input

width = 101
height = 103

_puzzle_input = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

# width = 11
# height = 7
seconds = 100

robot_re = r"p=(\d+),\s*(\d+)\s*v=([+-]?\d+),\s*([+-]?\d+)"

# Parse the input into a list of ints
coords = [(int(x) for x in m) for m in re.findall(robot_re, puzzle_input)]

def move_robot(x, y, vx, vy):
    return ((x + vx*seconds) % width, (y + vy*seconds) % height, vx, vy)

coords = [move_robot(*c) for c in coords]

mid_x = width // 2
mid_y = height // 2

total = (
    len([None for x, y, vx, vy in coords if x < mid_x and y < mid_y]) *
    len([None for x, y, vx, vy in coords if x < mid_x and y > mid_y]) *
    len([None for x, y, vx, vy in coords if x > mid_x and y < mid_y]) *
    len([None for x, y, vx, vy in coords if x > mid_x and y > mid_y])
)

print(total)
