from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2022, day=17)

TEST = False
PART_ONE = False

if TEST:
  lines = [">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"]
else:
  lines = p.input_data.splitlines()

angles = list(lines[0])
moves = []
for a in angles:
  if a == '>':
    moves.append(1)
  elif a == '<':
    moves.append(-1)
  else:
    logging.warning(f"Unexpected move: {a}")

logging.info(f"Found {len(moves)} moves")

# y = 0 is a the bottom, and increases as we move up
shapes = [
[(0,0), (1,0), (2,0), (3,0)], # shape -

[       (1,2),
 (0,1), (1,1), (2,1),
        (1,0)],               # shape +

[              (2,2),
               (2,1),
 (0,0), (1,0), (2,0)],        # shape L

[(0,3),
 (0,2),
 (0,1),
 (0,0)],                      # shape I

[(0,1), (1,1),
 (0,0), (1,0)],               # shape o

]

CAVE_WIDTH = 7

def print_cave(cave, max_height):
  for h in range(max_height, 0, -1):
    for x in range(CAVE_WIDTH):
      v = '.'
      if (x,h) in cave:
        v = cave[(x,h)]
      print(v, end='')
    print('')
  print('-' * CAVE_WIDTH)

def get_modulo(short_list, long_number):
  return short_list[long_number % len(short_list)]

def blocked_bottom(cave, shape_index, x, y):
  shape = get_modulo(shapes, shape_index)
  bottom = None
  if shape_index % 5 == 0:
    bottom = shape
  elif shape_index % 5 == 1:
    bottom = [shape[1], shape[3], shape[4]]
  elif shape_index % 5 == 2:
    bottom = shape[2:]
  elif shape_index % 5 == 3:
    bottom = shape[-1:]
  elif shape_index % 5 == 4:
    bottom = shape[-2:]

  for bx, by in bottom:
    # If a rock exists directly below this point, we're blocked.
    logging.debug(f"Checking if bottom {bx},{by} is blocked relative to {x},{y}")
    next_y = by + y - 1
    if next_y == 0 or (bx+x, next_y) in cave:
      return True
  return False

def blocked_right(cave, shape_index, x, y):
  shape = get_modulo(shapes, shape_index)
  right = None
  if shape_index % 5 == 0:
    right = shape[-1:]
  elif shape_index % 5 == 1:
    right = [shape[0], shape[3], shape[4]]
  elif shape_index % 5 == 2:
    right = [shape[0], shape[1], shape[4]]
  elif shape_index % 5 == 3:
    right = shape
  elif shape_index % 5 == 4:
    right = [shape[1], shape[3]]

  for bx, by in right:
    # If a rock exists directly to the right of this point, we're blocked.
    logging.debug(f"Checking if right {bx},{by} is blocked relative to {x},{y}")
    next_x = bx + x + 1
    if next_x >= CAVE_WIDTH or (next_x, by+y) in cave:
      return True
  return False

def blocked_left(cave, shape_index, x, y):
  shape = get_modulo(shapes, shape_index)
  left = None
  if shape_index % 5 == 0:
    left = shape[:1]
  elif shape_index % 5 == 1:
    left = [shape[0], shape[1], shape[4]]
  elif shape_index % 5 == 2:
    left = [shape[0], shape[1], shape[2]]
  elif shape_index % 5 == 3:
    left = shape
  elif shape_index % 5 == 4:
    left = [shape[0], shape[2]]

  for bx, by in left:
    # If a rock exists directly to the left of this point, we're blocked.
    logging.debug(f"Checking if left {bx},{by} is blocked relative to {x},{y}")
    next_x = bx + x - 1
    if next_x < 0 or (next_x, by+y) in cave:
      return True
  return False

def apply_move(move, cave, shape_index, x, y):
  moved = x + move
  if moved < 0:
    return 0
  if moved >= CAVE_WIDTH:
    return x
  if move > 0 and blocked_right(cave, shape_index, x, y):
    return x
  if move < 0 and blocked_left(cave, shape_index, x, y):
    return x
  return moved

