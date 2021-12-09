import sys

from collections import deque
from functools import reduce


def parse_line(line):
    return list(map(int, line))


def read_input():
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    return [parse_line(line) for line in lines]


def iter_neighbours(data, x, y):
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if 0 <= (nx := x + dx) < len(data[0]) and 0 <= (ny := y + dy) < len(data):
            yield nx, ny


def find_lowest_parts(data):
    lowest_parts = []
    for j in range(len(data)):
        for i in range(len(data[0])):
            if all(data[j][i] < data[y][x] for x, y in iter_neighbours(data, i, j)):
                lowest_parts.append((i, j))

    return lowest_parts


def get_bassin_size(data, x, y):
    queue = deque([(x, y)])
    visited = set()

    while len(queue) > 0:
        x, y = queue.popleft()

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for nx, ny in iter_neighbours(data, x, y):
            nn = data[ny][nx]
            if nn != 9 and nn > data[y][x]:
                queue.append((nx, ny))

    return len(visited)


def part_1(data):
    return sum(1 + data[y][x] for x, y in find_lowest_parts(data))


def part_2(data):
    bassin_sizes = sorted(
        get_bassin_size(data, x, y) for (x, y) in find_lowest_parts(data)
    )

    return reduce(lambda a, b: a * b, bassin_sizes[-3:], 1)


data = read_input()
print(part_1(data))
print(part_2(data))
