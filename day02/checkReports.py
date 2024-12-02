def parse_input(filename):
    with open(filename) as f:
        for line in f:
            yield [int(x) for x in line.strip().split(' ')]

def report_is_safe(report):
    sign = 1 if report[1] - report[0] >= 0 else -1
    for i, x in enumerate(report[:-1]):
        diff = (report[i+1]-x) * sign
        if diff < 1 or diff > 3:
            return False
    return True

def count_safe_reports(reports):
    return sum([report_is_safe(r) for r in reports])

if __name__ == '__main__':
    print(f"Safe report count: {count_safe_reports(parse_input('input.txt'))}")