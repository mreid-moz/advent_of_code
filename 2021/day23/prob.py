import logging
import re
import sys
from collections import defaultdict
import copy

logging.basicConfig(level=logging.DEBUG)

# Start:
# #############
# #...........#
# ###B#A#A#D###
#   #D#C#B#C#
#   #########

# #############
# #.........D.#  2000
# ###B#A#A#.###
#   #D#C#B#C#
#   #########

# #############
# #A........D.#  2000 + 5
# ###B#.#A#.###
#   #D#C#B#C#
#   #########

# #############
# #AA.......D.#  2000 + 5 + 6
# ###B#.#.#.###
#   #D#C#B#C#
#   #########

# #############
# #AA.B.....D.#  2000 + 5 + 6 + 50
# ###B#.#.#.###
#   #D#C#.#C#
#   #########

# #############
# #AA.B.....D.#  2000 + 5 + 6 + 50 + 600
# ###B#.#.#.###
#   #D#.#C#C#
#   #########

# #############
# #AA.B.....D.#  2000 + 5 + 6 + 50 + 600 + 500
# ###B#.#C#.###
#   #D#.#C#.#
#   #########

# #############
# #AA.B.......#  2000 + 5 + 6 + 50 + 600 + 500 + 3000
# ###B#.#C#.###
#   #D#.#C#D#
#   #########

# #############
# #AA.........#  2000 + 5 + 6 + 50 + 600 + 500 + 3000 + 30
# ###B#.#C#.###
#   #D#B#C#D#
#   #########

# #############
# #AA.........#  2000 + 5 + 6 + 50 + 600 + 500 + 3000 + 30 + 40
# ###.#B#C#.###
#   #D#B#C#D#
#   #########

# #############
# #AA.........#  2000 + 5 + 6 + 50 + 600 + 500 + 3000 + 30 + 40 + 9000
# ###.#B#C#D###
#   #.#B#C#D#
#   #########

# #############
# #A..........#  2000 + 5 + 6 + 50 + 600 + 500 + 3000 + 30 + 40 + 9000 + 3
# ###.#B#C#D###
#   #A#B#C#D#
#   #########

# #############
# #...........#  2000 + 5 + 6 + 50 + 600 + 500 + 3000 + 30 + 40 + 9000 + 3 + 3
# ###A#B#C#D###
#   #A#B#C#D#
#   #########

# Total = 2000 + 5 + 6 + 50 + 600 + 500 + 3000 + 30 + 40 + 9000 + 3 + 3 = 15237

logging.info("Part 1 Total energy: 15237")

def print_burrow(b):
  print("#############")
  print(''.join(['#'] + b['r'] + ['#']))
  for i in range(4):
    if i == 0:
      print('###', end='')
    else:
      print('  #', end='')
    print('#'.join([b['h1'][i], b['h2'][i], b['h3'][i], b['h4'][i]]), end='')
    if i == 0:
      print('###')
    else:
      print('#  ')
  print('  #########')

def get_distance(k1, o1, k2, o2):
  distance = 0
  if k1 == 'r':
    h1_offset = 0
    r1_offset = o1
  else:
    h1_offset = o1 + 1
    r1_offset = 2 # top of h1
    if k1 == 'h2':
      r1_offset = 4
    elif k1 == 'h3':
      r1_offset = 6
    elif k1 == 'h4':
      r1_offset = 8

  if k2 == 'r':
    h2_offset = 0
    r2_offset = o2
  else:
    h2_offset = o2 + 1
    r2_offset = 2 # top of h1
    if k2 == 'h2':
      r2_offset = 4
    elif k2 == 'h3':
      r2_offset = 6
    elif k2 == 'h4':
      r2_offset = 8

  distance = h1_offset + abs(r2_offset - r1_offset) + h2_offset
  return distance


def move(burrow, key1, offset1, key2, offset2):
  logging.debug(f"Moving {key1}[{offset1}] ({burrow[key1][offset1]}) to {key2}[{offset2}] ({burrow[key2][offset2]})")
  if burrow[key1][offset1] == '.' or burrow[key2][offset2] != '.':
    logging.error("Illegal move.")

  move_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}[burrow[key1][offset1]]
  burrow[key2][offset2] = burrow[key1][offset1]
  burrow[key1][offset1] = '.'
  # return cost of this move.
  move_distance = get_distance(key1, offset1, key2, offset2)
  energy = move_cost * move_distance
  logging.debug(f"Distance from {k1}[{o1}] to {k2}[{o2}]: {move_distance} spaces * {move_cost} per space = {energy}")
  return energy

moves = [
 [('h4', 0), ('r', 10)],
 [('h4', 1), ('r',  9)],
 [('h3', 0), ('r',  0)],
 [('h3', 1), ('r',  1)],
 [('h3', 2), ('r',  3)],
 [('h3', 3), ('r',  5)],
 [('h4', 2), ('h3', 3)],
 [('h4', 3), ('h3', 2)],
 # stuck :(
]

moves = [
 [('h3', 0), ('r',  0)],
 [('h3', 1), ('r',  10)],
 [('h3', 2), ('r',  9)],
 [('h3', 3), ('r',  7)],
 [('h2', 0), ('r',  1)],
 [('h2', 1), ('h3', 3)],
 [('h2', 2), ('r',  3)],
 [('h2', 3), ('h3', 2)],
 [('r',  3), ('h2', 3)],
 [('h1', 0), ('h2', 2)],
 [('r',  7), ('h2', 1)],
 # stuck
]

moves = [
 [('h3', 0), ('r',  10)],
 [('h3', 1), ('r',  9)],
 [('h3', 2), ('r',  0)],
 [('h3', 3), ('r',  7)],
 [('h2', 0), ('r',  1)],
 [('h2', 1), ('h3', 3)],
 [('h2', 2), ('r',  3)],
 [('h2', 3), ('h3', 2)],
 [('r',  3), ('h2', 3)],
 [('h1', 0), ('h2', 2)],
 [('r',  7), ('h2', 1)],
 [('r',  9), ('h2', 0)],
 [('h4', 0), ('r',  5)],
 [('h4', 1), ('r',  9)],
 [('h4', 2), ('h3', 1)],
 [('h4', 3), ('h3', 0)],
 [('r',  5), ('h4', 3)],
 [('h1', 1), ('h4', 2)],
 [('h1', 2), ('h4', 1)],
 [('h1', 3), ('h4', 0)],
 [('r',  1), ('h1', 3)],
 [('r',  0), ('h1', 2)],
 [('r',  9), ('h1', 1)],
 [('r', 10), ('h1', 0)],
]

# Start:
# #############
# #...........#
# ###B#A#A#D###
#   #D#C#B#A#
#   #D#B#A#C#
#   #D#C#B#C#
#   #########

my_burrow = {
  'h1': ['B','D','D','D'],
  'h2': ['A','C','B','C'],
  'h3': ['A','B','A','B'],
  'h4': ['D','A','C','C'],
  'r': ['.','.','.','.','.','.','.','.','.','.','.']
}
print("Start:")
print_burrow(my_burrow)
total_cost = 0
for m in moves:
  (k1, o1), (k2, o2) = m
  total_cost += move(my_burrow, k1, o1, k2, o2)
  print_burrow(my_burrow)

logging.info(f"Total cost was {total_cost}")
