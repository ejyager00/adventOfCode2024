import matplotlib.pyplot as plt
import networkx
import numpy as np
import sys

def parse_input(filename: str) -> list[list[int]]:
    top_map = []
    with open(filename) as f:
        for line in f:
            top_map.append([int(x) for x in line.strip()])
    return top_map

def build_graph(arr):
    G = networkx.DiGraph()
    arr = np.array(arr)
    rows, cols = arr.shape

    # Add nodes
    for i in range(rows):
        for j in range(cols):
            G.add_node((i, j), value=arr[i, j])

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Add edges
    for i in range(rows):
        for j in range(cols):
            current_value = arr[i, j]
            for dx, dy in directions:
                nx, ny = i + dx, j + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    neighbor_value = arr[nx, ny]
                    if neighbor_value == current_value + 1:
                        G.add_edge((i, j), (nx, ny))

    return G

def count_paths(G, start_num, end_num):
    start_nodes = [node for node, data in G.nodes(data=True) if data.get('value') == start_num]
    end_nodes = [node for node, data in G.nodes(data=True) if data.get('value') == end_num]
    
    path_count = 0
    
    for start in start_nodes:
        for end in end_nodes:
            if networkx.has_path(G, start, end):
                path_count += 1
    
    return path_count

def count_unique_paths(G, start_num, end_num):
    start_nodes = [node for node, data in G.nodes(data=True) if data.get('value') == start_num]
    end_nodes = [node for node, data in G.nodes(data=True) if data.get('value') == end_num]
    
    path_count = 0
    
    for start in start_nodes:
        for end in end_nodes:
            path_count += len(list(networkx.all_simple_paths(G, start, end)))
    
    return path_count

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python checkReports.py <input_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]

    try:
        top_map = parse_input(input_file)
        graph = build_graph(top_map)
        print(f"Total paths: {count_paths(graph, 0, 9)}")
        print(f"Total unique paths: {count_unique_paths(graph, 0, 9)}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")