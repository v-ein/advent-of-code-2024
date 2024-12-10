from typing import Dict, Set

from puzzle_input import puzzle_input


rules_str, updates_str = puzzle_input.split("\n\n")

rules: Dict[str, Set[str]] = dict()
for rule in rules_str.strip().split():
    a, _, b = rule.partition("|")
    if not a in rules:
        rules[a] = set()
    rules[a].add(b)

total = 0
for update in updates_str.strip().split():
    pages = update.split(",")
    prev_set: Set[str] = set()
    is_correct = True
    for page in pages:
        if page in rules and (prev_set & rules[page]):
            is_correct = False
            break
        prev_set.add(page)

    if is_correct:
        total += int(pages[len(pages) // 2])

print(total)
