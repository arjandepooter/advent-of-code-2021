import sys
from collections import deque
from itertools import count, product

SIZE = 10


def parse_line(line):
    return [int(n) for n in line]


def read_input():
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    return [parse_line(line) for line in lines]


def iter_neighbours(i, j):
    for di, dj in product(range(-1, 2), range(-1, 2)):
        if 0 <= (i + di) < SIZE and 0 <= (j + dj) < SIZE and not (di == 0 and dj == 0):
            yield (i + di, j + dj)


def iter_coords():
    return product(range(SIZE), range(SIZE))


def step(grid):
    grid = [[n + 1 for n in line] for line in grid]
    acc = 0
    queue = deque((i, j) for (i, j) in iter_coords() if grid[i][j] > 9)

    while len(queue):
        acc += 1
        i, j = queue.popleft()
        for ni, nj in iter_neighbours(i, j):
            grid[ni][nj] += 1
            if grid[ni][nj] == 10:
                queue.append((ni, nj))

    for i, j in iter_coords():
        if grid[i][j] > 9:
            grid[i][j] = 0

    return grid, acc


def part_1(grid):
    acc = 0
    for _ in range(100):
        grid, flashes = step(grid)
        acc += flashes
    return acc


def part_2(grid):
    for n in count(1):
        grid, flashes = step(grid)
        if flashes == SIZE * SIZE:
            return n


data = read_input()
print(part_1(data))
print(part_2(data))
