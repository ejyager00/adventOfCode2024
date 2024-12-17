import sys

class ThreeBit:
    def __init__(self, program: list[int], a: int=0, b: int=0, c: int=0):
        self.instr_point = 0
        self.output = []
        self.reg_a = a
        self.reg_b = b
        self.reg_c = c
        self.program = program

    def __str__(self) -> str:
        return f"Register A = {self.reg_a}\nRegister B = {self.reg_b}\nRegister C = {self.reg_c}\nProgram: {self.program}"

    def _get_reg_by_num(self, num: int) -> int:
        if num==4: return self.reg_a
        if num==5: return self.reg_b
        return self.reg_c

    def _op(self, instr: int, opd: int) -> int:
        jump = 2
        print(f"program {instr},{opd} has result ", end='')
        match instr:
            case 0:
                if opd==7: raise ValueError(f"{opd} is illegal operand for instruction {instr}")
                self.reg_a //= 2**(opd if opd<4 else self._get_reg_by_num(opd))
                print(f"register A = {self.reg_a}")
            case 1:
                self.reg_b ^= opd
                print(f"register B = {self.reg_b}")
            case 2:
                if opd==7: raise ValueError(f"{opd} is illegal operand for instruction {instr}")
                self.reg_b = (opd if opd<4 else self._get_reg_by_num(opd))%8
                print(f"register B = {self.reg_b}")
            case 3:
                if self.reg_a != 0:
                    self.instr_point = opd
                    jump = 0
                    print(f"jump to {self.instr_point}")
                else:
                    print("no jump")
            case 4:
                self.reg_b ^= self.reg_c
                print(f"register B = {self.reg_b}")
            case 5:
                self.output.append((opd if opd<4 else self._get_reg_by_num(opd))%8)
                print(f"output {self.output[-1]}")
            case 6:
                self.reg_b = self.reg_a // 2**(opd if opd<4 else self._get_reg_by_num(opd))
                print(f"register B = {self.reg_b}")
            case 7:
                self.reg_c = self.reg_a // 2**(opd if opd<4 else self._get_reg_by_num(opd))
                print(f"register C = {self.reg_c}")
        return jump

    def run_program(self) -> str:
        self.output = []
        while self.instr_point < len(self.program):
            inc = self._op(self.program[self.instr_point], self.program[self.instr_point+1])
            self.instr_point+=inc
        return ",".join([str(x) for x in self.output])

def parse_input(filename: str) -> ThreeBit:
    with open(filename) as f:
        data = f.read().strip()
        regs, prog = data.split("\n\n")
        a, b, c = [int(x.split(": ")[1]) for x in regs.split("\n")]
        prog = [int(x) for x in prog.split(": ")[1].split(",")]
    return ThreeBit(prog, a, b, c)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    try:
        three_bit = parse_input(sys.argv[1])
        print(f"The program outputs: {three_bit.run_program()}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{sys.argv[1]}'")