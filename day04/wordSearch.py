import sys

def parse_input(filename: str) -> str:
    with open(filename) as f:
        return [line.strip().upper() for line in f]

def count_matches(puzzle: list[str], word: str) -> int:
    word = word.upper()
    h = len(puzzle)
    w = len(puzzle[0])
    l = len(word)
    matches = 0
    for i in range(h):
        for j in range(w):
            if puzzle[i][j] == word[0]:
                # forward horizontal
                if j + l <= w and puzzle[i][j : j+l] == word:
                    matches += 1
                # backward horizontal
                if j + 1 - l >= 0 and puzzle[i][j+1-l: j+1] == word[::-1]:
                    matches += 1
                # forward vertical
                if i + l <= h and "".join([puzzle[k][j] for k in range(i, i+l)]) == word:
                    matches += 1
                # backward vertical
                if i + 1 - l >= 0 and "".join([puzzle[k][j] for k in range(i + 1 - l, i+1)]) == word[::-1]:
                    matches += 1
                # north east
                if j + l <= w and i + 1 - l >= 0 and "".join([puzzle[i-d][j+d] for d in range(l)]) == word:
                    matches += 1
                # south east
                if j + l <= w and i + l <= h and "".join([puzzle[i+d][j+d] for d in range(l)]) == word:
                    matches += 1
                # north west
                if j + 1 - l >= 0 and i + 1 - l >= 0 and "".join([puzzle[i-d][j-d] for d in range(l)]) == word:
                    matches += 1
                # south west
                if j + 1 - l >= 0 and i + l <= h and "".join([puzzle[i+d][j-d] for d in range(l)]) == word:
                    matches += 1
    return matches

def count_x_matches(puzzle: list[str], word: str) -> int:
    matches = 0
    word = word.upper()[:3]
    h = len(puzzle)
    w = len(puzzle[0])
    for i in range(1,h-1):
        for j in range(1,w-1):
            if puzzle[i][j]==word[1]:
                if puzzle[i-1][j-1]==word[0] and puzzle[i+1][j+1]==word[2]:
                    if puzzle[i-1][j+1]==word[0] and puzzle[i+1][j-1]==word[2]:
                        matches += 1
                    if puzzle[i+1][j-1]==word[0] and puzzle[i-1][j+1]==word[2]:
                        matches += 1
                if puzzle[i+1][j+1]==word[0] and puzzle[i-1][j-1]==word[2]:
                    if puzzle[i-1][j+1]==word[0] and puzzle[i+1][j-1]==word[2]:
                        matches += 1
                    if puzzle[i+1][j-1]==word[0] and puzzle[i-1][j+1]==word[2]:
                        matches += 1
    return matches

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python checkReports.py <input_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    
    try:
        puzzle = parse_input(input_file)
        print(f"Number of XMASs: {count_matches(puzzle, 'XMAS')}")
        print(f"Number of X-MASs: {count_x_matches(puzzle, 'MAS')}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")