def get_top_layer(cave, max_height):
  top = [None] * CAVE_WIDTH
  top_count = 0
  for layer in range(max_height, -1, -1):
    logging.debug(f"Looking for tops in layer {layer}")
    for x in range(CAVE_WIDTH):
      if (x, layer) in cave:
        if top[x] is None:
          top_count += 1
          top[x] = layer- max_height
          if top_count == CAVE_WIDTH:
            break
    if top_count == CAVE_WIDTH:
      break

  for i in range(CAVE_WIDTH):
    if top[i] is None:
      top[i] = -1
  return ",".join([str(i) for i in top])

if TEST:
  foo = {}
  foo[(0,0)] = '#'
  foo[(1,0)] = '#'
  foo[(2,0)] = '#'
  foo[(3,5)] = '#'
  foo[(4,0)] = '#'
  foo[(5,0)] = '#'
  foo[(6,0)] = '#'

  tops = get_top_layer(foo, 5)
  logging.info(f"Top layer was {tops}")

  foo[(5,1)] = '#'
  foo[(6,2)] = '#'
  foo[(6,11)] = '#'

  tops = get_top_layer(foo, 5)
  logging.info(f"Top layer was {tops}")

cave = {}
max_height = 0
move_index = 0
shape_index = 0
rock_count = 0

print_cave(cave, max_height)

if PART_ONE:
  num_rocks = 2022
else:
  num_rocks = 1000000000000

memo = {}

while rock_count < num_rocks:
  # Look for a "top layer" we've seen before with a shape_index and move_index we've also seen.
  si = shape_index % len(shapes)
  mi = move_index % len(moves)
  top_layer = get_top_layer(cave, max_height)
  if (si, mi, top_layer) in memo:
   last_rock_count, last_height = memo[(si, mi, top_layer)]

   # one cycle like this adds
   rocks_added = rock_count - last_rock_count
   height_added = max_height - last_height
   logging.info(f"Saw a repeat: shape {si}, move {mi}, top {top_layer}. Last time rock count was {last_rock_count}, height was {last_height}. This time rock count is {rock_count} and height is {max_height}. Added {rocks_added} rocks and {height_added} height.")

   # determine how many more rocks are left
   rocks_left = num_rocks - rock_count

   # get pretty close
   multiplier = rocks_left // rocks_added
   rock_count += multiplier * rocks_added
   max_height += multiplier * height_added
   # reapply the top layer
   logging.info(f"Reapplying top layer {top_layer}")
   top_layer_ys = [int(s) for s in top_layer.split(',')]
   for tlx, tly in enumerate(top_layer_ys):
    logging.info(f"Reapplying top layer {tlx},{max_height + tly}")
    cave[(tlx, max_height + tly)] = '#'
  else:
   memo[(si, mi, top_layer)] = (rock_count, max_height)

  logging.info(f"After {rock_count} rocks, max height was {max_height}. Shape: {si}, Move: {mi}, Top: {top_layer}")
  shape = get_modulo(shapes, shape_index)
  x, y = (2, max_height + 3 + 1)
  while True:
    # First, move
    move = get_modulo(moves, move_index)
    logging.debug(f"Applying move {move} to {x}")
    move_index += 1
    x = apply_move(move, cave, shape_index, x, y)

    # Then, fall
    logging.debug(f"Falling from {y} to {y - 1}")
    if blocked_bottom(cave, shape_index, x, y):
      break
    else:
      y -= 1

  for rx, ry in shape:
    cave[(x + rx, y + ry)] = '#'
    if y + ry > max_height:
      max_height = y + ry
  rock_count += 1
  # print_cave(cave, max_height)

  shape_index += 1

logging.info(f"After {num_rocks}, max height was {max_height}")
# p.answer_a = 10
