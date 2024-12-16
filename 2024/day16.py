from aocd.models import Puzzle
from collections import defaultdict
from functools import cache
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2024, day=16)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

def get_next_dir(r1, c1, r2, c2):
    if r1 > r2:
        return '^'
    if r1 < r2:
        return 'v'
    if c1 > c2:
        return '<'
    if c1 < c2:
        return '>'
    return None

@cache
def path_score(path):
    score = 0
    current = '>'
    for pi in path[1:]:
        if pi != current and pi != 'E':
            score += 1000
        current = pi
    score += len(path) - 1
    return score

def get_closest_tentative(unvisited, distances):
    candidate = None
    candidate_path = []
    for k, v in distances.items():
        if k in unvisited:
            if candidate is None or path_score(v) < path_score(candidate_path):
                candidate = k
                candidate_path = v
    return candidate

def dijkstra(grid):
    tentatives = {}
    unvisited_nodes = set()
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '#':
                unvisited_nodes.add((r,c))

    r, c = (rows-2,1)
    current = (r, c)
    if grid[r][c] != 'S':
        logging.error(f"grid[{r},{c}] == {grid[r][c]} (expected S)")
    tentatives[current] = '>'
    while unvisited_nodes:
        r, c = current
        for next_row, next_col in [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]:
            if next_row < 0 or next_row >= rows:
                continue
            if next_col < 0 or next_col >= cols:
                continue

            next_dir = get_next_dir(r, c, next_row, next_col)

            neighbour = (next_row, next_col)
            # logging.debug("from {},{} looking at neighbour {},{}".format(r, c, next_row, next_col))
            if neighbour not in unvisited_nodes:
                continue
            new_path = tentatives[current] + next_dir

            neigh_distance = path_score(new_path)
            if neighbour not in tentatives or path_score(tentatives[neighbour]) > neigh_distance:
                tentatives[neighbour] = new_path

        unvisited_nodes.remove(current)
        if grid[r][c] == 'E':
            logging.debug(f"Found E at {current}")
            # if current == (rows - 1, cols - 1):
            break
        current = get_closest_tentative(unvisited_nodes, tentatives)
    return tentatives[current]

# for line in lines:
#     logging.debug(line)

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#^#
#.#.#.#...#...#^#
#.#.#.#.###.#.#^#
#>>v#.#.#.....#^#
#^#v#.#.#.#####^#
#^#v..#.#.#>>>>^#
#^#v#####.#^###.#
#^#v#..>>>>^#...#
#^#v###^#####.###
#^#v#>>^#.....#.#
#^#v#^#####.###.#
#^#v#^........#.#
#^#v#^#########.#
#S#>>^..........#
#################
test_path = "S^^^^^^^^^>>vvvvvvvvvv>>^^^^>>^^>>>>^^>>>>^^^^^^E"
logging.debug(f"Score for {test_path}: {path_score(test_path)}")

###############
#.......#....E#
#.#.###.#.###^#
#.....#.#...#^#
#.###.#####.#^#
#.#.#.......#^#
#.#.#####.###^#
#..>>>>>>>>v#^#
###^#.#####v#^#
#>>^#.....#v#^#
#^#.#.###.#v#^#
#^....#...#v#^#
#^###.#.#.#v#^#
#S..#.....#>>^#
###############
test_path = "S^^^>>^^>>>>>>>>vvvvvv>>^^^^^^^^^^^^E"
logging.debug(f"Score for {test_path}: {path_score(test_path)}")

shortest = dijkstra(lines)
shortest_score = path_score(shortest)
logging.info(f"Shortest path: {shortest} for score {shortest_score}")

if not TEST:
    p.answer_a = shortest_score
