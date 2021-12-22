import sys
from functools import reduce
from itertools import product
from typing import Iterator, List, Set, Tuple


def parse_range(s: str) -> Tuple[int, int]:
    parts = s.split("..")
    return int(parts[0][2:]), int(parts[1])


def parse_line(line: str) -> "Cuboid":
    # on x=2..47,y=-22..22,z=-23..27
    status, ranges = line.split(" ")
    status = status == "on"
    parts = [parse_range(part) for part in ranges.split(",")]

    return Cuboid(status, *parts)


def read_input() -> List["Cuboid"]:
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    return [parse_line(line) for line in lines]


class Cuboid:
    def __init__(
        self,
        status: bool,
        x: Tuple[int, int],
        y: Tuple[int, int],
        z: Tuple[int, int],
    ):
        self.status = status
        self.x = x
        self.y = y
        self.z = z

    def reach(self) -> int:
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

    def dimensions(self) -> Iterator[Tuple[int, int]]:
        yield self.x
        yield self.y
        yield self.z

    def __sub__(self, other: "Cuboid") -> Iterator["Cuboid"]:
        if not self.has_overlap(other):
            yield self
            return

        (xs0, xs1), (ys0, ys1), (zs0, zs1) = self.dimensions()
        (xo0, xo1), (yo0, yo1), (zo0, zo1) = other.dimensions()
        nx = max(xs0, xo0), min(xs1, xo1)
        ny = max(ys0, yo0), min(ys1, yo1)

        if xo1 < xs1:
            yield Cuboid(self.status, (xo1 + 1, xs1), self.y, self.z)
        if xo0 > xs0:
            yield Cuboid(self.status, (xs0, xo0 - 1), self.y, self.z)
        if yo1 < ys1:
            yield Cuboid(self.status, nx, (yo1 + 1, ys1), self.z)
        if yo0 > ys0:
            yield Cuboid(self.status, nx, (ys0, yo0 - 1), self.z)
        if zo1 < zs1:
            yield Cuboid(self.status, nx, ny, (zo1 + 1, zs1))
        if zo0 > zs0:
            yield Cuboid(self.status, nx, ny, (zs0, zo0 - 1))

    def __len__(self) -> int:
        return reduce(
            lambda a, b: a * (b[1] - b[0] + 1),
            self.dimensions(),
            1,
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
        ranges = ", ".join(f"{a}..{b}" for a, b in self.dimensions())
        return f"Cuboid({'ON' if self.status else 'OFF'}, {ranges})"


def combine_cuboids(cuboids: List[Cuboid]) -> List[Cuboid]:
    combined: List[Cuboid] = []

    for cuboid in cuboids:
        new_combined: List[Cuboid] = []
        for other in combined:
            new_combined.extend(other - cuboid)
        if cuboid.status:
            new_combined.append(cuboid)
        combined = new_combined

    return combined


def part_1(cuboids: List[Cuboid]) -> int:
    combined = combine_cuboids([cuboid for cuboid in cuboids if cuboid.reach() <= 50])

    return sum(map(len, combined))


def part_2(cuboids: List[Cuboid]) -> int:
    combined = combine_cuboids(cuboids)

    return sum(map(len, combined))


if __name__ == "__main__":
    if sys.stdin.isatty():
        import pytest

        sys.exit(pytest.main([__file__, "-v"]))

    cuboids = read_input()
    print(part_1(cuboids))
    print(part_2(cuboids))


def test_split():
    cuboid1 = Cuboid(True, (0, 9), (0, 9), (0, 9))
    cuboid2 = Cuboid(False, (0, 6), (0, 6), (0, 6))

    assert list(cuboid1 - cuboid2) == [
        Cuboid(True, (7, 9), (0, 9), (0, 9)),
        Cuboid(True, (0, 6), (7, 9), (0, 9)),
        Cuboid(True, (0, 6), (0, 6), (7, 9)),
    ]
