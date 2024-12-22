import sys

def parse_input(filename: str) -> list[str]:
    with open(filename) as f:
        return [int(x) for x in f.read().strip().split("\n")]

mix = lambda a, b : a^b
prune = lambda a : a % 16777216

def monkey_hash(x: int) -> int:
    x = prune(mix(x*64,x))
    x = prune(mix(x//32,x))
    x = prune(mix(x*2048,x))
    return x

def hash_times(x: int, times: int) -> int:
    for i in range(times):
        x = monkey_hash(x)
    return x

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    try:
        prices = parse_input(sys.argv[1])
        print(f"The sum of the 2000th prices is {sum([hash_times(x, 2000) for x in prices])}")
        
    except FileNotFoundError:
        print(f"Error: Could not find input file '{sys.argv[1]}'")