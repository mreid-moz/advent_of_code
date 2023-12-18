def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def rows_to_cols(rows):
    cols = []
    for i in range(len(rows[0])):
        cols.append(''.join([r[i] for r in rows]))
    return cols

def draw_map(m, max_x, max_y, min_x=0, min_y=0, print_now=True, default_char='.'):
    lines = []
    for y in range(min_y, max_y+1, 1):
        chars = []
        for x in range(min_x, max_x+1, 1):
            chars.append(m.get((x, y), default_char))
        lines.append(''.join(chars))
        if print_now:
            print(lines[-1])
    return lines

def coalesce(v, default_char):
    if v is None:
        return default_char
    return v

def draw_grid(g, print_now=True, default_char='.'):
    lines = []
    for row in g:
        line = ''.join(str(coalsece(x, default_char) for x in g[row]))
        if print_now:
            print(line)
        lines.append(line)
    return lines

def map_to_grid(m, mx, my):
    grid = []
    for y in range(my):
        grid.append([] * x)
    for kx, ky in m.keys():
        grid[ky][kx] = m[(kx, ky)]

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


def get_closest_tentative(unvisited, distances):
    candidate = None
    candidate_dist = -1
    for k, v in distances.items():
        if k in unvisited:
            if candidate is None or v < candidate_dist:
                candidate = k
                candidate_dist = v
    return candidate

def dijkstra(grid):
    tentatives = {}
    unvisited_nodes = set()
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            unvisited_nodes.add((r,c))

    current = (0,0)
    tentatives[current] = 0
    while unvisited_nodes:
        r, c = current
        for next_row, next_col in [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]:
            if next_row < 0 or next_row >= rows:
                continue
            if next_col < 0 or next_col >= cols:
                continue
            if next_col == c and next_row == r:
                continue

            neighbour = (next_row, next_col)
            # logging.debug("from {},{} looking at neighbour {},{}".format(r, c, next_row, next_col))
            if neighbour not in unvisited_nodes:
                continue
            neigh_distance = tentatives[current] + grid[next_row][next_col]
            if neighbour not in tentatives or tentatives[neighbour] > neigh_distance:
                tentatives[neighbour] = neigh_distance

        unvisited_nodes.remove(current)
        if current == (rows - 1, cols - 1):
            break
        current = get_closest_tentative(unvisited_nodes, tentatives)
    return tentatives[current]
