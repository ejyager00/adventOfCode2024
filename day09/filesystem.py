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

def compute_checksum(data: list[int]) -> int:
    checksum = 0
    for i, x in enumerate(data):
        if x != -1:
            checksum += i*x
    return checksum

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

def frontload_whole_files(filesys: list[int], file_sizes: list[int], spaces: list[int]):
    files = [(i, size) for i, size in enumerate(file_sizes)]
    current_pos = 0
    
    for file_id in range(len(files)-1, -1, -1):
        file_size = file_sizes[file_id]
        
        file_start = None
        for i in range(len(filesys)):
            if filesys[i] == file_id:
                file_start = i
                break
                
        if file_start is None:
            continue
            
        space_start = None
        for i in range(len(filesys)):
            if filesys[i] == -1:
                if all(filesys[j] == -1 for j in range(i, min(i + file_size, len(filesys)))):
                    space_start = i
                    break
                    
        if space_start is not None and space_start < file_start:
            for i in range(file_size):
                filesys[space_start + i] = file_id
                filesys[file_start + i] = -1

def get_frontloaded_checksum(diskMap: str) -> int:
    filesys = construct_filesystem(diskMap)
    frontload_files(filesys)
    return compute_checksum(filesys)

def get_unfrag_front_checksum(diskMap: str) -> int:
    file_sizes = [int(x) for x in diskMap[::2]]
    spaces = [int(x) for x in diskMap[1::2]]
    filesys = construct_filesystem(diskMap)
    frontload_whole_files(filesys, file_sizes, spaces)
    return compute_checksum(filesys)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python checkReports.py <input_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]

    try:
        diskMap = parse_input(input_file)
        print(f"Checksum for frontloaded system is      {get_frontloaded_checksum(diskMap)}")
        print(f"Checksum while not fragmenting files is {get_unfrag_front_checksum(diskMap)}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")