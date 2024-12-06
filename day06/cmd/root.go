package cmd

import (
	"fmt"
	"os"

	"github.com/ejyager00/adventOfCode2024/day06/internal/io"
	"github.com/ejyager00/adventOfCode2024/day06/internal/path"
	"github.com/spf13/cobra"
)

func countGuardCoverage(situationMap [][]byte) int {
	y, x := path.FindFirstArrow(&situationMap)
	direction := path.GetDirection(situationMap[y][x])
	fmt.Println("Starting at ", y, x, " facing ", direction)
	return 0
}

var rootCmd = &cobra.Command{
	Use:   "track-guard",
	Short: "Solution for 2024 Advent of Code day six.",
	Long:  `Solution for 2024 Advent of Code day six.`,
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		situationMap, err := io.ReadFileToByteSlices(args[0])
		if err != nil {
			fmt.Println("Error reading file: ", err)
			return
		}
		fmt.Printf("The guard visited %d positions.\n", countGuardCoverage(situationMap))
	},
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {

}
