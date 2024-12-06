import sys

def parse_input(filename):
    first_nums = []
    second_nums = []
    
    with open(filename, 'r') as f:
        for line in f:
            nums = [int(x) for x in line.split()]
            first_nums.append(nums[0])
            second_nums.append(nums[1])
    
    return (first_nums, second_nums)

# Day one part one solution
def get_distance(list1, list2):
    list1.sort()
    list2.sort()

    total_distance = 0
    for x, y in zip(list1, list2):
        total_distance += abs(x - y)
    return total_distance

# Day one part two solution
def get_similarity(list1, list2):
    ids = set(list1)

    total_similarity = 0
    for id in list2:
        if id in ids:
            total_similarity += id
    return total_similarity

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python findLocations.py <input_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    
    try:
        first_list, second_list = parse_input(input_file)
        print(f"Total distance: {get_distance(first_list, second_list)}")
        print(f"Total similarity: {get_similarity(first_list, second_list)}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")