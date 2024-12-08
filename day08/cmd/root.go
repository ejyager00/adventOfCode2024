package cmd

import (
	"fmt"
	"os"

	"github.com/ejyager00/adventOfCode2024/day08/internal/io"
	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "antinodes",
	Short: "Solution for 2024 Advent of Code day six.",
	Long:  `Solution for 2024 Advent of Code day six.`,
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		grid, err := io.ReadFileToByteSlices(args[0])
		if err != nil {
			fmt.Println("Error reading file: ", err)
			return
		}
		fmt.Println(grid)
	},
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {}
