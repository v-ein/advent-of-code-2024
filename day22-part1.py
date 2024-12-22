from puzzle_input import puzzle_input

seeds = [int(line) for line in puzzle_input.strip().splitlines()]

rounds = 2000

def next_rand(s):
    s = (s ^ s << 6) & 0xff_ffff
    s = (s ^ s >> 5) & 0xff_ffff
    s = (s ^ s << 11) & 0xff_ffff
    return s

def final_rand(s):
    for i in range(rounds):
        s = next_rand(s)
    return s


finals = [final_rand(s) for s in seeds]
total = sum(finals)
print(total)
