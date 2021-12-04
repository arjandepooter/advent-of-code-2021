import sys


def parse_card(block):
    acc = []
    for line in block.strip().split("\n"):
        for number in line.strip().split():
            acc.append(int(number))
    return acc


def read_input():
    blocks = sys.stdin.read().split("\n\n")

    numbers = [int(n) for n in blocks[0].split(",")]
    cards = [parse_card(block) for block in blocks[1:] if block]

    return (numbers, cards)


def cols(card):
    for i in range(5):
        yield [card[i + j * 5] for j in range(5)]


def rows(card):
    for i in range(5):
        yield card[i * 5 : i * 5 + 5]


def has_won(numbers, card):
    return any(all(n in numbers for n in col) for col in cols(card)) or any(
        all(n in numbers for n in row) for row in rows(card)
    )


def get_score(numbers, card):
    empty_spaces = sum(n for n in card if n not in numbers)
    last_drawn = numbers[-1]
    return empty_spaces * last_drawn


def part_1(numbers, cards):
    drawn = 0
    while True:
        for card in cards:
            if has_won(numbers[:drawn], card):
                return get_score(numbers[:drawn], card)
        drawn += 1


def part_2(numbers, cards):
    drawn = 0
    while len(cards) > 1:
        for card in cards:
            if has_won(numbers[:drawn], card):
                cards.remove(card)
        drawn += 1

    return get_score(numbers[: drawn - 1], cards[0])


data = read_input()
print(part_1(*data))
print(part_2(*data))
