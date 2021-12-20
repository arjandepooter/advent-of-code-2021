import sys
from collections import defaultdict
from math import isqrt
from typing import Tuple

Area = Tuple[int, int, int, int]


def read_input() -> Area:
    line = sys.stdin.readline()
    xs, ys = line[13:].split(", ")
    x1, x2 = [int(x) for x in xs[2:].split("..")]
    y1, y2 = [int(y) for y in ys[2:].split("..")]
    return x1, x2, y1, y2


def triangle(n: int) -> int:
    return (n * (n + 1)) // 2


def is_triangle(n: int) -> bool:
    return triangle(reverse_triangle(n)) == n


def reverse_triangle(n: int) -> int:
    return (isqrt(8 * n + 1) - 1) // 2


def hits_after_t(target: Area, dy: int):
    pass


def part_1(target: Area) -> int:
    _, _, min_y, _ = target
    return (min_y ** 2 + min_y) // 2


def part_2(target: Area) -> int:
    min_x, max_x, min_y, max_y = target

    # combinations of y and t
    yt_combinations = defaultdict(list)
    for dy in range(-min_y + 1):
        top = triangle(dy)

    return 0


if __name__ == "__main__":
    if sys.stdin.isatty():
        import pytest

        sys.exit(pytest.main([__file__]))
    data = read_input()
    print(part_1(data))
    print(part_2(data))


def test_triangle():
    assert triangle(0) == 0
    assert triangle(4) == 10
    assert triangle(7) == 28


def test_reverse_triangle():
    assert reverse_triangle(0) == 0
    assert reverse_triangle(10) == 4
    assert reverse_triangle(14) == 4
    assert reverse_triangle(15) == 5
    assert reverse_triangle(16) == 5
    assert reverse_triangle(17) == 5
    assert reverse_triangle(18) == 5
    assert reverse_triangle(19) == 5
    assert reverse_triangle(20) == 5
    assert reverse_triangle(21) == 6


def test_is_triangle():
    assert is_triangle(0) == True
    assert is_triangle(10) == True
    assert is_triangle(28) == True
    assert is_triangle(11) == False


def test_part1():
    area: Area = (20, 30, -10, -5)

    assert part_1(area) == 45


def test_part2():
    area: Area = (20, 30, -10, -5)

    assert part_2(area) == 112
