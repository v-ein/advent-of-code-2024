from puzzle_input import puzzle_input

text_lines = puzzle_input.strip().splitlines()
reports=[[int(s) for s in l.split()] for l in text_lines]

def is_safe(report):
    diffs = [ b - a for a, b in zip(report, report[1:])]
    return (all(x*diffs[0] > 0 for x in diffs) > 0
        and max(diffs) <= 3 and min(diffs) >= -3)

def is_safe_dampened(report):
    if is_safe(report):
        return True

    for i in range(len(report)):
        if is_safe(report[:i] + report[i+1:]):
            return True

    return False

safe_reports = [r for r in reports if is_safe(r)]
print(len(safe_reports))
safe_reports = [r for r in reports if is_safe_dampened(r)]
print(len(safe_reports))
