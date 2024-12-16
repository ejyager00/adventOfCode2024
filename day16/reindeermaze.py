import sys
import networkx as nx

def parse_input(filename: str):
    with open(filename) as f:
        lines = f.read().strip().split("\n")
    return lines

def create_graph(lines):
    G = nx.DiGraph()
    fourdir = (1, -1, 1j, -1j)
    start = None
    end = None

    for i, line in enumerate(lines):
        for j, x in enumerate(line):
            if x == "#":
                continue
            z = i + 1j * j
            if x == "S":
                start = (z, 1j)
            if x == "E":
                end = z
            for dz in fourdir:
                G.add_node((z, dz))

    for z, dz in G.nodes:
        if (z + dz, dz) in G.nodes:
            G.add_edge((z, dz), (z + dz, dz), weight=1)
        for rot in -1j, 1j:
            G.add_edge((z, dz), (z, dz * rot), weight=1000)

    for dz in fourdir:
        G.add_edge((end, dz), "end", weight=0)

    return G, start, end

def get_shortest_path_length(G, start):
    return nx.shortest_path_length(G, start, "end", weight="weight")

def count_unique_positions(G, start):
    return len({z for path in nx.all_shortest_paths(G, start, "end", weight="weight") 
                for z, _ in path[:-1]})

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        lines = parse_input(input_file)
        G, start, end = create_graph(lines)
        
        print(f"Shortest path length = {get_shortest_path_length(G, start)}")
        print(f"Number of unique positions = {count_unique_positions(G, start)}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")
