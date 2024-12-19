import sys
from functools import lru_cache, reduce

def parse_input(filename: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    with open(filename) as f:
        towels, displays = f.read().split("\n\n")
        return (tuple(towels.split(", ")), tuple(displays.split("\n")))

@lru_cache(maxsize=None)
def display_is_possible(towels: tuple[str, ...], display: str) -> bool:
    if len(display)==0 or display in towels:
        return True

    for towel in towels:
        if display[:len(towel)]==towel and display_is_possible(towels, display[len(towel):]):
            return True

    return False

def possible_designs(towels: tuple[str, ...], displays: tuple[str, ...]) -> int:
    return sum([display_is_possible(towels, display) for display in displays])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python checkReports.py <input_file>")
        sys.exit(1)

    try:
        towels, displays = parse_input(sys.argv[1])
        print(f"The number of possible designs is {possible_designs(towels, displays)}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{sys.argv[1]}'")