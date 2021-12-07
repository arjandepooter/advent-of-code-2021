import sys


def read_input():
    return [int(n) for n in sys.stdin.read().strip().split(",")]


def part_1(numbers):
    numbers.sort()
    median = numbers[len(numbers) // 2]
    return sum(abs(median - n) for n in numbers)


def part_2(numbers):
    max_n, min_n = max(numbers), min(numbers)

    fuel_costs = []
    for m in range(min_n, max_n + 1):
        fuel_cost = sum(abs(m - n) * (abs(m - n) + 1) // 2 for n in numbers)
        fuel_costs.append(fuel_cost)

    return min(fuel_costs)


data = read_input()
print(part_1(data))
print(part_2(data))
