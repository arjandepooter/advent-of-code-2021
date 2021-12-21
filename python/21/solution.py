import sys
from functools import cache
from typing import Iterator, TextIO, Tuple


def read_input(input: TextIO) -> Tuple[int, int]:
    p1 = int(input.readline().strip()[28:])
    p2 = int(input.readline().strip()[28:])
    return (p1, p2)


def np(p: int) -> int:
    return ((p - 1) % 10) + 1


def die() -> Iterator[int]:
    d = 0
    while True:
        yield d + 1
        d = (d + 1) % 100


@cache
def play(p1: int, p2: int, s1: int = 0, s2: int = 0, r: int = -1) -> Tuple[int, int]:
    if r % 6 == 0:
        s2 += p2
        if s2 >= 21:
            return (0, 1)
        r = 0
    elif r % 3 == 0:
        s1 += p1
        if s1 >= 21:
            return (1, 0)

    # dirty fix for not updating score in the first call
    if r == -1:
        r = 0

    w1 = w2 = 0
    for die in range(1, 4):
        n1, n2 = play(
            np(p1 + die if (0 <= r <= 2) else p1),
            np(p2 + die if (3 <= r <= 5) else p2),
            s1,
            s2,
            r + 1,
        )
        w1 += n1
        w2 += n2

    return (w1, w2)


def part_1(p1: int, p2: int) -> int:
    s1 = s2 = 0
    dice = die()
    rolls = 0

    while s1 < 1000 and s2 < 1000:
        p1 = np(p1 + next(dice) + next(dice) + next(dice))
        s1 += p1
        rolls += 3
        p1, p2, s1, s2 = p2, p1, s2, s1

    return rolls * min(s1, s2)


def part_2(p1: int, p2: int) -> int:
    return max(play(p1, p2))


if __name__ == "__main__":
    data = read_input(sys.stdin)
    print(part_1(*data))
    print(part_2(*data))
