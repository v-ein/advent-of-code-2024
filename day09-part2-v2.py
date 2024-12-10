from puzzle_input import puzzle_input


compact_map = [int(c) for c in puzzle_input.strip().replace("\n", "")]

files = [ (-1 if id %2 else id // 2, chunk_len) for id, chunk_len in enumerate(compact_map) ]

tail_idx = len(files) - 1
# This will make sure each file is only moved once
move_id = len(files) // 2
while tail_idx > 0:
    file_id, file_len = files[tail_idx]
    if file_id == move_id:
        # Next time we'll be moving the file with a lower id
        move_id -= 1
        # Look up for a gap that can hold this file
        for i, (cur_id, cur_len) in enumerate(files):
            # This should be faster than slicing `files` on every iteration
            if i >= tail_idx:
                break
            if cur_id < 0 and cur_len >= file_len:
                # Reclaim file's space
                files[tail_idx] = (-1, file_len)
                # Move the file to the new position (onto the gap's place)
                files[i] = (file_id, file_len)
                # If there's space remaining in the gap, keep it after the file
                if cur_len > file_len:
                    files.insert(i + 1, (-1, cur_len - file_len))
                    # Compensate for indices shift
                    tail_idx += 1
                break
    # Go check next file
    tail_idx -= 1

# Go count them!
checksum = 0
pos = 0
for id, chunk_len in files:
    if id > 0:
        # Now the file's checksum can be computed based on the sum of a finite arithmetic progression
        checksum += id * int(chunk_len * (2*pos + chunk_len - 1) / 2)
    pos += chunk_len

print(checksum)
