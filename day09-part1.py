from itertools import chain, zip_longest

from puzzle_input import puzzle_input


compact_map = [int(c) for c in puzzle_input.strip().replace("\n", "")]

# Some itertools magic
map_pieces = [ [file_id] * file_len + [-1] * gap_len
    for file_id, (file_len, gap_len) in enumerate(zip_longest(compact_map[::2], compact_map[1::2], fillvalue=0)) ]
# Flatten it - now the map contains file IDs for each block, -1 where the gaps are
map = list(chain.from_iterable(map_pieces))

# Now this is dumb but quick to implement
head_idx = 0
tail_idx = len(map) - 1
while head_idx < tail_idx:
    if map[head_idx] < 0:
        map[head_idx] = map[tail_idx]
        map[tail_idx] = -1
        while head_idx < tail_idx and map[tail_idx] < 0:
            tail_idx -= 1
    head_idx += 1

# Go count them!
checksum = sum([ i * file_id for i, file_id in enumerate(map) if file_id >= 0 ])
print(checksum)
