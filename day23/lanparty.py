import sys
import networkx as nx

def parse_input(filename: str) -> list[tuple[str,str]]:
    with open(filename) as f:
        return [tuple(x.split('-')) for x in f.read().strip().split("\n")]

def get_connection_groups(connections: list[tuple[str,str]]) -> set[tuple[str,str,str]]:
    connection_groups = {}
    parties = set()
    for conn in connections:
        if conn[0] not in connection_groups:
            connection_groups[conn[0]] = set()
        if conn[1] not in connection_groups:
            connection_groups[conn[1]] = set()
        connection_groups[conn[0]].add(conn[1])
        connection_groups[conn[1]].add(conn[0])
        if len(connection_groups[conn[0]].intersection(connection_groups[conn[1]])) > 0:
            if conn[0][0]=='t' or conn[1][0]=='t':
                for x in connection_groups[conn[0]].intersection(connection_groups[conn[1]]):
                    parties.add(tuple(sorted([conn[0],conn[1],x])))
            else:
                for x in connection_groups[conn[0]].intersection(connection_groups[conn[1]]):
                    if x[0]=='t':
                        parties.add(tuple(sorted([conn[0],conn[1],x])))
    return parties

def get_largest_party(connections: list[tuple[str,str]]) -> tuple[str,...]:
    graph = nx.Graph()
    graph.add_edges_from(connections)

    cliques = list(nx.find_cliques(graph))
    largest_clique = max(cliques, key=len)

    return tuple(sorted(largest_clique))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    try:
        connections = parse_input(sys.argv[1])
        print(f"The number of parties with a 't' is {len(get_connection_groups(connections))}")
        print(f"The largest party is {",".join(get_largest_party(connections))}")
    except FileNotFoundError: 
        print(f"Error: Could not find input file '{sys.argv[1]}'")