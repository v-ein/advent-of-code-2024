from puzzle_input import puzzle_input


word = "XMAS"

# We could also use a regex with a .{n} between individual characters of `word`,
# and it would probably make a much simpler solution.

def count_horizontal(lines):
    return sum([line.count(word) + line[::-1].count(word) for line in lines])

def count_vertical(lines):
    # let's just transpose the text "matrix"
    transposed = list("".join(line_tuple) for line_tuple in zip(*lines))
    return count_horizontal(transposed)

def count_diagonal(lines, offset):
    pad_len = len(lines) - 1
    final_len = len(lines[0]) + pad_len
    if offset > 0:
        skewed_lines = [ (" "*i + line).ljust(final_len) for i, line in enumerate(lines) ]
    else:
        skewed_lines = [ (line + " "*i).ljust(i).rjust(final_len) for i, line in enumerate(lines) ]

    return count_vertical(skewed_lines)


lines = puzzle_input.strip().split()

total_count = (
        count_horizontal(lines) +
        count_vertical(lines) +
        count_diagonal(lines, +1) +
        count_diagonal(lines, -1))

print(total_count)
