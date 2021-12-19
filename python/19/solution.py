import sys
from collections import Counter
from itertools import permutations, product
from typing import Dict, List, Optional, Tuple

import numpy as np


def parse_block(block):
    lines = block.split("\n")

    points = []
    for line in lines[1:]:
        if not line.strip():
            continue
        x, y, z = [int(n) for n in line.split(",")]
        points.append(Point(x, y, z))

    return points


def read_input() -> List["Scanner"]:
    blocks = [
        parse_block(block) for block in sys.stdin.read().split("\n\n") if block.strip()
    ]
    return [Scanner(i, block) for i, block in enumerate(blocks)]


x_rot = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
y_rot = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
z_rot = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

rotations = [
    np.linalg.matrix_power(x_rot, x) @ np.linalg.matrix_power(y_rot, y)
    for x, y in product(range(4), range(4))
] + [
    np.linalg.matrix_power(x_rot, x) @ np.linalg.matrix_power(z_rot, z)
    for x, z in product(range(4), (1, 3))
]


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __matmul__(self, other) -> "Point":
        return Point(*(list(self) @ other))

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
        self.rotations = [
            [point @ rotation for point in points] for rotation in rotations
        ]

    def rotated_points(self, rotation: int) -> List[Point]:
        return self.rotations[rotation]

    def __repr__(self):
        return f"Scanner({self.scanner_id})"


def find_overlap(
    scanner1: Scanner, scanner2: Scanner, rotation: int
) -> Optional[Tuple[Point, int]]:
    points2 = scanner2.rotated_points(rotation)

    for rotation in range(len(rotations)):
        points1 = scanner1.rotated_points(rotation)
        counts = Counter((p2 - p1 for p1, p2 in product(points1, points2)))
        diff, max_count = counts.most_common(1)[0]
        if max_count >= 12:
            return (diff, rotation)


def find_scanner_offsets(
    scanners: List[Scanner],
) -> List[Tuple[Scanner, Tuple[Point, int]]]:
    found: Dict[Scanner, Tuple[Point, int]] = {scanners[0]: (Point(0, 0, 0), 0)}

    while len(found) != len(scanners):
        for scanner1 in scanners:
            if scanner1 in found:
                continue

            for scanner2, (offset2, rotation2) in found.items():
                if result := find_overlap(scanner1, scanner2, rotation2):
                    offset1, rotation1 = result
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
