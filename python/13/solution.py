import sys


def read_input():
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    coords = set()
    folds = []

    for line in lines:
        if line.startswith("fold along"):
            a, b = line[11:].split("=")
            folds.append((a, int(b)))
        else:
            a, b = line.split(",")
            coords.add((int(a), int(b)))

    return (coords, folds)


def fold(coords, axis, n):
    new_coords = set()

    for x, y in coords:
        if axis == "x" and x > n:
            new_coords.add((2 * n - x, y))
        elif axis == "y" and y > n:
            new_coords.add((x, 2 * n - y))
        else:
            new_coords.add((x, y))

    return new_coords


def print_coords(coords):
    max_x = max(x for x, _ in coords)
    max_y = max(y for _, y in coords)

    for j in range(max_y + 1):
        print()
        for i in range(max_x + 1):
            print("█" if (i, j) in coords else " ", end="")
    print()


def part_1(coords, folds):
    new_coords = fold(coords, *(folds[0]))
    return len(new_coords)


def part_2(coords, folds):
    for f in folds:
        coords = fold(coords, *f)
    print_coords(coords)


data = read_input()
print(part_1(*data))
part_2(*data)
