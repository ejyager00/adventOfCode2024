package path

import "github.com/golang-collections/collections/set"

const (
	Up = iota
	Down
	Left
	Right
)

func FindFirstArrow(grid *[][]byte) (int, int) {
	for y := range *grid {
		for x := range (*grid)[y] {
			switch (*grid)[y][x] {
			case '^', '>', '<', 'v':
				return y, x
			}
		}
	}
	return -1, -1
}

func GetDirection(guard byte) int {
	switch guard {
	case '^':
		return Up
	case '>':
		return Right
	case '<':
		return Left
	case 'v':
		return Down
	}
	return -1
}

func StepGuard(grid *[][]byte, y *int, x *int, direction *int, visited *set.Set) bool {
	return false
}
