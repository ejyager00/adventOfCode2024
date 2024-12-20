import sys

DIRECTIONS = ((0,-1),(-1,0),(0,1),(1,0))

def parse_input(filename: str) -> list[str]:
    with open(filename) as f:
        return f.read().strip().split("\n")

def get_start_and_end(racetrack: list[str]) -> tuple[tuple[int, int],tuple[int, int]]:
    start = ()
    end = ()
    for i, row in enumerate(racetrack):
        if row.find('S')>-1:
            start = (i,row.find('S'))
            if end: return (start, end)
        elif row.find('E')>-1:
            end = (i,row.find('E'))
            if start: return (start, end)
    return (start, end)

def get_track_positions(racetrack: list[str], start: tuple[int, int], end: tuple[int, int]) -> dict[tuple[int, int],int]:
    last_position = ()
    position = start
    track_positions = {}
    while position!=end:
        track_positions[position] = len(track_positions)
        for y, x in DIRECTIONS:
            if racetrack[position[0]+y][position[1]+x]=='.' and (position[0]+y,position[1]+x)!=last_position:
                last_position, position = position, (position[0]+y,position[1]+x)
                break
    else:
        track_positions[position] = len(track_positions)
    return track_positions

def get_cheats(racetrack: list[str], min_saving: int) -> int:
    start, end = get_start_and_end(racetrack)
    racetrack[start[0]] = racetrack[start[0]].replace('S','.')
    racetrack[end[0]] = racetrack[end[0]].replace('E','.')
    track_positions = get_track_positions(racetrack,start, end)
    cheats = 0
    for ty, tx in track_positions:
        for y, x in DIRECTIONS:
            if track_positions.get((ty+2*y, tx+2*x),-1)>track_positions[(ty,tx)] and (ty+y, tx+x) not in track_positions:
                time_saved = track_positions[(ty+2*y, tx+2*x)]-track_positions[(ty,tx)]-2
                # print(f"cheating from {(ty,tx)} to {(ty+2*y, tx+2*x)} saves {time_saved} picoseconds")
                cheats += 1 if time_saved>=min_saving else 0
    return cheats
        
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    try:
        MIN_SAVINGS = 100
        lines = parse_input(sys.argv[1])
        print(f"The number of ways to save at least {MIN_SAVINGS} picoseconds is {get_cheats(lines, MIN_SAVINGS)}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{sys.argv[1]}'")