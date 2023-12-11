def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def neighbours(x, y, min_x=None, max_x=None, min_y=None, max_y=None, include_diagonals=True):
    n = []
    for xd in [-1, 0, 1]:
        nx = x + xd
        if min_x is not None and nx < min_x:
            continue
        if max_x is not None and nx > max_x:
            continue
        for yd in [-1, 0, 1]:
            if xd == 0 and yd == 0:
                continue
            if not include_diagonals and (xd != 0 and yd != 0):
                continue
            ny = y + yd
            if min_y is not None and ny < min_y:
                continue
            if max_y is not None and ny > max_y:
                continue
            n.append((nx, ny))
    return n

def get_overlap(a_start, a_end, b_start, b_end):
    # a.......a
    #      b......b
    #      ^  ^

    #    a.......a
    # b......b
    #    ^   ^

    # a.......a
    #              b......b
    #      None
    overlap_start = max(a_start, b_start)
    overlap_end = min(a_end, b_end)
    if overlap_end >= overlap_start:
        return (overlap_start, overlap_end)
    return None

def manhattan(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)
