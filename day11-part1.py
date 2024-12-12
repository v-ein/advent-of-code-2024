from puzzle_input import puzzle_input

stones = [int(x) for x in puzzle_input.split()]

def blink_iter(stones):
    for stone in stones:
        if stone == 0:
            yield 1
        else:
            text = str(stone)
            if len(text) % 2 == 0:
                half = len(text) // 2
                yield int(text[:half])
                yield int(text[half:])
            else:
                yield stone * 2024


for i in range(25):
    stones = list(blink_iter(stones))

print(f"25 times: {len(stones)}")
