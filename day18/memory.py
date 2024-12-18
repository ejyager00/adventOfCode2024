import sys
import networkx as nx

def parse_input(filename: str) -> list[tuple[int, int]]:
    coords = lambda x: tuple(int(y) for y in x.split(","))
    with open(filename) as f:
        return [coords(line.strip()) for line in f]

def create_graph(size: int, fallen_bytes: list[tuple[int, int]]) -> nx.DiGraph:
    G = nx.DiGraph()
    fourdir = (1, -1, 1j, -1j)
    start = (0 + 0j, 1)
    end = (size - 1) + (size - 1) * 1j
    
    obstacles = {x + y*1j for x,y in fallen_bytes}
    
    for i in range(size):
        for j in range(size):
            z = i + 1j * j
            if z in obstacles:
                continue
            for dz in fourdir:
                G.add_node((z, dz))
    
    for z, dz in G.nodes:
        next_pos = z + dz
        if (next_pos, dz) in G.nodes:
            if 0 <= next_pos.real < size and 0 <= next_pos.imag < size:
                G.add_edge((z, dz), (next_pos, dz), weight=1)
        for rot in -1j, 1j:
            if (z, dz * rot) in G.nodes:
                G.add_edge((z, dz), (z, dz * rot), weight=0)
    
    for dz in fourdir:
        if (end, dz) in G.nodes:
            G.add_edge((end, dz), "end", weight=0)
            
    return G

def get_shortest_path_length(G: nx.DiGraph) -> float:
    return nx.shortest_path_length(G, (0 + 0j, 1), "end", weight="weight")

def first_blocking_byte(begin: int, grid_size: int, bad_bytes: list[tuple[int, int]]) -> str:
    left, right = begin, len(bad_bytes)

    def has_path(num_bytes: int) -> bool:
        try:
            test_graph = create_graph(grid_size, bad_bytes[:num_bytes])
            nx.shortest_path_length(test_graph, (0 + 0j, 1), "end", weight="weight")
            return True
        except nx.NetworkXNoPath:
            return False
    
    while left < right:
        mid = (left + right) // 2
        if has_path(mid):
            left = mid + 1
        else:
            right = mid
            
    return f"{bad_bytes[left-1][0]},{bad_bytes[left-1][1]}"
                
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    grid_size = 71
    fallen_bytes = 1024

    try:
        bad_bytes = parse_input(sys.argv[1])
        G = create_graph(grid_size, bad_bytes[:fallen_bytes])
        
        print(f"Shortest path length = {get_shortest_path_length(G)}")
        print(f"The first byte to cutoff the path is {first_blocking_byte(fallen_bytes, grid_size, bad_bytes)}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{sys.argv[1]}'")