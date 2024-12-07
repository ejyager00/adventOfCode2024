import sys
from dataclasses import dataclass

@dataclass
class CalibrationEquation:
    result: int
    operands: list[int]

def parse_input(filename: str) -> list[CalibrationEquation]:
    equations = []
    with open(filename) as f:
        for line in f:
            r, o = line.strip().split(": ")
            r = int(r)
            o = [int(x) for x in o.split(' ')]
            equations.append(CalibrationEquation(r, o))
    return equations

def is_viable(eq: CalibrationEquation) -> bool:
    if len(eq.operands) == 1:
        return eq.result == eq.operands[0]
    if sum(eq.operands) > eq.result:
        return False
    addition = CalibrationEquation(eq.result, [eq.operands[0]+eq.operands[1]]+eq.operands[2:])
    multiplication = CalibrationEquation(eq.result, [eq.operands[0]*eq.operands[1]]+eq.operands[2:])
    return is_viable(addition) or is_viable(multiplication)

def sum_results(equations: list[CalibrationEquation]) -> int:
    total = 0
    for eq in equations:
        print(eq)
        if is_viable(eq):
            print("yes")
            total += eq.result
        else:
            print("no")
    return total

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python checkReports.py <input_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]

    try:
        equations = parse_input(input_file)
        print(f"Sum of valid test values is {sum_results(equations)}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")