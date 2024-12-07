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

func listContains(s *[]int, e int) bool {
	for _, a := range *s {
		if a == e {
			return true
		}
	}
	return false
}

func mapContains(visited *map[string][]int, y, x, d int) bool {
	if dirs, ok := (*visited)[fmt.Sprintf("%d,%d", y, x)]; !ok {
		return false
	} else if listContains(&dirs, d) {
		return true
	}
	return false
}

func isValidPosition(grid *[][]byte, y, x int) bool {
	return y >= 0 && x >= 0 && y < len(*grid) && x < len((*grid)[0])
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

func CountGuardSteps(grid *[][]byte, y, x, direction int) (int, bool) {
	visited := make(map[string][]int)
	for isValidPosition(grid, y, x) && !mapContains(&visited, y, x, direction) {
		key := fmt.Sprintf("%d,%d", y, x)
		if dirs, exists := visited[key]; exists {
			visited[key] = append(dirs, direction)
		} else {
			visited[key] = []int{direction}
		}
		y += DIRECTION_DIFFS[direction][0]
		x += DIRECTION_DIFFS[direction][1]
		if isValidPosition(grid, y, x) && (*grid)[y][x] == '#' {
			y -= DIRECTION_DIFFS[direction][0]
			x -= DIRECTION_DIFFS[direction][1]
			direction = (direction + 1) % 4
		}
	}

	return len(visited), mapContains(&visited, y, x, direction)
}
