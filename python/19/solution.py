import sys
from itertools import permutations, product
from typing import List, Tuple
import numpy as np


Coord = Tuple[int, int, int]

x_rot = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
y_rot = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
z_rot = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

rotations = []
for x in range(4):
    for y in range(4):
        rotations.append(
            np.linalg.matrix_power(x_rot, x) @ np.linalg.matrix_power(y_rot, y)
        )
    for z in (1, 3):
        rotations.append(
            np.linalg.matrix_power(x_rot, x) @ np.linalg.matrix_power(z_rot, z)
        )


def parse_block(block):
    lines = block.split("\n")
    scanner_num = int(lines[0].split()[-2])
    points = []
    for line in lines[1:]:
        if not line.strip():
            continue
        x, y, z = line.split(",")
        x, y, z = int(x), int(y), int(z)
        points.append(Point(x, y, z))

    return points


def parse_line(line):
    return line


def read_input() -> List["Scanner"]:
    blocks = [
        parse_block(block) for block in sys.stdin.read().split("\n\n") if block.strip()
    ]
    return [Scanner(i, block) for i, block in enumerate(blocks)]


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def rotate(self, rotation):
        return (self.x, self.y, self.z) @ rotation

    def __matmul__(self, other):
        return Point(*list((self.x, self.y, self.z) @ other))

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z})"

    def __eq__(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


class Scanner:
    def __init__(self, scanner_id, points: List[Point]):
        self.scanner_id = scanner_id
        self.points = points

    def rotated_points(self, rotation):
        for point in self.points:
            yield point @ rotation

    def __repr__(self):
        return f"Scanner({self.scanner_id})"


def find_overlap(scanner1, scanner2, rotation):
    points2 = set(scanner2.rotated_points(rotation))
    for rotation in rotations:
        points1 = list(scanner1.rotated_points(rotation))

        diffs = (p2 - p1 for p1, p2 in product(points1, points2))
        for diff in diffs:
            if len([p1 for p1 in points1 if p1 + diff in points2]) >= 12:
                return (diff, rotation)

    return None, None


def find_scanner_offsets(scanners):
    found = {
        scanners[0]: (
            Point(0, 0, 0),
            rotations[0],
        ),
    }

    while len(found) != len(scanners):
        for scanner1 in scanners:
            if scanner1 in found:
                continue

            for scanner2, (offset2, rotation2) in found.items():
                offset1, rotation1 = find_overlap(scanner1, scanner2, rotation2)
                if offset1 is not None and rotation1 is not None:
                    found[scanner1] = (offset1 + offset2, rotation1)
                    break

    return list(found.items())


def solve(scanners: List[Scanner]):
    offsets = find_scanner_offsets(scanners)

    points = set()
    for scanner, (offset, rotation) in offsets:
        for point in scanner.rotated_points(rotation):
            points.add(point + offset)

    print(len(points))

    acc = 0
    for a, b in permutations([offset for _, (offset, _) in offsets], 2):
        x, y, z = a - b
        acc = max(acc, abs(x) + abs(y) + abs(z))
    print(acc)


def part_2(data):
    pass


if __name__ == "__main__":
    data = read_input()
    solve(data)
