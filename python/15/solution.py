import sys
from collections import *
from functools import *
from itertools import *


def parse_line(line):
    return [int(n) for n in line]


def read_input():
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]

    return [parse_line(line) for line in lines]


def iter_neighbours(grid, point):
    i, j = point
    for di, dj in (0, 1), (1, 0), (0, -1), (-1, 0):
        if 0 <= (ni := i + di) < len(grid) and 0 <= (nj := j + dj) < len(grid[0]):
            yield (ni, nj)


def grow_grid(grid, x=5):
    new_grid = []
    for i in range(x):
        for line in grid:
            new_line = []
            for j in range(x):
                new_line += [((i + j + n - 1) % 9) + 1 for n in line]
            new_grid.append(new_line)
    return new_grid


def path(grid):
    queue = deque([(0, 0)])
    seen = {}

    while len(queue):
        i, j = queue.pop()
        v = seen.get((i, j), 0)

        for ni, nj in iter_neighbours(grid, (i, j)):
            nv = grid[ni][nj] + v
            if ((ni, nj) in seen and nv < seen[(ni, nj)]) or (ni, nj) not in seen:
                seen[(ni, nj)] = nv
                queue.appendleft((ni, nj))

    return seen[(len(grid) - 1, len(grid[0]) - 1)]


def part_1(data):
    return path(data)


def part_2(data):
    grid = grow_grid(data)

    return path(grid)


data = read_input()
print(part_1(data))
print(part_2(data))
