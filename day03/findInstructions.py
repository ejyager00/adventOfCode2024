import re
import sys

MUL_INSTRUCT_REGEX = re.compile(r"mul\([0-9]{1,3},[0-9]{1,3}\)")
NUM_REGEX = re.compile(r"[0-9]{1,3}")
CONDITIONALS_REGEX = re.compile(r"(do\(\))|(don't\(\))")

def parse_input(filename: str) -> str:
    with open(filename) as f:
        return "\n".join([line.strip() for line in f])

def get_mul_instructions(memory: str) -> list[re.Match]:
    return MUL_INSTRUCT_REGEX.finditer(memory)

def get_product(mul_instruction: str) -> int:
    x, y = NUM_REGEX.findall(mul_instruction)
    return int(x)*int(y)

def instruct_sum_product(mul_instructions: list[re.Match]) -> int:
    return sum([get_product(match[0]) for match in mul_instructions])

def conditional_sum_product(memory: str) -> int:
    memory = "do()" + memory
    total = 0
    sections = CONDITIONALS_REGEX.split(memory)
    should_sum = True
    
    for section in sections:
        if not section:
            continue
        if section == "do()":
            should_sum = True
        elif section == "don't()":
            should_sum = False
        elif should_sum:
            total += sum(get_product(match[0]) for match in MUL_INSTRUCT_REGEX.finditer(section))
    
    return total
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python checkReports.py <input_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    
    try:
        mem_dump = parse_input(input_file)
        print(f"The sum of the products is {instruct_sum_product(get_mul_instructions(mem_dump))}.")
        print(f"The sum of the products using conditionals is {conditional_sum_product(mem_dump)}.")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")

