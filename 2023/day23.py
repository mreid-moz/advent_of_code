from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=23)

TEST = True
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

def dijkstra(grid, start_row=0, start_col=0):
    rows = len(grid)
    cols = len(grid[0])
    dist = {}
    prev = {}
    unvisited = set()
    for r in range(rows):
        for c in range(cols):
            dist[(r, c)] = -1
            if grid[r][c] != '#':
                unvisited.add((r, c))
    dist[(start_row,start_col)] = 0

    while unvisited:
        furthest = None
        max_dist = None
        for u in unvisited:
            if max_dist is None or dist[u] > max_dist:
                max_dist = dist[u]
                furthest = u
        unvisited.remove(furthest)

        logging.debug("Looking at {} (dist {})".format(furthest, max_dist))

        r, c = furthest
        for next_row, next_col, next_dir in [(r-1, c, '^'), (r+1, c, 'v'), (r, c-1, '<'), (r, c+1, '>')]:
            if (next_row, next_col) not in unvisited:
                # this also rules out invalid points and the point itself (since we removed it above)
                # logging.debug("skipping {},{} wasn't in unvisited.".format(next_row, next_col))
                continue

            if grid[next_row][next_col] != '.' and grid[next_row][next_col] != next_dir:
                logging.debug("Skipping {},{}, since it was {} and the slope was {}".format(next_row, next_col, next_dir, grid[next_row][next_col]))
                continue

            logging.debug("Looking from {},{} {} {},{}".format(r, c, next_dir, next_row, next_col))
            next_dist = max_dist + 1
            if next_dist > dist[(next_row, next_col)]:
                logging.debug("Setting distance {},{} to {}".format(next_row, next_col, next_dist))
                dist[(next_row, next_col)] = next_dist
                prev[(next_row, next_col)] = furthest
            else:
                logging.debug("Already had a better distance for {},{} ({} > current {})".format(next_row, next_col, dist[(next_row, next_col)], next_dist))
        logging.debug("{} remaining".format(len(unvisited)))
    return dist, prev


start_col = lines[0].find('.')
distances, paths = dijkstra(lines, 0, start_col)
end_col = lines[-1].find('.')
longest_dist = distances[(len(lines)-1, end_col)]
logging.info("Longest path from 0,{} to {},{}: {}".format(start_col, len(lines) - 1, end_col, longest_dist))

if not TEST:
    p.answer_a = longest_dist
