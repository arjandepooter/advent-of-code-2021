import sys
from collections import *
from functools import *
from itertools import *
from typing import Iterator, List, Set, Tuple


class Cuboid:
    def __init__(
        self, status: bool, x: Tuple[int, int], y: Tuple[int, int], z: Tuple[int, int]
    ):
        self.status = status
        self.x = x
        self.y = y
        self.z = z

    def magnitude(self):
        return max(
            abs(n)
            for n in [self.x[0], self.x[1], self.y[0], self.y[1], self.z[0], self.z[1]]
        )

    def has_overlap(self, other: "Cuboid") -> bool:
        return all(
            (
                self.x[0] <= other.x[1],
                self.x[1] >= other.x[0],
                self.y[0] <= other.y[1],
                self.y[1] >= other.y[0],
                self.z[0] <= other.z[1],
                self.z[1] >= other.z[0],
            )
        )

    def split(self, other: "Cuboid") -> List["Cuboid"]:
        if not self.has_overlap(other):
            return [self]

        result = []

        xs0, xs1 = self.x
        xo0, xo1 = other.x

        match (xo0 <= xs0, xo0 <= xs1, xo1 >= xs0, xo1 >= xs1):
            case (True, True, True, False):
                result.append(Cuboid(self.status, (xo1 + 1, xs1), self.y, self.z))
            case (False, True, True, False):
                result.append(Cuboid(self.status, (xs0, xo0 - 1), self.y, self.z))
                result.append(Cuboid(self.status, (xo1 + 1, xs1), self.y, self.z))
            case (False, True, True, True):
                result.append(Cuboid(self.status, (xs0, xo0 - 1), self.y, self.z))
        
        nx0, nx1 = max(xs0, xo0), min(xs1, xo1)

        ys0, ys1 = self.y
        yo0, yo1 = other.y

        match (yo0 <= ys0, yo0 <= ys1, yo1 >= ys0, yo1 >= ys1):
            case (True, True, True, False):
                result.append(Cuboid(self.status, (nx0, nx1), (yo1 + 1, ys1), self.z))
            case (False, True, True, False):
                result.append(Cuboid(self.status, (nx0, nx1), (ys0, yo0 - 1), self.z))
                result.append(Cuboid(self.status, (nx0, nx1), (yo1 + 1, ys1), self.z))
            case (False, True, True, True):
                result.append(Cuboid(self.status, (nx0, nx1), (ys0, yo0 - 1), self.z))
        
        ny0, ny1 = max(ys0, yo0), min(ys1, yo1)

        zs0, zs1 = self.z
        zo0, zo1 = other.z

        match (zo0 <= zs0, zo0 <= zs1, zo1 >= zs0, zo1 >= zs1):
            case (True, True, True, False):
                result.append(Cuboid(self.status, (nx0, nx1), (ny0, ny1), (zo1 + 1, zs1)))
            case (False, True, True, False):
                result.append(Cuboid(self.status, (nx0, nx1), (ny0, ny1), (zs0, zo0 - 1)))
                result.append(Cuboid(self.status, (nx0, nx1), (ny0, ny1), (zo1 + 1, zs1)))
            case (False, True, True, True):
                result.append(Cuboid(self.status, (nx0, nx1), (ny0, ny1), (zs0, zo0 - 1)))

        return result

    def dimensions(self) -> Iterator[Tuple[int, int]]:
        yield self.x
        yield self.y
        yield self.z

    def __len__(self) -> int:
        return reduce(lambda a, b: a * (b[1] - b[0] + 1), self.dimensions(), 1,)

    def __iter__(self) -> Iterator[Tuple[int, int, int]]:
        return product(
            range(self.x[0], self.x[1] + 1),
            range(self.y[0], self.y[1] + 1),
            range(self.z[0], self.z[1] + 1),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cuboid):
            return False
        return (
            self.status == other.status
            and self.x == other.x
            and self.y == other.y
            and self.z == other.z
        )

    def __hash__(self) -> int:
        return hash((self.status, self.x, self.y, self.z))

    def __repr__(self) -> str:
        return f"Cuboid({'ON' if self.status else 'OFF'}, {self.x[0]}..{self.x[1]}, {self.y[0]}..{self.y[1]}, {self.z[0]}..{self.z[1]})"


def parse_range(s: str) -> Tuple[int, int]:
    parts = s.split("..")
    return int(parts[0][2:]), int(parts[1])


def parse_line(line: str) -> Cuboid:
    # on x=2..47,y=-22..22,z=-23..27
    status, ranges = line.split(" ")
    status = status == "on"
    parts = [parse_range(part) for part in ranges.split(",")]

    return Cuboid(status, *parts)


def read_input() -> List[Cuboid]:
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    return [parse_line(line) for line in lines]


def part_1(cuboids: List[Cuboid]) -> int:
    points: Set[Tuple[int, int, int]] = set()
    for cuboid in cuboids:
        if cuboid.magnitude() > 50:
            continue
        for point in cuboid:
            if cuboid.status:
                points.add(point)
            else:
                if point in points:
                    points.remove(point)
    return len(points)


def part_2(cuboids: List[Cuboid]) -> int:
    filled: Set[Cuboid] = set()

    for cuboid in cuboids:
        to_add = set()
        to_remove = set()
        for other in filled:
            if cuboid.has_overlap(other):
                for new_cuboid in other.split(cuboid):
                    to_add.add(new_cuboid)
                to_remove.add(other)
        filled |= to_add
        filled -= to_remove

        if cuboid.status:
            filled.add(cuboid)
    
    return sum(len(cuboid) for cuboid in filled)


if __name__ == "__main__":
    if sys.stdin.isatty():
        import pytest
        sys.exit(pytest.main([__file__, '-v']))

    cuboids = read_input()
    print(part_1(cuboids))
    print(part_2(cuboids))


def test_split():
    cuboid1 = Cuboid(True, (0, 9), (0, 9), (0, 9))
    cuboid2 = Cuboid(False, (0, 6), (0, 6), (0, 6))

    assert cuboid1.split(cuboid2) == [
        Cuboid(True, (7, 9), (0, 9), (0, 9)),
        Cuboid(True, (0, 6), (7, 9), (0, 9)),
        Cuboid(True, (0, 6), (0, 6), (7, 9)),
    ]
