package main

import (
	"fmt"
	"os"
	"slices"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

const OP_MAX_SHIFT = 6
const OP_BITS = 1 << OP_MAX_SHIFT

type Literal struct {
	v        int
	polarity bool
}

func ci(cond bool, v int) Literal {
	return Literal{v: v, polarity: cond}
}

func yes(v int) Literal {
	return ci(true, v)
}

func no(v int) Literal {
	return ci(false, v)
}

func (l *Literal) neg() Literal {
	return Literal{v: l.v, polarity: !l.polarity}
}

type Checkpoint struct {
	nConstraints int
	aLoc         int
	bLoc         int
	cLoc         int
	nVars        int
}

type Comment struct {
	cidx int
	text string
}

type SymbolicExecutor struct {
	// Constraints in CNF (AND of ORs); - indicates NOT
	constraints [][]Literal
	// Indices of the variables containing the lowest bit of the registers.
	// Register bits are stored in little endian.
	aLoc int
	bLoc int
	cLoc int
	// The number of variables assigned so far.
	nVars int
	// Stack of negated guard variables; e.g. if constraints should be
	// conditional on var. #24, then this would contain [-24]
	guardStack []Literal
	why        []Comment
}

func makeSymbolicExecutor(b int64, c int64) SymbolicExecutor {
	constraints := [][]Literal{}
	for i := 0; i < OP_BITS; i += 1 {
		constraints = append(
			constraints,
			[]Literal{ci((b&(1<<i)) != 0, OP_BITS+i)},
			[]Literal{ci((c&(1<<i)) != 0, 2*OP_BITS+i)},
		)
	}
	return SymbolicExecutor{
		constraints: constraints,
		aLoc:        0,
		bLoc:        OP_BITS,
		cLoc:        2 * OP_BITS,
		nVars:       3 * OP_BITS,
		guardStack:  []Literal{},
		why:         []Comment{},
	}
}

func (se *SymbolicExecutor) comment(text string) {
	se.why = append(se.why, Comment{cidx: len(se.constraints), text: text})
}

func (se *SymbolicExecutor) save() Checkpoint {
	return Checkpoint{nConstraints: len(se.constraints), aLoc: se.aLoc, bLoc: se.bLoc, cLoc: se.cLoc, nVars: se.nVars}
}

func (se *SymbolicExecutor) restoreAndRollbackClauses(cp Checkpoint) {
	se.aLoc = cp.aLoc
	se.bLoc = cp.bLoc
	se.cLoc = cp.cLoc
	se.nVars = cp.nVars
	se.constraints = slices.Delete(se.constraints, cp.nConstraints, len(se.constraints))
}

func (se *SymbolicExecutor) restore(cp Checkpoint) {
	se.aLoc = cp.aLoc
	se.bLoc = cp.bLoc
	se.cLoc = cp.cLoc
}

func (se *SymbolicExecutor) nextVar() int {
	r := se.nVars
	se.nVars += 1
	return r
}

func (se *SymbolicExecutor) nextBlock() int {
	r := se.nVars
	se.nVars += OP_BITS
	return r
}

func (se *SymbolicExecutor) addConstraint(c []Literal) {
	se.constraints = append(se.constraints, slices.Concat(se.guardStack, c))
}

// a = b
func (se *SymbolicExecutor) addEqConstraint(a int, b int) {
	se.addConstraint([]Literal{yes(a), no(b)})
	se.addConstraint([]Literal{no(a), yes(b)})
}

// a != b
func (se *SymbolicExecutor) addXorConstraint(a int, b int) {
	se.addConstraint([]Literal{yes(a), yes(b)})
	se.addConstraint([]Literal{no(a), no(b)})
}

// cond -> (a = b)
func (se *SymbolicExecutor) addCondEqConstraint(cond Literal, a int, b int) {
	se.addConstraint([]Literal{cond.neg(), yes(a), no(b)})
	se.addConstraint([]Literal{cond.neg(), no(a), yes(b)})
}

// a = bStart || (bStart + 1) || ... || (bEnd - 1)
func (se *SymbolicExecutor) addEqConstraintOrOfRange(a int, bStart int, bEnd int) {
	c1 := []Literal{no(a)}
	for b := bStart; b < bEnd; b += 1 {
		c1 = append(c1, yes(b))
		se.addConstraint([]Literal{yes(a), no(b)})
	}
	se.addConstraint(c1)
}

// a implies b, which is (!a || b)
func (se *SymbolicExecutor) addImpliesConstraint(a Literal, b Literal) {
	se.addConstraint([]Literal{a.neg(), b})
}

// a = (bStart..(bStart + bCount)) matches bValue
func (se *SymbolicExecutor) addEqConstraintMatchingBits(a int, bStart int, bCount int, bValue int) {
	c1 := []Literal{yes(a)}
	for i := 0; i < bCount; i += 1 {
		set := (bValue & (1 << i)) != 0
		se.addImpliesConstraint(yes(a), ci(set, bStart+i)) // a implies MATCH
		// MATCH implies A == !MATCH or A == (!match0 or !match1 or ...) or A
		c1 = append(c1, ci(!set, bStart+i))
	}
	se.addConstraint(c1)
}

func (se *SymbolicExecutor) executeShift(shiftSrc int) int {
	dest := se.nextBlock()
	se.comment(fmt.Sprintf("Destination of shift operand: $%d", dest))
	var shiftAmtLoc int
	switch shiftSrc {
	// Constant shift amount
	case 0, 1, 2, 3:
		se.comment(fmt.Sprintf("Shift by constant %d", shiftSrc))
		for i := 0; i < OP_BITS; i += 1 {
			if i+shiftSrc >= OP_BITS {
				se.addConstraint([]Literal{no(dest + i)})
			} else {
				// Otherwise, dest[i] == a_old[i + x]
				se.addEqConstraint(dest+i, se.aLoc+i+shiftSrc)
			}
		}
		return dest
	case 4:
		shiftAmtLoc = se.aLoc
	case 5:
		shiftAmtLoc = se.bLoc
	case 6:
		shiftAmtLoc = se.cLoc
	default:
		panic(0)
	}
	se.comment(fmt.Sprintf("Shift by variable $%d", shiftAmtLoc))
	// If any bits from OP_MAX_SHIFT..OP_BITS are set, then A is 0
	zeroedLoc := se.nextVar()
	se.comment(fmt.Sprintf("Control var for shift ≥64: ^%d", zeroedLoc))
	se.addEqConstraintOrOfRange(zeroedLoc, shiftAmtLoc+OP_MAX_SHIFT, shiftAmtLoc+OP_BITS)
	for i := dest + OP_MAX_SHIFT; i < dest+OP_BITS; i += 1 {
		se.addImpliesConstraint(yes(zeroedLoc), no(i))
	}
	// Otherwise, add constraints for each shift value
	for shift := 0; shift < OP_BITS; shift += 1 {
		shiftedByThisAmtLoc := se.nextVar()
		se.comment(fmt.Sprintf("Control var for shift %d: ^%d", shift, shiftedByThisAmtLoc))
		se.addEqConstraintMatchingBits(shiftedByThisAmtLoc, shiftAmtLoc, OP_MAX_SHIFT, shift)
		for i := 0; i < OP_BITS; i += 1 {
			if i+shift >= OP_BITS {
				// If shiftedByThisAmountLoc is true, then any overshifted bits are unset.
				se.addImpliesConstraint(yes(shiftedByThisAmtLoc), no(dest+i))
			} else {
				// If shiftedByThisAmountLoc is true, then dest[i] == a_old[i + x]
				// for non-overshifted bits
				se.addCondEqConstraint(yes(shiftedByThisAmtLoc), dest+i, se.aLoc+i+shift)
			}
		}
	}
	return dest
}

func (se *SymbolicExecutor) execute(programList []byte, ip int, op int) bool {
	for ip < len(programList) {
		// fmt.Printf("executing inst %d at %d\n", programList[ip], ip)
		switch programList[ip] {
		case 0:
			shiftSrc := int(programList[ip+1])
			se.aLoc = se.executeShift(shiftSrc)
		case 1:
			newB := se.nextBlock()
			se.comment(fmt.Sprintf("Set $%d to $%d ^ %d", newB, se.bLoc, programList[ip+1]))
			for i := 0; i < 3; i += 1 {
				n := newB + i
				b := se.bLoc + i
				if (programList[ip+1] & (1 << i)) != 0 {
					se.addXorConstraint(n, b)
				} else {
					se.addEqConstraint(n, b)
				}
			}
			for i := 3; i < OP_BITS; i += 1 {
				n := newB + i
				b := se.bLoc + i
				se.addEqConstraint(n, b)
			}
			se.bLoc = newB
		case 2:
			opType := programList[ip+1]
			newB := se.nextBlock()
			var opVars int
			switch opType {
			case 0, 1, 2, 3:
				se.comment(fmt.Sprintf("Set $%d to %d", newB, opType))
				for i := 0; i < 3; i += 1 {
					se.addConstraint([]Literal{ci((opType&(1<<i)) != 0, newB+i)})
				}
				for i := 3; i < OP_BITS; i += 1 {
					se.addConstraint([]Literal{no(newB + i)})
				}
				return true
			case 4:
				opVars = se.aLoc
			case 5:
				opVars = se.bLoc
			case 6:
				opVars = se.cLoc
			default:
				panic(0)
			}
			se.comment(fmt.Sprintf("Set $%d to $%d & 7", newB, opVars))
			for i := 0; i < 3; i += 1 {
				se.addEqConstraint(newB+i, opVars+i)
			}
			for i := 3; i < OP_BITS; i += 1 {
				se.addConstraint([]Literal{no(newB + i)})
			}
			se.bLoc = newB
		case 3:
			// Fork the VM into a == 0 and a != 0 cases
			a0Loc := se.nextVar()
			se.comment(fmt.Sprintf("Set ^%d iff $%d is zero", a0Loc, se.aLoc))
			se.addEqConstraintMatchingBits(a0Loc, se.aLoc, OP_BITS, 0)
			success := false
			// Try jumping
			cp := se.save()
			// Either we do not jump (i.e. a == 0) or clauses under this execute must satisfy
			se.guardStack = append(se.guardStack, yes(a0Loc))
			succBranch := se.execute(programList, int(programList[ip+1]), op)
			se.guardStack = se.guardStack[0 : len(se.guardStack)-1]
			if !succBranch {
				se.restoreAndRollbackClauses(cp)
				// Can’t jump, so a must be zero
				se.comment("Cannot jump")
				se.addConstraint([]Literal{yes(a0Loc)})
			} else {
				success = true
				se.restore(cp)
			}
			// Try not jumping
			cp = se.save()
			// Either we jump (i.e. a != 0) or clauses under this execute must satisfy
			se.guardStack = append(se.guardStack, no(a0Loc))
			succBranch = se.execute(programList, ip+2, op)
			se.guardStack = se.guardStack[0 : len(se.guardStack)-1]
			if !succBranch {
				se.restoreAndRollbackClauses(cp)
				// Need to jump, so a can’t be zero
				se.addConstraint([]Literal{no(a0Loc)})
			} else {
				success = true
				se.restore(cp)
			}
			return success
		case 4:
			newB := se.nextBlock()
			se.comment(fmt.Sprintf("Set $%d to $%d ^ $%d", newB, se.bLoc, se.cLoc))
			for i := 0; i < OP_BITS; i += 1 {
				n := newB + i
				b := se.bLoc + i
				c := se.cLoc + i
				se.addConstraint([]Literal{yes(n), yes(b), no(c)})
				se.addConstraint([]Literal{yes(n), no(b), yes(c)})
				se.addConstraint([]Literal{no(n), yes(b), yes(c)})
				se.addConstraint([]Literal{no(n), no(b), no(c)})
			}
			se.bLoc = newB
		case 5:
			if op >= len(programList) {
				return false
			}
			operand := programList[ip+1]
			expected := programList[op]
			var outSrc int
			switch operand {
			case 0, 1, 2, 3:
				if operand != expected {
					return false
				}
				op += 1
				continue
			case 4:
				outSrc = se.aLoc
			case 5:
				outSrc = se.bLoc
			case 6:
				outSrc = se.cLoc
			default:
				panic(0)
			}
			se.comment(fmt.Sprintf("Check that lower bits of %d are equal to %d", outSrc, expected))
			se.addConstraint([]Literal{ci((expected&1) != 0, outSrc)})
			se.addConstraint([]Literal{ci((expected&2) != 0, outSrc+1)})
			se.addConstraint([]Literal{ci((expected&4) != 0, outSrc+2)})
			op += 1
		case 6:
			shiftSrc := int(programList[ip+1])
			se.bLoc = se.executeShift(shiftSrc)
		case 7:
			shiftSrc := int(programList[ip+1])
			se.cLoc = se.executeShift(shiftSrc)
		}
		ip += 2
	}
	return op == len(programList)
}

const UNSOLVED = 255

func by(b bool) byte {
	if b {
		return 1
	}
	return 0
}

func chooseUnknownVar(given []byte) int {
	// Choose a variable to guess.
	// Prioritize the first OP_BITS, in reverse order,
	// so that we prioritize lower initial values of the A register
	for i := OP_BITS - 1; i >= 0; i -= 1 {
		if i < len(given) && given[i] == UNSOLVED {
			return i
		}
	}
	for i := OP_BITS; i < len(given); i += 1 {
		if given[i] == UNSOLVED {
			return i
		}
	}
	panic(0)
}

func solveGiven(constraints [][]Literal, given []byte) []byte {
	for {
		propagatedConstraints := [][]Literal{}
		progress := false
		for _, constraint := range constraints {
			newConstraint := []Literal{}
			satisfiable := false
			alreadySatisfied := false
			for _, l := range constraint {
				if given[l.v] == UNSOLVED {
					newConstraint = append(newConstraint, l)
					satisfiable = true
				} else {
					b := given[l.v] != 0
					p := l.polarity
					if b == p {
						satisfiable = true
						progress = true
						alreadySatisfied = true
					}
				}
			}
			if !satisfiable {
				return nil
			} else if len(newConstraint) < len(constraint) {
			}
			if !alreadySatisfied {
				if len(newConstraint) == 1 {
					// Unit clause; propagate
					given[newConstraint[0].v] = by(newConstraint[0].polarity)
				} else if len(newConstraint) > 0 {
					// Don’t add empty clauses
					propagatedConstraints = append(propagatedConstraints, newConstraint)
				}
			}
		}
		if len(propagatedConstraints) == 0 { // No more constraints to satisfy
			return given
		}
		if !progress {
			v := chooseUnknownVar(given)
			givenWithVarUnset := slices.Clone(given)
			givenWithVarUnset[v] = 0
			solution := solveGiven(constraints, givenWithVarUnset)
			if solution != nil {
				return solution
			}
			given[v] = 1
		}
		constraints = propagatedConstraints
	}
}

// Solves a Boolean satisfiability problem in CNF.
func solve(constraints [][]Literal, nVars int) []byte {
	return solveGiven(constraints, slices.Repeat([]byte{UNSOLVED}, nVars))
}

func exportToDimacs(constraints [][]Literal, comments []Comment, nVars int, out string) {
	f, err := os.Create(out)
	check(err)

	defer f.Close()

	cidx := 0

	fmt.Fprintf(f, "p cnf %d %d\n", nVars, len(constraints))
	for i, clause := range constraints {
		for cidx < len(comments) && comments[cidx].cidx <= i {
			fmt.Fprintf(f, "c %s\n", comments[cidx].text)
			cidx += 1
		}
		for _, l := range clause {
			if !l.polarity {
				fmt.Fprintf(f, "-%d ", l.v+1)
			} else {
				fmt.Fprintf(f, "%d ", l.v+1)
			}
		}
		fmt.Fprintf(f, "0\n")
	}
}

type Vm struct {
	programList []byte
	a           int64
	b           int64
	c           int64
	ip          int
	op          int
}

func (vm *Vm) comboOp() int64 {
	switch vm.programList[vm.ip+1] {
	case 0:
		return 0
	case 1:
		return 1
	case 2:
		return 2
	case 3:
		return 3
	case 4:
		return vm.a
	case 5:
		return vm.b
	case 6:
		return vm.c
	default:
		return 0
	}
}

func satisfied(programList []byte, a int64, b int64, c int64) bool {
	vm := Vm{programList: programList, a: a, b: b, c: c}
	for vm.ip < len(programList)-1 {
		switch programList[vm.ip] {
		case 0:
			vm.a >>= vm.comboOp()
		case 1:
			vm.b ^= int64(vm.programList[vm.ip+1])
		case 2:
			vm.b = vm.comboOp() & 7
		case 3:
			if vm.a != 0 {
				vm.ip = int(vm.programList[vm.ip+1]) - 2
			}
		case 4:
			vm.b ^= vm.c
		case 5:
			if vm.op >= len(vm.programList) || vm.programList[vm.op] != byte(vm.comboOp()&7) {
				return false
			}
			vm.op += 1
		case 6:
			vm.b = vm.a >> vm.comboOp()
		case 7:
			vm.c = vm.a >> vm.comboOp()
		}
		vm.ip += 2
	}
	return vm.op == len(vm.programList)
}

func main() {
	input, err := os.ReadFile("day17/input.txt")
	check(err)
	inputStr := string(input)
	var a int64 = 0
	var b int64 = 0
	var c int64 = 0
	programStr := ""
	_, err = fmt.Sscanf(inputStr, "Register A: %d\nRegister B: %d\nRegister C: %d\n\nProgram: %s\n", &a, &b, &c, &programStr)
	check(err)
	programListS := strings.Split(programStr, ",")
	programList := []byte{}
	for _, op := range programListS {
		programList = append(programList, op[0]-'0')
	}
	se := makeSymbolicExecutor(b, c)
	success := se.execute(programList, 0, 0)
	// return
	if !success {
		fmt.Println("warning: failed")
	}
	sol := solve(se.constraints, se.nVars)
	// fmt.Println(se)
	// fmt.Println(sol)
	res := 0
	for i := 0; i < OP_BITS; i += 1 {
		if sol[i] == 1 {
			res += (1 << i)
		}
	}
	fmt.Println(res)

}
