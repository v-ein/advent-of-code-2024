import __main__
from contextlib import suppress
from pathlib import Path
import re


def read_input_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


puzzle_input = ""

name = Path(__main__.__file__).stem
m = re.match(r"day(\d+)", name, re.IGNORECASE)

if m:
    with suppress(Exception):
        puzzle_input = read_input_file(f"input{m.group(1)}.txt")

if not puzzle_input:
    puzzle_input = read_input_file("input.txt")
