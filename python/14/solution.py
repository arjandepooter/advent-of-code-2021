import sys
from functools import cache


def read_input():
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    template = list(lines[0])
    rules = []

    for line in lines[1:]:
        a, b = line.split(" -> ")
        rules.append((tuple(list(a)), b))

    return (template, dict(rules))


def merge_counts(a, b):
    c = {}
    for k in set(a.keys()) | set(b.keys()):
        c[k] = a.get(k, 0) + b.get(k, 0)
    return c


def counts(template, rules, steps):
    @cache
    def wrapped(a, b, steps):
        if steps == 0:
            return {a: 1}
        m = rules[(a, b)]
        return merge_counts(wrapped(a, m, steps - 1), wrapped(m, b, steps - 1))

    result = {}
    for a, b in zip(template, template[1:]):
        result = merge_counts(result, wrapped(a, b, steps))

    result[template[-1]] += 1

    return result


def part_1(template, rules):
    c = counts(template, rules, 10)

    return max(c.values()) - min(c.values())


def part_2(template, rules):
    c = counts(template, rules, 40)

    return max(c.values()) - min(c.values())


data = read_input()
print(part_1(*data))
print(part_2(*data))
