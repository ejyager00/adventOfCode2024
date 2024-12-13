package strategy

import (
	"github.com/ejyager00/adventOfCode2024/day13/internal/input"
)

func MinPrizeTokens(game *input.Game) int {
	A, B := 0, 0
	if (game.A[1]*game.B[0] - game.A[0]*game.B[1]) != 0 {
		B = ((game.A[1] * game.Point[0]) - (game.A[0] * game.Point[1])) / (game.A[1]*game.B[0] - game.A[0]*game.B[1])
	}
	if game.A[0] != 0 {
		A = (game.Point[0] - (B * game.B[0])) / game.A[0]
	}

	if ((game.A[0]*A)+(game.B[0]*B)) == game.Point[0] && ((game.A[1]*A)+(game.B[1]*B)) == game.Point[1] {
		return 3*A + B
	}

	return 0
}
