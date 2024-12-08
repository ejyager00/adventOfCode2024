package maps

func AddAll(a *map[string]struct{}, b *map[string]struct{}) {
	for k, v := range *b {
		(*a)[k] = v
	}
}
