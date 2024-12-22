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

def hash_times(x: int, times: int) -> list[int]:
    hashes = [x]
    for i in range(times):
        hashes.append(monkey_hash(hashes[i]))
    return hashes

def get_maximum_bananas(hashes: list[list[int]]) -> int:
    prices = [[x%10 for x in y] for y in hashes]
    price_changes = [[x-y[i] for i, x in enumerate(y[1:])] for y in prices]
    sequence_scores = {}
    maximum = (None, -1)
    for i, monkey in enumerate(prices):
        seen_this_monkey = set()
        for j in range(3,len(price_changes[i])):
            sequence = tuple(price_changes[i][j-3:j+1])
            if sequence in seen_this_monkey:
                continue
            seen_this_monkey.add(sequence)
            sequence_scores[sequence] = sequence_scores.get(sequence, 0) + monkey[j+1]
            if sequence_scores[sequence]>maximum[1]:
                maximum = (sequence, sequence_scores[sequence])
    return maximum[1]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    try:
        prices = parse_input(sys.argv[1])
        hashes = [hash_times(x, 2000) for x in prices]
        print(f"The sum of the 2000th prices is {sum([x[-1] for x in hashes])}")
        print(f"The most bananas we can get is {get_maximum_bananas(hashes)}")
    except FileNotFoundError: 
        print(f"Error: Could not find input file '{sys.argv[1]}'")