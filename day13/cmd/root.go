package cmd

import (
	"fmt"
	"os"

	"github.com/ejyager00/adventOfCode2024/day13/internal/input"
	"github.com/ejyager00/adventOfCode2024/day13/internal/strategy"
	"github.com/spf13/cobra"
)

func cheapestPrizeStrategy(games *[]input.Game) int {
	tokens := 0
	for _, game := range *games {
		tokens += strategy.MinPrizeTokens(&game)
	}
	return tokens
}

var rootCmd = &cobra.Command{
	Use:   "antinodes",
	Short: "Solution for 2024 Advent of Code day six.",
	Long:  `Solution for 2024 Advent of Code day six.`,
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		clawGames, err := input.ParseInput(args[0])
		if err != nil {
			fmt.Println("Error reading file: ", err)
			return
		}
		fmt.Printf("Minimum tokens for maximum prizes: %d\n", cheapestPrizeStrategy(&clawGames))
		for i := range clawGames {
			clawGames[i].Point[0] += 10000000000000
			clawGames[i].Point[1] += 10000000000000
		}
		fmt.Printf("Minimum tokens with new coordinates: %d\n", cheapestPrizeStrategy(&clawGames))
	},
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {}
