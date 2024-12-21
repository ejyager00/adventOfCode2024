import sys
"""
789
456
123
 0A

 ^A
<^>
"""
NUMPAD = {
    'A': (2,0),
    '0': (1,0),
    '1': (0,1),
    '2': (1,1),
    '3': (2,1),
    '4': (0,2),
    '5': (1,2),
    '6': (2,2),
    '7': (0,3),
    '8': (1,3),
    '9': (2,3),
}
DIRPAD = {
    'A': (2,1),
    '^': (1,1),
    '<': (0,0),
    'v': (0,1),
    '>': (0,2),
}

def parse_input(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().strip().split("\n")

def enter_code(code: str, numeric: bool = False):
    pad = NUMPAD if numeric else DIRPAD
    dist = lambda s, e: (pad[e][0]-pad[s][0], pad[e][1]-pad[s][1])
    current = 'A'
    output = ''
    for k in code:
        x, y = dist(current, k)
        output += abs(y)*('^' if y>0 else 'v')+abs(x)*('>' if x>0 else '<')+'A'
        current = k
    return output

def manual_code(code: str) -> str:
    robot1 = enter_code(code, numeric=True)
    robot2 = enter_code(robot1)
    manual = enter_code(robot2)
    print(manual)
    print(robot2)
    print(robot1)
    print(code)
    return manual

def get_complexity(code: str, sequence: str) -> int:
    return int(code[:-1])*len(sequence)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    try:
        codes = parse_input(sys.argv[1])
        print(f"{codes[0]}: {get_complexity(codes[0], manual_code(codes[0]))}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{sys.argv[1]}'")