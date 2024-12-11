import sys
from functools import lru_cache, reduce

def parse_input(filename: str) -> tuple[int]:
    with open(filename) as f:
        return tuple([int(x) for x in f.read().split(' ')])

def split_even_digits(stone_str: str) -> tuple[int]:
    digits = len(stone_str)
    return (int(stone_str[:digits//2]), int(stone_str[digits//2:]))

def transform_stone(stone: int) -> tuple[int]:
    stone_str = str(stone)
    return split_even_digits(stone_str) if len(stone_str) % 2 == 0 else (stone * 2024,)

def apply_stone_rule(stone: int) -> tuple[int]:
    return (1,) if stone == 0 else transform_stone(stone)

@lru_cache(maxsize=None)
def num_stones_after_blinks(stones: tuple[int, ...], blinks: int = 1) -> int:
    if blinks == 0:
        return len(stones)
    
    count_single = lambda stone: num_stones_after_blinks(apply_stone_rule(stone), blinks - 1)
    
    return reduce(lambda acc, stone: acc + count_single(stone), stones, 0) if len(stones) > 1 else count_single(stones[0])

def main(stones: tuple[int, ...]) -> None:
    print(f"Stones after 25 blinks: {num_stones_after_blinks(stones, blinks=25)}")
    print(f"Stones after 75 blinks: {num_stones_after_blinks(stones, blinks=75)}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python checkReports.py <input_file>")
        sys.exit(1)

    try:
        stones = parse_input(sys.argv[1])
        main(stones)
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")