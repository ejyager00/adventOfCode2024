package path

import "fmt"

const (
	Up = iota
	Right
	Down
	Left
)

var DIRECTION_DIFFS = [4][2]int{
	{-1, 0},
	{0, 1},
	{1, 0},
	{0, -1},
}

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

func CountGuardSteps(grid *[][]byte, y int, x int, direction int) int {
	fmt.Printf("Current position: %d, %d\n", y, x)
	var visited map[string]struct{} = make(map[string]struct{})
	visited[fmt.Sprintf("%d,%d", y, x)] = struct{}{}
	ydiff, xdiff := DIRECTION_DIFFS[direction][0], DIRECTION_DIFFS[direction][1]
	for y+ydiff >= 0 && x+xdiff >= 0 && y+ydiff < len(*grid) && x+xdiff < len((*grid)[0]) {
		x = x + xdiff
		y = y + ydiff
		if (*grid)[y][x] == '#' {
			direction = (direction + 1) % 4
			y = y - ydiff + DIRECTION_DIFFS[direction][0]
			x = x - xdiff + DIRECTION_DIFFS[direction][1]
			ydiff = DIRECTION_DIFFS[direction][0]
			xdiff = DIRECTION_DIFFS[direction][1]
		}
		fmt.Printf("Current position: %d, %d\n", y, x)
		visited[fmt.Sprintf("%d,%d", y, x)] = struct{}{}
	}
	return len(visited)
}
