import re

from puzzle_input import puzzle_input


# the original data has no linefeeds; they just got copy-pasted from the browser,
# and they affect regexp matches
puzzle_input = puzzle_input.strip().replace("\n", "")

# first removing all the pieces between "don't" and "do"
filtered_input = re.sub(r"don't\(\).*?(?:do\(\)|$)", "", puzzle_input)
# now extracting the multiplied numbers
numbers_in_text = re.findall(r"mul\((\d+),(\d+)\)", filtered_input)
muls = [ int(a)*int(b) for a, b in numbers_in_text ]
print(sum(muls))
