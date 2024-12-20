from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2024, day=20)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

def get_closest_tentative(unvisited, distances):
    candidate = None
    candidate_path = []
    for k, v in distances.items():
        if k in unvisited:
            if candidate is None or len(v) < len(candidate_path):
                candidate = k
                candidate_path = v
    return candidate

def dijkstra(grid, start, end):
    tentatives = {}
    unvisited_nodes = set()
    for x, y in grid.keys():
        if grid[(x, y)] != '#':
            unvisited_nodes.add((x, y))

    current = start
    tentatives[current] = [current]
    while unvisited_nodes:
        if current not in tentatives:
            return None
        (x, y) = current
        for next_x, next_y in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
            neighbour = (next_x, next_y)
            if neighbour not in unvisited_nodes:
                continue
            new_path = tentatives[current] + [neighbour]

            neigh_distance = len(new_path)
            if neighbour not in tentatives or neigh_distance < len(tentatives[neighbour]):
                tentatives[neighbour] = new_path

        unvisited_nodes.remove(current)
        if (x, y) == end:
            logging.debug(f"Found E at {current}")
            break
        current = get_closest_tentative(unvisited_nodes, tentatives)
    return tentatives.get(end, None)

racetrack = {}
start = None
end = None
max_x = len(lines[0])
max_y = len(lines)
for x in range(max_x):
    for y in range(max_y):
        c = lines[y][x]
        racetrack[(x, y)] = c
        if c == 'S':
            start = (x, y)
        elif c == 'E':
            end = (x, y)


shortest = dijkstra(racetrack, start, end)

logging.info(f"Shortest path was {len(shortest)} long: {shortest}")

hundreds_saved = 0
for i, (x, y) in enumerate(shortest):
    remainder = shortest[i+1:]
    # logging.info(f"Cheating starting from: {x},{y}")
    for next_x, next_y in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
        if (next_x, next_y) not in shortest: # good, hit a wall
            if next_x < 0 or next_x >= max_x:
                continue
            if next_y < 0 or next_y >= max_y:
                continue
        for nn_x, nn_y in [(next_x-1,next_y), (next_x+1,next_y), (next_x,next_y-1), (next_x,next_y+1)]:
            if (nn_x, nn_y) in remainder:
                # back on track!
                distance_saved = remainder.index((nn_x, nn_y)) - 1
                if distance_saved > 0:
                    # logging.debug(f"Saved {distance_saved} by cheating from {x},{y} at {next_x},{next_y} and {nn_x},{nn_y}")
                    if distance_saved >= 100:
                        hundreds_saved += 1

logging.info(f"Found {hundreds_saved} cheats that saved at least 100 picos")
if not TEST:
    p.answer_a = hundreds_saved

def distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)

how_many = defaultdict(int)
cheat_counter = 0
cheat_target = 100
if TEST:
    cheat_target = 50
for i1 in range(len(shortest) - cheat_target + 1):
    for i2 in range(i1 + cheat_target - 1, len(shortest)):
        x1, y1 = shortest[i1]
        x2, y2 = shortest[i2]
        cheat_distance = distance(x1, y1, x2, y2)
        if cheat_distance <= 20:
            d = i2 - i1 - cheat_distance
            if d >= cheat_target:
                how_many[d] += 1
                # logging.debug(f"Found an effective cheat of length {d} from {i1}={x1},{y1} to {i2}={x2},{y2}")
                cheat_counter += 1

# for k, v in how_many.items():
#     logging.debug(f"Found {v} cheats of length {k}")

logging.info(f"Found {cheat_counter} cheats of at least {cheat_target}")
if not TEST:
    p.answer_b = cheat_counter

