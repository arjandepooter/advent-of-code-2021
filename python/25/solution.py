import sys
from typing import Set, TextIO, Any, Tuple
from collections import *
from functools import *
from itertools import *

Data = Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]], int, int]
Result = int


def parse_input(buffer: TextIO) -> Data:
    east = set()
    south = set()
    lines = [line.strip() for line in buffer.readlines() if line.strip()]

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == ">":
                east.add((x, y))
            elif c == "v":
                south.add((x, y))

    return (east, south, len(lines[0]), len(lines))


def part_1(data: Data) -> Result:
    east, south, width, height = data
    moved = True
    steps = 0

    while moved:
        moved = False
        new_east = set()
        new_south = set()

        for x, y in east:
            if not ((x + 1) % width, y) in south and not ((x + 1) % width, y) in east:
                new_east.add(((x + 1) % width, y))
                moved = True
            else:
                new_east.add((x, y))
        east = new_east
        for x, y in south:
            if not (x, (y + 1) % height) in east and not (x, (y + 1) % height) in south:
                new_south.add((x, (y + 1) % height))
                moved = True
            else:
                new_south.add((x, y))
        south = new_south

        steps += 1

    return steps


if __name__ == "__main__":
    if sys.stdin.isatty():
        import os

        data = parse_input(
            open(os.path.join(os.path.dirname(__file__), "test_input.txt"))
        )

    else:
        data = parse_input(sys.stdin)
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: 🎄")
