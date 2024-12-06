import sys

def parse_input(filename: str):
    rules = {}
    updates = []
    with open(filename) as f:
        content = f.read()
        rule_string, update_string = content.split("\n\n")[:2]
        for rule in rule_string.split('\n'):
            k, v = [int(x) for x in rule.split('|')[:2]]
            try:
                rules[k].add(v)
            except KeyError:
                rules[k] = {v}
        for update in update_string.split('\n'):
            updates.append([int(x) for x in update.split(',')])
    return (rules, updates)

def valid_update(update: list[int], rules: dict) -> bool:
    current = {update[0]}
    for page in update[1:]:
        if len(current.intersection(rules.get(page,set()))) > 0:
            return False
        current.add(page)
    return True

def order_update(update: list[int], rules: dict) -> list[int]:
    current = [update[0]]
    for page in update[1:]:
        if len(set(current).intersection(rules.get(page,set()))) > 0:
            for i, p in enumerate(current):
                if p in rules[page]:
                    current.insert(i, page)
                    break
        else:
            current.append(page)
    return current

def count_valid_updates(updates: list[list[int]], rules: dict):
    return sum([update[int(len(update)/2)] if valid_update(update, rules) else 0 for update in updates])

def count_invalid_updates(updates: list[list[int]], rules: dict):
    return sum([order_update(update, rules)[int(len(update)/2)] if not valid_update(update, rules) else 0 for update in updates])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python checkReports.py <input_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    
    try:
        rules, updates = parse_input(input_file)
        print(f"sum of middle page of valid updates = {count_valid_updates(updates, rules)}")
        print(f"sum of middle page of corrected updates = {count_invalid_updates(updates, rules)}")
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")
    
