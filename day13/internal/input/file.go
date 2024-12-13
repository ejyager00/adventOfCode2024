package input

import (
	"bufio"
	"os"
	"strconv"
	"strings"
)

type Game struct {
	A     [2]int
	B     [2]int
	Point [2]int
}

func ParseInput(filePath string) ([]Game, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var games []Game
	scanner := bufio.NewScanner(file)
	var currentGame Game

	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			continue
		}

		if strings.HasPrefix(line, "Button A:") {
			parts := strings.Split(line, " ")
			x := strings.TrimPrefix(parts[2], "X+")
			y := strings.TrimPrefix(parts[3], "Y+")
			xVal, _ := strconv.Atoi(x[:len(x)-1])
			yVal, _ := strconv.Atoi(y)
			currentGame.A = [2]int{xVal, yVal}
		} else if strings.HasPrefix(line, "Button B:") {
			parts := strings.Split(line, " ")
			x := strings.TrimPrefix(parts[2], "X+")
			y := strings.TrimPrefix(parts[3], "Y+")
			xVal, _ := strconv.Atoi(x[:len(x)-1])
			yVal, _ := strconv.Atoi(y)
			currentGame.B = [2]int{xVal, yVal}
		} else if strings.HasPrefix(line, "Prize:") {
			parts := strings.Split(line, " ")
			x := strings.TrimPrefix(parts[1], "X=")
			y := strings.TrimPrefix(parts[2], "Y=")
			xVal, _ := strconv.Atoi(x[:len(x)-1])
			yVal, _ := strconv.Atoi(y)
			currentGame.Point = [2]int{xVal, yVal}
			games = append(games, currentGame)
			currentGame = Game{}
		}
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return games, nil
}
