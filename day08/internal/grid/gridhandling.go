package grid

import "fmt"

func inBounds(x, y, w, h int) bool {
	return x >= 0 && y >= 0 && x < w && y < h
}

func conditionalPut(m *map[string]struct{}, x, y, w, h int) bool {
	if inBounds(x, y, w, h) {
		(*m)[fmt.Sprintf("%d,%d", x, y)] = struct{}{}
		return true
	}
	return false
}

func GridToString(antennaMap *[][]byte, antinodes *map[string]struct{}) string {
	var result string
	for i, row := range *antennaMap {
		for j, char := range row {
			if antinodes != nil {
				key := fmt.Sprintf("%d,%d", j, i)
				if _, exists := (*antinodes)[key]; exists {
					result += "#"
					continue
				}
			}
			result += string(char)
		}
		if i < len(*antennaMap)-1 {
			result += "\n"
		}
	}
	return result
}

func LocateAntennas(antennaMap [][]byte) map[byte][][]int {
	locations := make(map[byte][][]int)
	for i, row := range antennaMap {
		for j, char := range row {
			if char != '.' {
				if locs, exists := locations[char]; exists {
					locations[char] = append(locs, []int{j, i})
				} else {
					locations[char] = [][]int{{j, i}}
				}
			}
		}
	}
	return locations
}

func LocateAntinodes(antennas [][]int, width, height int) *map[string]struct{} {
	antinodes := make(map[string]struct{})
	for i, a := range antennas {
		for _, b := range antennas[i+1:] {
			dx := a[0] - b[0]
			dy := a[1] - b[1]
			conditionalPut(&antinodes, a[0]+dx, a[1]+dy, width, height)
			conditionalPut(&antinodes, b[0]-dx, b[1]-dy, width, height)
		}
	}
	return &antinodes
}

func LocateAllAntinodes(antennas [][]int, width, height int) *map[string]struct{} {
	antinodes := make(map[string]struct{})
	for i, a := range antennas {
		for _, b := range antennas[i+1:] {
			dx := a[0] - b[0]
			dy := a[1] - b[1]
			for i := 0; conditionalPut(&antinodes, a[0]+i*dx, a[1]+i*dy, width, height); i++ {
			}
			for i := 0; conditionalPut(&antinodes, b[0]-i*dx, b[1]-i*dy, width, height); i++ {
			}
		}
	}
	return &antinodes
}
