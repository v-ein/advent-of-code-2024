from puzzle_input import puzzle_input

pics = puzzle_input.strip().split("\n\n")

def read_pic(pic):
    # Returns a (heights, is_key) tuple
    lines = pic.splitlines()
    transposed = list("".join(line_tuple) for line_tuple in zip(*lines))
    filler = transposed[0][-1]
    heights = tuple([t.index(filler) for t in transposed])
    return (heights, (filler == "#"))

objects = [read_pic(pic) for pic in pics]
locks = { heights: 0 for heights, is_key in objects if not is_key }
keys = [heights for heights, is_key in objects if is_key]

for key in keys:
    for lock in locks:
        if all(a <= b for a, b in zip(lock, key)):
            locks[lock] += 1

print(sum(locks.values()))
