import sys
from functools import lru_cache

def parse_input(filename: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
    with open(filename) as f:
        towels, displays = f.read().split("\n\n")
        return (tuple(towels.split(", ")), tuple(displays.split("\n")))

@lru_cache(maxsize=None)
def display_arrangements(towels: tuple[str, ...], display: str) -> int:
    if display=="":
        return 1
    return sum([display_arrangements(towels, display[len(towel):]) for towel in towels if display[:len(towel)]==towel])

def possible_designs(towels: tuple[str, ...], displays: tuple[str, ...]) -> int:
    return sum([display_arrangements(towels, display)>0 for display in displays])

def total_unique_arrangments(towels: tuple[str, ...], displays: tuple[str, ...]) -> int:
    return sum([display_arrangements(towels, display) for display in displays])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python toweldisplay.py <input_file>")
        sys.exit(1)

    try:
        towels, displays = parse_input(sys.argv[1])
        print(f"The number of possible designs is {possible_designs(towels, displays)}")
        print(f"The number of unique design arrangements is {total_unique_arrangments(towels, displays)}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{sys.argv[1]}'")