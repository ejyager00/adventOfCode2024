import sys

# {(stone_label, blinks): stone_count}
stone_cache = {(0, 1): 1}

def parse_input(filename: str) -> list[list[int]]:
    with open(filename) as f:
        return [int(x) for x in f.read().split(' ')]

def apply_rule(stone: int) -> list[int]:
    if stone==0:
        return [1]
    stone_string = str(stone)
    digits = len(stone_string)
    if digits%2==0:
        return [int(stone_string[:digits//2]), int(stone_string[digits//2:])]
    return [stone*2024]

def blink(stones: list[int], blinks: int=1) -> int:
    if blinks==0:
        return len(stones)
    if len(stones) > 1:
        return sum([blink([s], blinks=blinks) for s in stones])
    stone = stones[0]
    key = (stone, blinks)
    if key not in stone_cache:
        stone_cache[key] = blink(apply_rule(stone), blinks=blinks-1)
    return stone_cache[key]
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python checkReports.py <input_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]

    try:
        stone_list = parse_input(input_file)
        print(f"Stones after 25 blinks: {blink(stone_list, blinks=25)}")
        print(f"Stones after 75 blinks: {blink(stone_list, blinks=75)}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")