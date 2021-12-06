import sys
from collections import deque


def read_input():
    return ([int(n) for n in sys.stdin.read().strip().split(",")],)


def build_fish_count_list(fishes):
    result = [0] * 9
    for fish in fishes:
        result[fish] += 1
    return deque(result)


def grow_fish(fishes, days):
    fish_per_t = build_fish_count_list(fishes)
    for d in range(days):
        fish_per_t.rotate(-1)
        fish_per_t[6] += fish_per_t[-1]
    return sum(fish_per_t)


def part_1(data):
    return grow_fish(data, 80)


def part_2(data):
    return grow_fish(data, 256)


data = read_input()
print(part_1(*data))
print(part_2(*data))
