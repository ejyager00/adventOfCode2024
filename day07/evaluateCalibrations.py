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

def is_viable(eq: CalibrationEquation, concat: bool) -> bool:
    if len(eq.operands) == 1:
        return eq.result == eq.operands[0]
    addition = CalibrationEquation(eq.result, [eq.operands[0]+eq.operands[1]]+eq.operands[2:])
    multiplication = CalibrationEquation(eq.result, [eq.operands[0]*eq.operands[1]]+eq.operands[2:])
    concatenation = None
    if concat:
        concatenation = CalibrationEquation(eq.result, [int(str(eq.operands[0])+str(eq.operands[1]))] + eq.operands[2:])
    return is_viable(addition, concat) or is_viable(multiplication, concat) or (concat and is_viable(concatenation, concat))

def sum_results(equations: list[CalibrationEquation], concat: bool = False) -> int:
    total = 0
    for eq in equations:
        if is_viable(eq, concat):
            total += eq.result
    return total

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python checkReports.py <input_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]

    try:
        equations = parse_input(input_file)
        print(f"Sum of valid test values excluding concatenation is {sum_results(equations)}")
        print(f"Sum of valid test values including concatenation is {sum_results(equations, True)}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")