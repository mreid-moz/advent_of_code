from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2024, day=18)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
    num_bytes = 12
    max_size = 6+1
else:
    lines = p.input_data.splitlines()
    num_bytes = 1024
    max_size = 70+1

def get_closest_tentative(unvisited, distances):
    candidate = None
    candidate_path = []
    for k, v in distances.items():
        if k in unvisited:
            if candidate is None or len(v[0]) < len(candidate_path[0]):
                candidate = k
                candidate_path = v
    return candidate

def dijkstra(grid):
    tentatives = {}
    unvisited_nodes = set()
    for x in range(max_size):
        for y in range(max_size):
            if grid.get((x, y), None) != '#':
                unvisited_nodes.add((x, y))

    current = (0, 0)
    tentatives[current] = [[current]]
    while unvisited_nodes:
        if current not in tentatives:
            return None
        # logging.debug(f"curent is {current}, path so far is {tentatives.get(current, [[(-1,-1)]])[0]}")
        (x, y) = current
        for next_x, next_y in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
            if next_x < 0 or next_x >= max_size:
                continue
            if next_y < 0 or next_y >= max_size:
                continue

            neighbour = (next_x, next_y)
            if neighbour not in unvisited_nodes:
                continue
            new_path = tentatives[current][0] + [neighbour]

            neigh_distance = len(new_path)
            if neighbour not in tentatives or neigh_distance < len(tentatives[neighbour][0]):
                tentatives[neighbour] = [new_path]

        unvisited_nodes.remove(current)
        if (x, y) == (max_size-1,max_size-1):
            logging.debug(f"Found E at {current}")
            break
        current = get_closest_tentative(unvisited_nodes, tentatives)
    return tentatives.get((max_size-1,max_size-1), None)


points = [(int(a), int(b)) for a, b in [line.split(',') for line in lines[0:num_bytes]]]
logging.info(f"Found {len(points)} points")
memory_space = {}
for point in points:
    memory_space[point] = '#'

shortest = dijkstra(memory_space)
logging.info(f"Shortest was {len(shortest[0]) - 1}")
if not TEST:
    p.answer_a = len(shortest[0]) - 1

more_points = [(int(a), int(b)) for a, b in [line.split(',') for line in lines[num_bytes:]]]
current_shortest = set(shortest[0])
for mp in more_points:
    memory_space[mp] = '#'
    if mp not in current_shortest:
        logging.debug(f"Don't care about {mp} because it wasn't on our path")
    else:
        # update the path
        logging.debug(f"Path contained {mp}, recalculating...")
        new_shortest = dijkstra(memory_space)
        if new_shortest is None:
            logging.info(f"The answer is {mp}")
            if not TEST:
                x, y = mp
                p.answer_b = f"{x},{y}"
            break
        else:
            current_shortest = set(new_shortest[0])
