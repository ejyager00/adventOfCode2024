import sys

def print_warehouse(warehouse: list[list[str]]):
    print("\n".join(["".join(x) for x in warehouse]))

def parse_input(filename: str) -> tuple[list[str], tuple[str, ...]]:
    with open(filename) as f:
        map_text, moves_text = f.read().split('\n\n')
        return [[x for x in y] for y in map_text.split("\n")], tuple([x for x in moves_text.replace("\n","")])

def locate_robot(warehouse: list[list[str]]) -> tuple[int, int]:
    for i, row in enumerate(warehouse):
        for j, spot in enumerate(row):
            if spot=='@':
                return i, j
    return -1, -1

def get_direction(move: str) -> tuple[int, int]:
    match move:
        case "v": return 1, 0
        case "^": return -1, 0
        case ">": return 0, 1
        case "<": return 0, -1
        case _: return 0, 0

def move_robot(warehouse: list[list[str]], move: str, robot: tuple[int, int]) -> tuple[int, int]:
    dyx = get_direction(move)
    loc = list(robot)
    neighbor = warehouse[loc[0]+dyx[0]][loc[1]+dyx[1]]
    shifting = 1
    while neighbor != "#" and neighbor != ".":
        shifting += 1
        loc[0]+=dyx[0]
        loc[1]+=dyx[1]
        neighbor = warehouse[loc[0]+dyx[0]][loc[1]+dyx[1]]
    if neighbor == "#":
        return robot
    if shifting>1:
        for i in range(shifting, 1, -1):
            warehouse[robot[0]+i*dyx[0]][robot[1]+i*dyx[1]]=warehouse[robot[0]+(i-1)*dyx[0]][robot[1]+(i-1)*dyx[1]]
    warehouse[robot[0]][robot[1]]="."
    warehouse[robot[0]+dyx[0]][robot[1]+dyx[1]]="@"
    return robot[0]+dyx[0], robot[1]+dyx[1]

def find_moved_boxes(warehouse: list[list[str]], box: tuple[int, int], dy: int) -> tuple[list[tuple[int, int]], bool]:
    if warehouse[box[0]+dy][box[1]]=="#" or warehouse[box[0]+dy][box[1]+1]=="#":
        return None, True
    if warehouse[box[0]+dy][box[1]]=="[":
        boxes, blocked = find_moved_boxes(warehouse, (box[0]+dy,box[1]), dy)
        if blocked:
            return None, True
        return [box]+boxes, False
    boxes = [box]
    if warehouse[box[0]+dy][box[1]]=="]":
        left_boxes, blocked = find_moved_boxes(warehouse, (box[0]+dy,box[1]-1), dy)
        if blocked:
            return None, True
        boxes+=left_boxes
    if warehouse[box[0]+dy][box[1]+1]=="[":
        right_boxes, blocked = find_moved_boxes(warehouse, (box[0]+dy,box[1]+1), dy)
        if blocked:
            return None, True
        boxes+=right_boxes
    return boxes, False

def move_robot_expanded(warehouse: list[list[str]], move: str, robot: tuple[int, int]) -> tuple[int, int]:
    print_warehouse(warehouse)
    print()
    dyx = get_direction(move)
    if dyx[0]==0:
        return move_robot(warehouse, move, robot)
    loc = robot
    dy = dyx[0]
    if warehouse[loc[0]+dy][loc[1]]=="#":
        return robot
    if warehouse[loc[0]+dy][loc[1]]==".":
        warehouse[robot[0]][robot[1]]="."
        warehouse[robot[0]+dy][robot[1]]="@"
        return robot[0]+dy, robot[1]
    start = (loc[0]+dy, loc[1]) if warehouse[loc[0]+dy][loc[1]]=="[" else (loc[0]+dy, loc[1]-1)
    boxes, blocked = find_moved_boxes(warehouse, start, dy)
    if blocked:
        return robot
    for box in boxes[::-1]:
        warehouse[box[0]][box[1]]="."
        warehouse[box[0]][box[1]+1]="."
        warehouse[box[0]+dy][box[1]]="["
        warehouse[box[0]+dy][box[1]+1]="]"
    warehouse[robot[0]][robot[1]]="."
    warehouse[robot[0]+dy][robot[1]]="@"
    if start[1]==robot[1]:
        warehouse[robot[0]+dy][robot[1]+1]="."
    else:
        warehouse[robot[0]+dy][robot[1]-1]="."
    return robot[0]+dy, robot[1]

def sum_gps(warehouse: list[list[str]]) -> int:
    total = 0
    for i, row in enumerate(warehouse):
        for j, spot in enumerate(row):
            if spot=='O' or spot=="[":
                total += i*100+j
    return total

def expand_warehouse(warehouse: list[list[str]]) -> list[list[str]]:
    return [[x for x in "".join(row).replace("#","##").replace("O","[]").replace(".","..").replace("@","@.")] for row in warehouse]

def move_and_tally(warehouse: list[list[str]], moves: tuple[str, ...], big: bool = False) -> int:
    loc = locate_robot(warehouse)
    move = move_robot_expanded if big else move_robot
    for m in moves:
        loc = move(warehouse, m, loc)
    return sum_gps(warehouse)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python checkReports.py <input_file>")
        sys.exit(1)

    try:
        warehouse, movements = parse_input(sys.argv[1])
        big_warehouse = expand_warehouse(warehouse)
        print(f"The sum of all boxes' GPS coordinates is {move_and_tally(warehouse, movements)}.")
        print(f"The sum of all boxes' GPS coordinates in the big warehouse is {move_and_tally(big_warehouse, movements, big=True)}.")
        print_warehouse(big_warehouse)
    except FileNotFoundError:
        print(f"Error: Could not find input file '{sys.argv[1]}'")