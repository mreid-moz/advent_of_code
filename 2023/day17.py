from aocd.models import Puzzle
from collections import defaultdict
from functools import cache
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=17)

TEST = True
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

crucibles = []
for i, line in enumerate(lines):
    crucibles.append([int(s) for s in line])

@cache
def get_direction(a, b):
    (ar, ac) = a
    (br, bc) = b
    dr = br - ar
    dc = bc - ac

    if dr > 0:
        return 'v'
    if dr < 0:
        return '^'
    if dc > 0:
        return '>'
    return '<'

def get_dir_string(path):
    if path == []:
        return ''

    dir_string = ''
    for i in range(len(path) - 1):
        dir_string += get_direction(path[i], path[i+1])
    return dir_string

# def get_closest_tentative(unvisited, distances, path):
#     candidate = None
#     candidate_dist = -1
#     path_str = ''
#     for i in range(len(path) - 1):
#         path_str += get_direction(path[i], path[i+1])
#     logging.debug("Path so far: {}".format(path_str))
#     for k, v in distances.items():
#         if k in unvisited:
#             if candidate is None or v < candidate_dist:
#                 # if len(path) >= 3 and len(set(path[-3:])) == 1:
#                 #     d = get_direction(path[-1], candidate)
#                 #     if d == path_str[-1]:
#                 #         logging.debug("Skipping candidate {} because it results in path {}{}".format(candidate, path_str, d))
#                 #         continue
#                 candidate = k
#                 candidate_dist = v
#     return candidate

# def dijkstra(grid):
#     tentatives = {}
#     unvisited_nodes = set()
#     path = []
#     rows = len(grid)
#     cols = len(grid[0])
#     distances = {}

#     logging.debug("Checking {} rows and {} columns".format(rows, cols))
#     for r in range(rows):
#         for c in range(cols):
#             unvisited_nodes.add((r,c))

#     current = (0,0)
#     path.append(current)
#     tentatives[current] = 0
#     current_dir = 'e'
#     current_dir_count = 0
#     while unvisited_nodes:
#         logging.debug("there are {} unvisited nodes to consider.".format(len(unvisited_nodes)))
#         r, c = current
#         for next_row, next_col, next_d in [(r-1,c, 'n'), (r+1,c, 's'), (r,c-1, 'w'), (r,c+1, 'e')]:
#             if next_row < 0 or next_row >= rows:
#                 continue
#             if next_col < 0 or next_col >= cols:
#                 continue
#             if next_col == c and next_row == r:
#                 continue

#             # if next_d == current_dir and current_dir_count >= 3:
#             #     logging.debug("Not considering {},{} because we've already moved {} {} times".format(next_row, next_col, next_d, current_dir_count))
#             #     continue

#             neighbour = (next_row, next_col)
#             logging.debug("from {},{} looking at neighbour {},{}".format(r, c, next_row, next_col))
#             if neighbour not in unvisited_nodes:
#                 continue
#             neigh_distance = tentatives[current] + grid[next_row][next_col]
#             if neighbour not in tentatives or tentatives[neighbour] > neigh_distance:
#                 tentatives[neighbour] = neigh_distance
#                 if current_dir == next_d:
#                     current_dir_count += 1
#                 else:
#                     current_dir = next_d
#                     current_dir_count = 1

#         unvisited_nodes.remove(current)
#         if current == (rows - 1, cols - 1):
#             break
#         current = get_closest_tentative(unvisited_nodes, tentatives, path)
#         path.append(current)
#     #logging.debug("Path lengths:")
#     #for r in range(rows):
#     #    for c in range(cols):
#     #        distance = distances[(r,c)]["distance"]
#     #        if distance is None:
#     #            distance = '.'
#     #        print(distance, end='')
#     #    print()
#     return tentatives[current], path

# def get_key_for_min_map_value(m):
#     min_k = None
#     min_v = None
#     for k, v in m.items():
#         if min_v is None or v < min_v:
#             min_k = k
#             min_v = v
#     return min_k, min_v

# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
def dijkstra2(grid):
    rows = len(grid)
    cols = len(grid[0])
    dist = {}
    prev = {}
    unvisited = set()
    for r in range(rows):
        for c in range(cols):
            dist[(r, c)] = 10000000000
            unvisited.add((r, c))
    dist[(0,0)] = 0

    while unvisited:
        closest = None
        min_dist = None
        for u in unvisited:
            if min_dist is None or dist[u] < min_dist:
                min_dist = dist[u]
                closest = u
        unvisited.remove(closest)

        logging.debug("Looking at {} (dist {})".format(closest, min_dist))

        r, c = closest
        for next_row, next_col in [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]:
            if (next_row, next_col) not in unvisited:
                # this also rules out invalid points and the point itself (since we removed it above)
                logging.info("skipping {},{} wasn't in unvisited.")
                continue

            next_dist = min_dist + grid[next_row][next_col]
            if next_dist < dist[(next_row, next_col)]:
                # Check the path so far and make sure it's not too long.
                current_path = get_path(prev, r, c) + [(next_row, next_col)]
                path_so_far = get_dir_string(current_path)
                logging.debug("Path so far to {},{} -> {},{}: {}".format(r, c, next_row, next_col, path_so_far))
                if len(path_so_far) > 3 and len(set(path_so_far[-4:])) == 1:
                    logging.debug("skipping path {} that ends with >3 of the same thing: {}".format(path_so_far, path_so_far[-4:]))
                else:
                    logging.debug("Setting distance {},{} to {}".format(next_row, next_col, next_dist))
                    dist[(next_row, next_col)] = next_dist
                    prev[(next_row, next_col)] = closest
            else:
                logging.debug("Already had a better distance for {},{} ({} < current {})".format(next_row, next_col, dist[(next_row, next_col)], next_dist))
        logging.debug("{} remaining".format(len(unvisited)))
    return dist, prev

def get_path(prev, goal_row, goal_col, start_row=0, start_col=0):
    p = []
    t = (goal_row, goal_col)
    if t in prev or t == (start_row, start_col):
        while t is not None:
            p.insert(0, t)
            # logging.debug("inserting {}".format(t))
            t = prev.get(t)
            # logging.debug("next: {}".format(t))
    return p

dist, prev = dijkstra2(crucibles)
path = get_path(prev, len(crucibles)-1, len(crucibles[0])-1)
# logging.info(prev)
logging.info("Min distance {} with path of {}".format(dist[len(crucibles)-1, len(crucibles[0])-1], path))
path_viz = get_dir_string(path)
logging.info("Path: {}".format(path_viz))
s = 0
for row, col in path:
    s += crucibles[row][col]
    logging.debug("{},{}={} (sum={})".format(row, col, crucibles[row][col], s))

logging.info("total: {}".format(s))

test_path = [
    (0,0),(0,1),(0,2),(1,2),(1,3),(1,4),(1,5),
    (0,5),(0,6),(0,7),(0,8),(1,8),(2,8),(2,9),
    (2,10),(3,10),(4,10),(4,11),(5,11),(6,11),
    (7,11),(7,12),(8,12),(9,12),(10,12),(10,11),
    (11,11),(12,11),(12,12)
]
logging.debug(get_dir_string(test_path))
s = 0
for row, col in test_path:
    s += crucibles[row][col]
    logging.debug("{},{}={} (sum={})".format(row, col, crucibles[row][col], s))

logging.info("test path total: {}".format(s))

# if not TEST:
#     p.answer_a = 10

# logging.info("{},{} to {},{}: {}".format(0,0, 0,1, get_direction((0,0),(0,1))))
# logging.info("{},{} to {},{}: {}".format(0,0, 1,0, get_direction((0,0),(1,0))))
# logging.info("{},{} to {},{}: {}".format(1,0, 0,0, get_direction((1,0),(0,0))))
# logging.info("{},{} to {},{}: {}".format(0,1, 0,0, get_direction((0,1),(0,0))))


# 2413432311323
# 3215453535623
# 3255245654254
# 3446585845452
# 4546657867536
# 1438598798454
# 4457876987766
# 3637877979653
# 4654967986887
# 4564679986453
# 1224686865563
# 2546548887735
# 4322674655533

# 2>>34^>>>1323
# 32v>>>35v5623
# 32552456v>>54
# 3446585845v52
# 4546657867v>6
# 14385987984v4
# 44578769877v6
# 36378779796v>
# 465496798688v
# 456467998645v
# 12246868655<v
# 25465488877v5
# 43226746555v>
