import sys
import operator
from collections import namedtuple
from collections.abc import Callable

class Gate:

    ops = {
        "AND": operator.and_,
        "XOR": operator.xor,
        "OR": operator.or_,
    }

    def __init__(self, string):
        in1, self.op, in2, _, self.out = string.split(" ")
        self.input = tuple(sorted([in1,in2]))
        self.operate = lambda a, b : Gate.ops[self.op](a,b)
    
    def __str__(self):
        return f"{self.input[0]} {self.op} {self.input[1]} -> {self.out}"

Adder = namedtuple("Adder",["carry","partsum","generate","propagate"])

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
def get_gate_output(gates: list[Gate], gate: str) -> str:
    for g in gates:
        if str(g)[:len(gate)]==gate:
            return g.out
    gate = gate[-3:] + gate[3:-3] + gate[:3]
    for g in gates:
        if str(g)[:len(gate)]==gate:
            return g.out
    return None
    
def get_gate_inputs(gates: list[Gate], result: str) -> Gate:
    for g in gates:
        if g.out==result:
            return g
    return None

def missing_operand(op1: str, op2: str, ops: tuple[str, str]) -> tuple[bool, bool]:
    res1 = op1 in ops
    res2 = op2 in ops
    return (res1, res2)

def find_carry_gate(gates: list[Gate], prop: str, gen: str) -> tuple[Gate, str]:
    for g in gates:
        if (prop in g.input or gen in g.input) and g.op == "OR":
            return (g, prop if gen in g.input else gen)
    return None

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

def get_mismatched_outputs1(gates: list[Gate], max_z: int) -> set[str]:
    output = lambda gate : get_gate_output(gates, gate)
    get_gate = lambda gate : get_gate_inputs(gates, gate)
    get_carry = lambda prop, gen : find_carry_gate(gates, prop, gen)
    errors = set()
    # least significant bit
    outbit0 = output("x00 XOR y00")
    if (outbit0!="z00"):
        errors.update(("z00",outbit0))
    adders = [Adder(output("x00 AND y00"),None,None,None)]
    # other bits
    for i in range(1,max_z):
        digit = str(i).zfill(2)
        partsum = output(f"x{digit} XOR y{digit}")
        outgate = get_gate(f"z{digit}")
        prop_in = list(outgate.input)
        outgate_inputs = missing_operand(partsum, adders[i-1].carry,  outgate.input)
        if (not any(outgate_inputs)): # z output is in wrong spot
            actual = output(f"{partsum} XOR {adders[i-1].carry}")
            errors.update((f"z{digit}",actual))
            other = get_gate(actual)
            prop_in = other.input
        elif (not outgate_inputs[0]): # partsum is in wrong spot
            actual = outgate.input[(outgate.input.index(adders[i-1].carry)+1)%2]
            errors.update((partsum,actual))
            partsum = actual
        elif (not outgate_inputs[1]): # previous carry is in wrong spot
            actual = outgate.input[(outgate.input.index(partsum)+1)%2]
            errors.update((adders[i-1].carry,actual))
        generate = output(f"x{digit} AND y{digit}")
        propagate = output(f"{prop_in[0]} AND {prop_in[1]}")
        carry = output(f"{generate} OR {propagate}")
        if carry == None: # propagate or generate is wrong
            carry_gate, misplaced = get_carry(propagate, generate)
            carry = carry_gate.out
            other = get_gate(misplaced)
            if misplaced == generate:
                generate = carry_gate.input[(carry_gate.input.index(propagate)+1)%2]
            else:
                propagate = carry_gate.input[(carry_gate.input.index(generate)+1)%2]
        adders.append(Adder(carry,partsum,generate,propagate))
    return errors

def isDirect(gate: Gate) -> bool:
    return gate.input[0][0]=='x' or gate.input[1][0]=='x'

def isOutput(gate: Gate) -> bool:
    return gate.out[0]=='z'

def isGate(type: str) -> Callable[[], bool]:
    return lambda gate : gate.op == type

def hasOutput(output: str) -> Callable[[], bool]:
    return lambda gate : gate.out == output

def hasInput(input: str) -> Callable[[], bool]:
    return lambda gate : gate.input[0] == input or gate.input[1] == input

def get_mismatched_outputs2(gates: list[Gate], max_z: int) -> set[str]:
    flags = set()
    partsums = filter(isDirect, filter(isGate('XOR'), gates))
    for gate in partsums:
        if "x00" in gate.input:
            if (gate.out != "z00"):
                flags.add(gate.out)
            continue
        elif gate.out == "z00":
            flags.add(gate.out)
        if isOutput(gate):
            flags.add(gate.out)
    
    outputs = filter(isGate("XOR"), filter(lambda g : not isDirect(g), gates))
    for gate in outputs:
        if not isOutput(gate):
            flags.add(gate.out)
    
    sumGates = filter(isOutput, gates)
    for gate in sumGates:
        if gate.out == f"z{str(max_z).zfill(2)}":
            if gate.op != "OR":
                flags.add(gate.out)
            continue
        elif gate.op != "XOR":
            flags.add(gate.out)
    
    checkNext = []
    for gate in partsums:
        if gate.out in flags or gate.out == "z00":
            continue
        matches = filter(hasInput(gate.out), gates)
        if len(matches) == 0:
            checkNext.append(gate)
            flags.add(gate.out)

    for gate in checkNext:
        intendedResult = f"z{gate.input[0][1:]}"
        toCheck = filter(hasOutput(intendedResult), outputs)[0].input
        orMatch = filter(isGate("OR"), filter(lambda g: g.out in toCheck, gates))[0].out
        correctOutput = [x for x in toCheck if x != orMatch][0]
        flags.add(correctOutput)

    return flags

def get_mismatched_outputs(gates: list[Gate], max_z: int) -> tuple[str,...]:
    return tuple(sorted(list(get_mismatched_outputs1(gates, max_z).union(get_mismatched_outputs2(gates, max_z)))))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    try:
        starts, gates, max_z = parse_input(sys.argv[1])
        print(f"The monitor is outputting {get_monitor_output(starts, gates, max_z)}")
        print()
        starts, gates, max_z = parse_input(sys.argv[1])
        print(f"The mismatched outputs are {",".join(get_mismatched_outputs(gates, max_z))}")
    except FileNotFoundError: 
        print(f"Error: Could not find input file '{sys.argv[1]}'")