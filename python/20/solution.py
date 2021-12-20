import sys
from functools import reduce
from itertools import product


def read_input():
    enhancement = [c == "#" for c in sys.stdin.readline().strip()]
    lines = [line.strip() for line in sys.stdin.readlines() if line.strip()]
    image = [[c == "#" for c in line] for line in lines]

    return (enhancement, image)


def iter_pixels(image, x, y, default):
    for i, j in product(range(-1, 2), range(-1, 2)):
        nx, ny = x + j, y + i
        if nx < 0 or ny < 0 or nx >= len(image) or ny >= len(image[nx]):
            yield default
        else:
            yield image[ny][nx]


def enhance(enhancement, image, n):
    enhanced_image = []
    for y in range(-1, len(image) + 1):
        enhanced_image.append([])
        for x in range(-1, len(image[0]) + 1):
            pixels = list(iter_pixels(image, x, y, enhancement[0] and n % 2 != 0))
            enhanced_pixel = reduce(lambda a, b: a << 1 | b, pixels, 0)
            enhanced_image[-1].append(enhancement[enhanced_pixel])
    return enhanced_image


def count_lit_pixels(image):
    return len(
        [0 for x, y in product(range(len(image)), range(len(image[0]))) if image[y][x]]
    )


def part_1(enhancement, image):
    for n in range(2):
        image = enhance(enhancement, image, n)

    return count_lit_pixels(image)


def part_2(enhancement, image):
    for n in range(50):
        image = enhance(enhancement, image, n)

    return count_lit_pixels(image)


if __name__ == "__main__":
    data = read_input()
    print(part_1(*data))
    print(part_2(*data))
