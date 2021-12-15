import sys
from heapq import heapify, heappop, heappush


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


def calc_smallest_risk(grid):
    queue = [(0, 0, 0)]
    heapify(queue)
    seen = {}

    while len(queue):
        v, i, j = heappop(queue)

        for ni, nj in iter_neighbours(grid, (i, j)):
            nv = grid[ni][nj] + v
            if (ni, nj) not in seen or nv < seen[(ni, nj)]:
                seen[(ni, nj)] = nv
                heappush(queue, (nv, ni, nj))

    return seen[(len(grid) - 1, len(grid[0]) - 1)]


def part_1(grid):
    return calc_smallest_risk(grid)


def part_2(grid):
    grid = grow_grid(grid)

    return calc_smallest_risk(grid)


data = read_input()
print(part_1(data))
print(part_2(data))
