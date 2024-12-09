import sys

def parse_input(filename: str) -> str:
    with open(filename) as f:
        return f.read()

def construct_filesystem(diskMap: str) -> list[int]:
    filesys = []
    for i, x in enumerate(diskMap):
        if i%2:
            filesys += [-1]*int(x)
        else:
            filesys += [int(i/2)]*int(x)
    return filesys

def frontload_files(filesys: list[int]):
    p1 = 0
    p2 = len(filesys)-1
    while (p1<p2):
        while p1<p2 and filesys[p1]!=-1:
            p1+=1
        while p2>p1 and filesys[p2]==-1:
            p2-=1
        if p1<p2:
            filesys[p1] = filesys[p2]
            filesys[p2] = -1
    return

def compute_checksum(data: list[int]) -> int:
    checksum = 0
    for i, x in enumerate(data):
        if x != -1:
            checksum += i*x
    return checksum

def get_frontloaded_checksum(diskMap: str) -> int:
    # print(diskMap)
    filesys = construct_filesystem(diskMap)
    # print(''.join(['.' if x==-1 else str(x) for x in filesys]))
    frontload_files(filesys)
    # print(''.join(['.' if x==-1 else str(x) for x in filesys]))
    return compute_checksum(filesys)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python checkReports.py <input_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]

    try:
        diskMap = parse_input(input_file)
        print(get_frontloaded_checksum(diskMap))
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")