from itertools import accumulate

from puzzle_input import puzzle_input


def show_map(files):
    buf = bytearray(b"." * 200)
    for id, (pos, length) in enumerate(files):
        assert buf[pos : pos+length].count(b".") == length, f"Overlapping regions: ({pos, length}) clashes with {buf[pos : pos+length].decode('utf-8')}"
        buf[pos : pos+length] = bytes([id + ord("0")]) * length
    return buf.decode("utf-8")


compact_map = [int(c) for c in puzzle_input.strip().replace("\n", "")]

# This will keep a list of (pos, len) pairs
chunks = list(zip([0] + list(accumulate(compact_map)), compact_map))
files = chunks[::2]
gaps = chunks[1::2]

for file_id, (file_pos, file_len) in reversed(list(enumerate(files))):
    for gap_id, (gap_pos, gap_len) in enumerate(gaps):
        # We don't want to move the file to the right
        if gap_pos >= file_pos:
            break
        # Does it fit?
        if gap_len >= file_len:
            files[file_id] = (gap_pos, file_len)
            if gap_len > file_len:
                gaps[gap_id] = (gap_pos + file_len, gap_len - file_len)
            else:
                del gaps[gap_id]
            break

# Now the file's checksum can be computed based on the sum of a finite arithmetic progression
checksum = sum([ file_id * int(file_len * (2*file_pos + file_len - 1) / 2)
                    for file_id, (file_pos, file_len) in enumerate(files) ])

print(checksum)
