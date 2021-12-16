import sys
from functools import reduce
from typing import List, Tuple


class Package:
    version: int

    def get_version(self) -> int:
        raise NotImplementedError()

    def evaluate(self) -> int:
        raise NotImplementedError()


class Literal(Package):
    def __init__(self, version: int, value: int):
        self.version = version
        self.value = value

    def __repr__(self) -> str:
        return f"Literal(v{self.version}, {self.value})"

    def get_version(self) -> int:
        return self.version

    def evaluate(self) -> int:
        return self.value


class Operator(Package):
    def __init__(self, version: int, type_: int, children: List[Package]):
        self.version = version
        self.type_ = type_
        self.children = children

    def __repr__(self) -> str:
        return f"Operator(v{self.version}, {self.type_}, [{', '.join(str(child) for child in self.children)}])"

    def get_version(self) -> int:
        return self.version + sum(
            [child.get_version() for child in self.children]
        )

    def evaluate(self) -> int:
        children = [child.evaluate() for child in self.children]

        match self.type_:            
            case 0:
                return sum(children)
            case 1:
                return reduce(lambda a, b: a * b, children, 1)
            case 2:
                return min(children)
            case 3:
                return max(children)
            case 5:
                return int(children[0] > children[1])
            case 6:
                return int(children[0] < children[1])
            case 7:
                return int(children[0] == children[1])
            case _:
                return 0

def read_input() -> List[bool]:
    line = [line.strip() for line in sys.stdin.readlines() if line.strip()][0]
    result: List[bool] = []
    for n in line:
        result += [n == '1' for n in bin(int(n, 16))[2:].zfill(4)]
    return result

def to_int(bits: List[bool]) -> int:
    return reduce(lambda acc, b: (acc << 1) | b,  bits, 0)

def read_varint(data: List[bool]) -> Tuple[int, List[bool]]:
    acc = 0
    offset = 0

    while True:
        acc = (acc << 4) + to_int(data[offset + 1 : offset + 5])
        cont = data[offset]
        offset += 5
        if not cont:
            break

    return acc, data[offset: ]


def read_int(data: List[bool], length: int) -> Tuple[int, List[bool]]:
    return to_int(data[:length]), data[length:]


def decode(data: List[bool]) -> Tuple[Package, List[bool]]:
    version, data = read_int(data, 3)
    type_, data = read_int(data, 3)
    
    if type_ == 4:
        value, data = read_varint(data)
        return Literal(version, value), data

    type_id, data = read_int(data, 1)

    children: List[Package] = []
    if type_id == 0:
        sub_length, data = read_int(data, 15)
        sub_data, data = data[:sub_length], data[sub_length:]
        
        while len(sub_data):
            child, sub_data = decode(sub_data)
            children.append(child)
    else:
        n, data = read_int(data, 11)
        for _ in range(n):
            child, data = decode(data)
            children.append(child)

    return Operator(version, type_, children), data

def part_1(data: List[bool]) -> int:
    package, _ = decode(data)

    return package.get_version()


def part_2(data: List[bool]) -> int:
    package, _ = decode(data)

    return package.evaluate()


data = read_input()
print(part_1(data))
print(part_2(data))
