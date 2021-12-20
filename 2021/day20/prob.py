import logging
import re
import sys
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

algo = [1 if c == '#' else 0 for c in my_input[0]]

FIELD_VALUE = 0

def get_field_value():
  #logging.debug(f"Getting default value for field of {FIELD_VALUE}")
  return FIELD_VALUE

def get_new_image():
  return defaultdict(get_field_value)

image = get_new_image()

for r in range(len(my_input) - 2):
  for c in range(len(my_input[2])):
    pixel = my_input[r+2][c]
    if pixel == '#':
      image[(r, c)] = 1
    else:
      image[(r, c)] = 0

def get_coords(image):
  min_row = 0
  max_row = 0
  min_col = 0
  max_col = 0
  for (r, c), v in image.items():
    if v:
      if r < min_row:
        min_row = r
      if c < min_col:
        min_col = c
      if r > max_row:
        max_row = r
      if c > max_col:
        max_col = c
  return (min_row, max_row, min_col, max_col)

def get_bits(image, row, col):
  return [
   image[(row-1,col-1)], image[(row-1,col)], image[(row-1,col+1)],
   image[(row  ,col-1)], image[(row  ,col)], image[(row  ,col+1)],
   image[(row+1,col-1)], image[(row+1,col)], image[(row+1,col+1)],
  ]

def bits2num(bits):
  return int(''.join([str(b) for b in bits]), 2)

def enhance(image, algo, coords):
  global FIELD_VALUE

  min_row, max_row, min_col, max_col = coords

  # expand the image past the maxes
  min_row -= 4
  max_row += 4
  min_col -= 4
  max_col += 4

  new_image = get_new_image()

  # check if we need to flip the field
  left_field = bits2num([FIELD_VALUE] * 9)
  new_field_value = algo[left_field]
  if algo[left_field] != FIELD_VALUE:
    logging.debug(f"Testing that {image[(min_row-10,min_col-10)]} should be the field value of {FIELD_VALUE}")
    logging.debug(f"Flipping field value from {FIELD_VALUE} to {new_field_value}")
    FIELD_VALUE = new_field_value
    logging.debug(f"Testing that {image[(min_row-10,min_col-10)]} should be the field value of {FIELD_VALUE}")

  for r in range(min_row, max_row + 1):
    for c in range(min_col, max_col + 1):
      bits = get_bits(image, r, c)
      idx = bits2num(bits)
      new_image[(r, c)] = algo[idx]
  return new_image, (min_row, max_row, min_col, max_col)

def count_ones(image):
  for (r, c), v in image.items():
    if v:
      logging.debug(f"Lit bit at {r},{c}")
  return sum(image.values())

def print_image(image):
  min_row, max_row, min_col, max_col = get_coords(image)
  for r in range(min_row - 2, max_row + 2 + 1):
    for c in range(min_col - 2, max_col + 2 + 1):
      if r == min_row - 2 and c == 0:
        print('0', end='')
      elif r == 0 and c == min_col - 2:
        print('0', end='')
      elif r == min_row - 2 or r == max_row + 2 or c == min_col - 2 or c == max_col + 2:
        print('.', end='')
      else:
        print('#' if image[(r, c)] else ' ', end='')
    print()

logging.debug("initial image:")
print_image(image)
count_ones(image)
coords = get_coords(image)

for i in range(2):
  image, coords = enhance(image, algo, coords)
  logging.debug(f"After {i+1} enhancements:")
  print_image(image)
logging.info(f"After enhancing twice, found {count_ones(image)} lit bits.")