from typing import List

from puzzle_input import puzzle_input


lines = puzzle_input.strip().splitlines()
parts = [line.split(": ") for line in lines]
equs = [(int(p[0]), [int(x) for x in p[1].split()]) for p in parts]

def compute(nums: List[int], operators: int) -> int:
    result = nums[0]
    for i, num in enumerate(nums[1:]):
        if (operators >> i) & 1:
            result *= num
        else:
            result += num
    return result

def is_equ_valid(nums, result) -> bool:
    for i in range(1 << (len(nums) - 1)):
        if compute(nums, i) == result:
            return True
    return False

total = sum([result for result, nums in equs if is_equ_valid(nums, result)])
print(total)
