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

func mapContains(visited *map[string][]int, y int, x int, d int) bool {
	if dirs, ok := (*visited)[fmt.Sprintf("%d,%d", y, x)]; !ok {
		return false
	} else if listContains(&dirs, d) {
		return true
	}
	return false
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

func CountGuardSteps(grid *[][]byte, y int, x int, direction int) (int, bool) {
	var visited map[string][]int = make(map[string][]int)
	// visited[fmt.Sprintf("%d,%d", y, x)] = []int{direction}
	// ydiff, xdiff := DIRECTION_DIFFS[direction][0], DIRECTION_DIFFS[direction][1]
	for y >= 0 && x >= 0 && y < len(*grid) && x < len((*grid)[0]) && !mapContains(&visited, y, x, direction) {
		newKey := fmt.Sprintf("%d,%d", y, x)
		if dirs, ok := visited[newKey]; ok {
			visited[newKey] = append(dirs, direction)
		} else {
			visited[newKey] = []int{direction}
		}
		ydiff, xdiff := DIRECTION_DIFFS[direction][0], DIRECTION_DIFFS[direction][1]
		y += ydiff
		x += xdiff
		if y >= 0 && x >= 0 && y < len(*grid) && x < len((*grid)[0]) && (*grid)[y][x] == '#' {
			direction = (direction + 1) % 4
			y -= ydiff
			x -= xdiff
		}
	}
	return len(visited), mapContains(&visited, y, x, direction)
}
