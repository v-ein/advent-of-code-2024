from dataclasses import dataclass
from itertools import zip_longest

from puzzle_input import puzzle_input


compact_map = [int(c) for c in puzzle_input.strip().replace("\n", "")]

# This looks like an overkill; there are other (probably simpler) alternatives,
# it just evolved into a dataclass as I was writing this solution :)
# (see day09-part2-v2.py for a simpler piece of code).
@dataclass
class File:
    id: int
    file_len: int
    gap_len: int

# Some itertools magic
files = [ File(file_id, file_len, gap_len)
    for file_id, (file_len, gap_len) in enumerate(zip_longest(compact_map[::2], compact_map[1::2], fillvalue=0)) ]

tail_idx = len(files) - 1
# This will make sure each file is only moved once
max_id = len(files) - 1
while tail_idx > 0:
    file_to_move = files[tail_idx]
    if file_to_move.id > max_id:
        tail_idx -= 1
        continue

    need_space = file_to_move.file_len
    # Look up for a gap that can hold this file
    for i, file in enumerate(files):
        # This should be faster than slicing `files` on every iteration
        if i >= tail_idx:
            break
        if file.gap_len >= need_space:
            # Reclaim file's space
            files[tail_idx - 1].gap_len += file_to_move.file_len + file_to_move.gap_len
            # Move the file
            del files[tail_idx]
            files.insert(i + 1, file_to_move)
            # Compensate for file move
            tail_idx += 1
            # Adjust gaps
            file_to_move.gap_len = file.gap_len - need_space
            file.gap_len = 0
            break
    # Go check next file
    tail_idx -= 1
    max_id -= 1

# Go count them!
checksum = 0
pos = 0
for f in files:
    # Now the file's checksum can be computed based on the sum of a finite arithmetic progression
    checksum += f.id * int(f.file_len * (2*pos + f.file_len - 1) / 2)
    pos += f.file_len + f.gap_len

print(checksum)
