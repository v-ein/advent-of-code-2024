import re

from puzzle_input import puzzle_input


# This one is really easier with regex
pattern = """
M.S
.A.
M.S
"""

def cook_regex(pattern, text_width):
    pat_width = pattern.index("\n")
    pattern = pattern.replace("\n", f".{{{text_width - pat_width}}}")
    return f"(?={pattern})"

def count_matches(pattern, text, text_width):
    regexp = cook_regex(pattern, text_width)
    return len(re.findall(regexp, text))

def transpose(pattern):
    lines = pattern.split()
    return "\n".join("".join(line_tuple) for line_tuple in zip(*lines))

def flip_180(pattern):
    return pattern[::-1]


pattern = pattern.strip()
puzzle_input = puzzle_input.strip()
width = puzzle_input.index("\n") + 1
# \n complicates regexps, but we can't simply join the lines - we need to prevent
# wrapping around the edge. For this text, spaces a good enough.
text = puzzle_input.replace("\n", " ")

total_count = (
    count_matches(pattern, text, width) +
    count_matches(transpose(pattern), text, width) +
    count_matches(flip_180(pattern), text, width) +
    count_matches(transpose(flip_180(pattern)), text, width)
)

print(total_count)
