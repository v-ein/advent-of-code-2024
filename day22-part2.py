from typing import Dict, Tuple
from puzzle_input import puzzle_input

seeds = [int(line) for line in puzzle_input.strip().splitlines()]

rounds = 2000

def next_rand(s):
    s = (s ^ s << 6) & 0xff_ffff
    s = (s ^ s >> 5) & 0xff_ffff
    s = (s ^ s << 11) & 0xff_ffff
    return s


def buyers_prices(seed):
    prices = [seed % 10]
    for i in range(rounds):
        seed = next_rand(seed)
        prices.append(seed % 10)
    return prices


bananas: Dict[Tuple[int, ...], int] = {}

for seed in seeds:
    prices = buyers_prices(seed)
    diffs = [b - a for a, b in zip(prices, prices[1:])]
    buyer_sequences = set()
    for seq, price in zip(zip(diffs, diffs[1:], diffs[2:], diffs[3:]), prices[4:]):
        if seq not in buyer_sequences:
            bananas[seq] = bananas.get(seq, 0) + price
            # Blocking further occurrences of the same sequence - the seller won't
            # have a chance to reach it anyway.
            buyer_sequences.add(seq)

print(max(bananas.values()))
