import sys

class Gate:
    def __init__(self, string):
        in1, op, in2, _, self.out = string.split(" ")
        self.input = tuple(sorted([in1,in2]))
        match op:
            case 'AND':
                self.operate = lambda a, b : a and b
            case 'OR':
                self.operate = lambda a, b : a or b
            case 'XOR':
                self.operate = lambda a, b : a != b
    
    def __str__(self):
        return f"{self.input[0]}, {self.input[1]} -> {self.out}"

def parse_input(filename: str) -> tuple[dict[str, int], list[Gate], int]:
    with open(filename) as f:
        start_str, gate_str = f.read().strip().split("\n\n")
        gates = [Gate(g) for g in gate_str.split("\n")]
        starts = {x[:3]: bool(int(x[-1])) for x in start_str.split("\n")}
        max_z = 0
        for g in gates:
            if g.out[0]=='z' and int(g.out[1:])>max_z:
                max_z = int(g.out[1:])
        return (starts, gates, max_z)

def get_monitor_output(vals: dict[str, int], gates: list[Gate], max_z: int) -> int:
    result = [None]*(max_z+1)
    while None in result:
        for i, gate in enumerate(gates):
            if gate.input[0] in vals and gate.input[1] in vals:
                vals[gate.out] = gate.operate(vals[gate.input[0]], vals[gate.input[1]])
                if gate.out[0]=='z':
                    result[int(gate.out[1:])] = vals[gate.out]
                del gates[i]
    return sum([2**i if x else 0 for i, x in enumerate(result)])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    try:
        starts, gates, max_z = parse_input(sys.argv[1])
        print(f"The monitor is outputting {get_monitor_output(starts, gates, max_z)}")
    except FileNotFoundError: 
        print(f"Error: Could not find input file '{sys.argv[1]}'")