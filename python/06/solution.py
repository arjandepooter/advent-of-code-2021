import sys
from functools import cache


def read_input():
    return ([int(n) for n in sys.stdin.read().strip().split(",")],)


@cache
def grow_fish(t, days):
    result = 1
    for day in range(days - t, 0, -7):
        result += grow_fish(8, day - 1)
    return result


def part_1(data):
    return sum([grow_fish(n, 80) for n in data])


def part_2(data):
    return sum([grow_fish(n, 256) for n in data])


data = read_input()
print(part_1(*data))
print(part_2(*data))
