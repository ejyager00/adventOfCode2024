import sys
from collections import Counter

NUMPAD = {key: (i % 3, i // 3) for i, key in enumerate("789456123 0A")}
DIRPAD = {key: (i % 3, i // 3) for i, key in enumerate(" ^A<v>")}

def parse_input(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().strip().split("\n")

def steps(G: dict[complex, str], s: str, i=1):
    px, py = G["A"]
    bx, by = G[" "]
    res = Counter()
    for c in s:
        npx, npy = G[c]
        f = npx == bx and py == by or npy == by and px == bx
        res[(npx - px, npy - py, f)] += i
        px, py = npx, npy
    return res


def get_min_complexity(codes: list[str], intermediaries: int = 2):
    r = 0
    for code in codes:
        res = steps(NUMPAD, code)
        for _ in range(intermediaries + 1):
            res = sum((steps(DIRPAD, ("<" * -x + "v" * y + "^" * -y + ">" * x)[:: -1 if f else 1] + "A", res[(x, y, f)]) for x, y, f in res), Counter())
        r += res.total() * int(code[:3])
    return r

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    try:
        codes = parse_input(sys.argv[1])
        print(f"The sum of the complexities is {get_min_complexity(codes)}")
        print(f"The sum of the complexities for the second person is {get_min_complexity(codes, 25)}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{sys.argv[1]}'")