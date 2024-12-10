import re

from puzzle_input import puzzle_input


numbers_in_text = re.findall(r"mul\((\d+),(\d+)\)", puzzle_input)
muls = [ int(a)*int(b) for a, b in numbers_in_text ]
print(sum(muls))
