import sys
from typing import List


def read_input():
    return [int(line) for line in sys.stdin.readlines() if line.strip()]


def number_of_ascending_pairs(l: List[int], offset: int):
    acc = 0

    for (a, b) in zip(l, l[offset:]):
        if a < b:
            acc += 1

    return acc


def part_1(data):
    return number_of_ascending_pairs(data, 1)


def part_2(data):
    return number_of_ascending_pairs(data, 3)


data = read_input()
print(part_1(data))
print(part_2(data))
