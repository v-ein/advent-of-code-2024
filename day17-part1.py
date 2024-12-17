import re
from typing import List
from puzzle_input import puzzle_input


# Here comes the real joy for a whole-life asm programmer! :)

input_re = r"Register A:\s*(\d+)\s*\nRegister B:\s*(\d+)\s*\nRegister C:\s*(\d+)\s*\n+Program:\s*((?:\d+,?)+)"
m = re.search(input_re, puzzle_input)
assert m, "Failed to parse input"

program = [int(s) for s in m[4].split(",")]
regs=[int(m[i]) for i in range(1, 4)]
out_values: List[int] = []
cp = 0


def get_combo(x):
    return x if x < 4 else regs[x - 4]


def adv(x):
    regs[0] = regs[0] // (1 << get_combo(x))

def bxl(x):
    regs[1] ^= x

def bst(x):
    regs[1] = get_combo(x) % 8

def jnz(x):
    if regs[0] != 0:
        global cp
        cp = x

def bxc(x):
    regs[1] ^= regs[2]

def out(x):
    out_values.append(get_combo(x) % 8)

def bdv(x):
    regs[1] = regs[0] // (1 << get_combo(x))

def cdv(x):
    regs[2] = regs[0] // (1 << get_combo(x))


opcodes_map = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]


# Go run the program
while 0 <= cp < len(program):
    opcode = program[cp]
    operand = program[cp + 1]
    cp += 2
    opcodes_map[opcode](operand)


print(",".join([str(x) for x in out_values]))
