import sys
from typing import List, Optional, Tuple


def extract_vars(data: List[str]) -> List[Tuple[int, int, int]]:
    vars = []
    for offset in range(14):
        a = int(data[offset * 18 + 4].strip().split(" ")[-1])
        b = int(data[offset * 18 + 5].strip().split(" ")[-1])
        c = int(data[offset * 18 + 15].strip().split(" ")[-1])
        vars.append((a, b, c))
    return vars


def solve(
    vars: List[Tuple[int, int, int]],
    n: List[int] = None,
    z: int = 0,
    reverse: bool = False,
) -> Optional[List[int]]:
    if n is None:
        n = []
    if len(n) == 14:
        return n if z == 0 else None

    a, b, c = vars[len(n)]

    if a == 26:
        m = (z % 26) + b
        if not (1 <= m <= 9):
            return
        return solve(vars, n + [m], z // 26, reverse)

    for m in range(1, 10) if reverse else range(9, 0, -1):
        r = solve(vars, n + [m], z * 26 + m + c, reverse)
        if r:
            return r


def part_1(data: List[str]) -> int:
    vars = extract_vars(data)
    r = solve(vars)

    return int("".join(str(c) for c in r)) if r else 0


def part_2(data: List[str]) -> int:
    vars = extract_vars(data)
    r = solve(vars, reverse=True)

    return int("".join(str(c) for c in r)) if r else 0


if __name__ == "__main__":
    data = sys.stdin.readlines()
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
