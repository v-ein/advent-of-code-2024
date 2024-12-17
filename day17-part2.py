import re
from typing import List
from puzzle_input import puzzle_input


# Here comes the real joy for a whole-life asm programmer! :)

input_re = r"Register A:\s*(\d+)\s*\nRegister B:\s*(\d+)\s*\nRegister C:\s*(\d+)\s*\n+Program:\s*((?:\d+,?)+)"
m = re.search(input_re, puzzle_input)
assert m, "Failed to parse input"

program = [int(s) for s in m[4].split(",")]
orig_regs=[int(m[i]) for i in range(1, 4)]


# Now this is cheating.  We only accept programs of a certain structure.
#  - it must end with a "jnz 0"
#  - there must be no other "jnz" instructions
#  - there must be only one "out" instruction in the loop
#  - there must be a single "adv" instruction in the loop, and it must be "adv 3".
# This lets us build the initial A value by partially reconstructing what the program
# will yield at various iterations of the loop formed by the last jnz instruction.
# 
# Let's validate the program.
prog_instr = program[::2]
assert program[-2:] == [3, 0], "The program must end with a jnz 0."
assert prog_instr.count(3) == 1, "There must be only one jnz instruction in the program."
assert prog_instr.count(5) == 1, "There must be only one out instruction in the program."
assert prog_instr.count(0) == 1, "There must be only one adv instruction in the program."
assert program[2*prog_instr.index(0) + 1] == 3, "The adv instruction must be 'adv 3'."


out_values: List[int] = []
cp = 0
regs = orig_regs[:]


def get_combo(x):
    return x if x < 4 else regs[x - 4]


def adv(x):
    regs[0] = regs[0] >> get_combo(x)

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
    x = get_combo(x) % 8
    out_values.append(x)

def bdv(x):
    regs[1] = regs[0] >> get_combo(x)

def cdv(x):
    regs[2] = regs[0] >> get_combo(x)


opcodes_map = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]


def run():
    global cp
    cp = 0
    # Go run the program
    while 0 <= cp < len(program):
        opcode = program[cp]
        operand = program[cp + 1]
        cp += 2
        opcodes_map[opcode](operand)

def run_with(a):
    regs[:] = orig_regs[:]
    regs[0] = a
    out_values.clear()
    run()


# Now, we'll start re-constructing the intial A value step-by-step, starting with
# the ending bytes of the program.
# Guess what... there might be multiple values in low bits of A that can produce
# the required digit in out_values, so we have to search recursively.
def check(init_a, tail_len):
    tail_len += 1
    if tail_len > len(program):
        return init_a
    tail = program[-tail_len:]
    # Now try various A values to get the tail in out_values
    init_a = init_a << 3
    for i in range(8):
        a = init_a | i
        run_with(a)
        if out_values == tail:
            a = check(a, tail_len)
            if a >= 0:
                return a
    return -1 

init_a = check(0, 0)
print(f"{init_a=}")
assert init_a >= 0, "Looks like we failed to find the initial A.  How could this happen?  Check the program logic."
run_with(init_a)
assert out_values == program, "Somehow the init_a value does not produce the program text."

