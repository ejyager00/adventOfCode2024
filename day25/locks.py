import sys

def parse_input(filename: str) -> tuple[list[list[int]], list[list[int]]]:
    with open(filename) as f:
        locks = []
        keys = []
        for schematic in f.read().strip().split("\n\n"):
            schem = [0,0,0,0,0]
            for row in schematic.split('\n')[1:-1]:
                for i, x in enumerate(row):
                    schem[i]+= 1 if x=='#' else 0
            if schematic[0]=='#':
                locks.append(schem)
            else:
                keys.append(schem)
    return (locks, keys)

def count_possible_pairs(locks: list[list[int]], keys: list[list[int]]) -> int:
    total = 0
    for lock in locks:
        for key in keys:
            total += not any([l+k>5 for l, k in zip(lock, key)])
    return total


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    try:
        locks, keys = parse_input(sys.argv[1])
        print(f"The number of possible key/lock pairs is {count_possible_pairs(locks, keys)}")
    except FileNotFoundError: 
        print(f"Error: Could not find input file '{sys.argv[1]}'")