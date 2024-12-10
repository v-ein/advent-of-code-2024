from typing import List

from puzzle_input import puzzle_input


lines = puzzle_input.strip().splitlines()
parts = [line.split(": ") for line in lines]
equs = [(int(p[0]), [int(x) for x in p[1].split()]) for p in parts]

def compute(nums: List[int], operators: int) -> int:
    result = nums[0]
    for i, num in enumerate(nums[1:]):
        op = (operators >> 2*i) & 3
        if op == 0:
            result *= num
        elif op == 1:
            result += num
        elif op == 2:
            result = int(str(result) + str(num))
        else:
            # An alternative would be to use a ternary number, but this would 
            # take more time to write.
            return -1
    return result

def is_equ_valid(nums, result) -> bool:
    for i in range(3 << (2*(len(nums) - 2))):
        if compute(nums, i) == result:
            return True
    return False

# total = sum([result for result, nums in equs if is_equ_valid(nums, result)])

percent_bound = -1
total = 0
for i, (result, nums) in enumerate(equs):
    percent = i*100 // len(equs)
    if percent >= percent_bound:
        percent_bound = percent + 5
        print(f"{percent}% completed")

    if is_equ_valid(nums, result):
        total += result

print(total)
