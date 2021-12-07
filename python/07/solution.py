import sys


def read_input():
    return [int(n) for n in sys.stdin.read().strip().split(",")]


def part_1(numbers):
    median = sorted(numbers)[len(numbers) // 2]
    return sum(abs(median - n) for n in numbers)


def fuel_cost(crabs, mid):
    return sum(abs(mid - n) * (abs(mid - n) + 1) // 2 for n in crabs)


def part_2(numbers):
    average = sum(numbers) // len(numbers)
    return min(fuel_cost(numbers, average), fuel_cost(numbers, average + 1))


data = read_input()
print(part_1(data))
print(part_2(data))
