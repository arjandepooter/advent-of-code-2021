import sys
from collections import defaultdict


def parse_point(part):
    x, y = part.split(",")
    return (int(x), int(y))


def parse_line(line):
    start, end = [parse_point(part) for part in line.split(" -> ")]
    return (start, end)


def read_input():
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    return ([parse_line(line) for line in lines],)


def get_hit_counts(lines):
    counts = defaultdict(int)

    for (x1, y1), (x2, y2) in lines:
        number_of_points = max(abs(x2 - x1), abs(y2 - y1)) + 1

        for offset in range(number_of_points):
            x = x1
            y = y1
            if y1 != y2:
                y = y1 + (offset if y1 < y2 else -offset)
            if x1 != x2:
                x = x1 + (offset if x1 < x2 else -offset)

            counts[(x, y)] += 1

    return counts


def part_1(lines):
    lines = [
        ((x1, y1), (x2, y2)) for ((x1, y1), (x2, y2)) in lines if x1 == x2 or y1 == y2
    ]
    hit_counts = get_hit_counts(lines)
    return len([True for hit_count in hit_counts.values() if hit_count > 1])


def part_2(lines):
    hit_counts = get_hit_counts(lines)
    return len([True for hit_count in hit_counts.values() if hit_count > 1])


data = read_input()
print(part_1(*data))
print(part_2(*data))
