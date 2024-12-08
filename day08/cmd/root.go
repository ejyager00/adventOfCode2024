package cmd

import (
	"fmt"
	"os"

	"github.com/ejyager00/adventOfCode2024/day08/internal/grid"
	"github.com/ejyager00/adventOfCode2024/day08/internal/io"
	"github.com/ejyager00/adventOfCode2024/day08/internal/maps"
	"github.com/spf13/cobra"
)

func countAntinodes(antennaMap [][]byte) int {
	//fmt.Println(grid.GridToString(&antennaMap, nil))
	locations := grid.LocateAntennas(antennaMap)
	antinodes := make(map[string]struct{})
	w, h := len(antennaMap[0]), len(antennaMap)
	for _, locs := range locations {
		maps.AddAll(&antinodes, grid.LocateAntinodes(locs, w, h))
	}
	//fmt.Println()
	//fmt.Println(grid.GridToString(&antennaMap, &antinodes))
	return len(antinodes)
}

var rootCmd = &cobra.Command{
	Use:   "antinodes",
	Short: "Solution for 2024 Advent of Code day six.",
	Long:  `Solution for 2024 Advent of Code day six.`,
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		antennaMap, err := io.ReadFileToByteSlices(args[0])
		if err != nil {
			fmt.Println("Error reading file: ", err)
			return
		}
		fmt.Printf("There are %d unique antinode locations.\n", countAntinodes(antennaMap))
	},
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {}
