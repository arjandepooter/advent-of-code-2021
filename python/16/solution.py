import sys
from functools import reduce


class Literal:
    def __init__(self, version, value):
        self.version = version
        self.value = value

    def __repr__(self) -> str:
        return f"Literal(v{self.version}, {self.value})"

    def get_version(self):
        return self.version

    def evaluate(self):
        return self.value


class Operator(Literal):
    def __init__(self, version, type_, children):
        self.version = version
        self.type_ = type_
        self.children = children

    def __repr__(self) -> str:
        return f"Operator(v{self.version}, {self.type_}, [{', '.join(str(child) for child in self.children)}])"

    def get_version(self):
        return self.version + sum(
            [child.get_version() for child in self.children if child]
        )

    def evaluate(self):
        children = [child.evaluate() for child in self.children]

        if self.type_ == 0:
            return sum(children)
        if self.type_ == 1:
            return reduce(lambda a, b: a * b, children, 1)
        if self.type_ == 2:
            return min(children)
        if self.type_ == 3:
            return max(children)
        if self.type_ == 5:
            return int(children[0] > children[1])
        if self.type_ == 6:
            return int(children[0] < children[1])
        if self.type_ == 7:
            return int(children[0] == children[1])


def read_input():
    line = [line.strip() for line in sys.stdin.readlines() if line.strip()][0]
    result = []
    for n in line:
        b = int(n, 16)
        result += list((bin(b)[2:]).zfill(4))
    return result


def to_int(b):
    return int("".join(b), 2)


def read_literal(data):
    acc = []
    s = 0

    while True:
        a = data[s + 1 : s + 5]
        acc += a
        if len(a) == 0 or data[s] == "0":
            break
        s += 5

    return to_int(acc), data[s + 5 :]


def read_int(data, length):
    version = data[:length]

    return to_int(version), data[length:]


def decode(data):
    if len(data) < 6:
        return None, []

    version, data = read_int(data, 3)
    type_, data = read_int(data, 3)

    if type_ == 4:
        value, data = read_literal(data)
        return Literal(version, value), data
    else:
        type_id, data = read_int(data, 1)

        if type_id == 0:
            sub_length, data = read_int(data, 15)
            sub_data = data[:sub_length]
            data = data[sub_length:]
            children = []
            while len(sub_data):
                child, sub_data = decode(sub_data)
                children.append(child)
            return Operator(version, type_, children), data
        elif type_id == 1:
            n, data = read_int(data, 11)
            children = []
            for _ in range(n):
                child, data = decode(data)
                children.append(child)
            return Operator(version, type_, children), data


def part_1(data):
    package, _ = decode(data)

    return package.get_version()


def part_2(data):
    package, _ = decode(data)

    return package.evaluate()


data = read_input()
print(part_1(data))
print(part_2(data))
