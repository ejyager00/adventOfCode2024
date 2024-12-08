package io

import (
	"bufio"
	"os"
)

func ReadFileToByteSlices(filePath string) ([][]byte, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines [][]byte
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lineBytes := make([]byte, len(scanner.Bytes()))
		copy(lineBytes, scanner.Bytes())
		lines = append(lines, lineBytes)
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return lines, nil
}
