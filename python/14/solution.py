import sys
from collections import Counter
from functools import cache, reduce


def read_input():
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    template = list(lines[0])
    rules = []

    for line in lines[1:]:
        a, b = line.split(" -> ")
        rules.append((tuple(list(a)), b))

    return (template, dict(rules))


def counts(template, rules, steps):
    @cache
    def wrapped(a, b, steps):
        if steps == 0:
            return Counter([a])
        m = rules[(a, b)]
        return wrapped(a, m, steps - 1) + wrapped(m, b, steps - 1)

    return reduce(
        lambda acc, pair: acc + wrapped(pair[0], pair[1], steps),
        zip(template, template[1:]),
        Counter([template[-1]]),
    )


def part_1(template, rules):
    c = counts(template, rules, 10)

    return max(c.values()) - min(c.values())


def part_2(template, rules):
    c = counts(template, rules, 40)

    return max(c.values()) - min(c.values())


data = read_input()
print(part_1(*data))
print(part_2(*data))
