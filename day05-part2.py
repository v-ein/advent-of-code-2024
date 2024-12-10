from typing import Any, Dict, Set

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

    if not is_correct:
        # There's a hundred ways to skin this cat.  Let's use a stupid one.
        # Remember dicts in Python are ordered.
        ordered: Dict[str, Any] = dict()
        # Iterating over the list of pages, moving all pages that go in the wrong
        # order over to the end of the list.
        while pages:
            page = pages.pop(0)
            if page in rules:
                reorder_set = rules[page] & ordered.keys()
                for wrong_page in reorder_set:
                    del ordered[wrong_page]
                    pages.append(wrong_page)

            ordered[page] = None

        pages = list(ordered.keys())
        total += int(pages[len(pages) // 2])

print(total)
