import logging
import copy
import re
import sys
from collections import defaultdict

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [[int(x) for x in list(l.strip())] for l in fin.readlines()]

rows = len(my_input)
cols = len(my_input[0])

min_score = None
min_score_path = None
total_path_count = 0

def get_closest_tentative(unvisited, distances):
  candidate = None
  for node in unvisited:
    distance = distances[node]["distance"]
    if distance is not None:
      if candidate is None or distance < distances[candidate]["distance"]:
        candidate = node
  return candidate

def dijkstra(grid):
  distances = {}
  unvisited_nodes = set()
  for r in range(rows):
    for c in range(cols):
      distances[(r,c)] = {"distance": None, "tentative": True}
      unvisited_nodes.add((r,c))

  distances[(0,0)] = {"distance": 0, "tentative": False}

  current = (0,0)
  while unvisited_nodes:
    r, c = current
    for next_row, next_col in [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]:
      if next_row < 0 or next_row >= rows:
        continue
      if next_col < 0 or next_col >= cols:
        continue

      neighbour = (next_row, next_col)
      if neighbour not in unvisited_nodes:
        continue
      neigh_distance = distances[current]["distance"] + grid[next_row][next_col]
      if distances[neighbour]["distance"] is None or distances[neighbour]["distance"] > neigh_distance:
        distances[neighbour]["distance"] = neigh_distance

    distances[current]["tentative"] = False
    unvisited_nodes.remove(current)
    if current == (rows - 1, cols - 1):
      break
    current = get_closest_tentative(unvisited_nodes, distances)

  #logging.debug("Path lengths:")
  #for r in range(rows):
  #  for c in range(cols):
  #    distance = distances[(r,c)]["distance"]
  #    if distance is None:
  #      distance = '.'
  #    print(distance, end='')
  #  print()
  return distances[current]["distance"]

min_distance = dijkstra(my_input)
logging.info("Found a min distance of {}".format(min_distance))


