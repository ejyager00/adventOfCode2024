def parse_input(filename: str) -> list[list[int]]:
    with open(filename) as f:
        for line in f:
            yield [int(x) for x in line.strip().split(' ')]

def report_is_safe(report: list[int], tolerance: int) -> bool:
    if len(report) < 2:
        return True
        
    def check_sequence(seq: list[int]) -> bool:
        diffs = [b - a for a, b in zip(seq, seq[1:])]
        sign = -1 if sum(d < 0 for d in diffs) > len(diffs)//2 else 1
        return all(1 <= diff * sign <= 3 for diff in diffs)
    
    if check_sequence(report):
        return True
        
    if tolerance > 0:
        for i in range(len(report)):
            new_report = report[:i] + report[i+1:]
            if report_is_safe(new_report, tolerance - 1):
                return True
                
    return False

def count_safe_reports(reports: list[list[int]], tolerance: int = 0) -> int:
    return sum([report_is_safe(r, tolerance) for r in reports])

if __name__ == '__main__':
    print(f"Safe report count: {count_safe_reports(parse_input('input.txt'))}")
    print(f"Safe report count: {count_safe_reports(parse_input('input.txt'), 1)}")
