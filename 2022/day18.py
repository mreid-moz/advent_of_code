from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

# Ugh.
sys.setrecursionlimit(50000)

p = Puzzle(year=2022, day=18)

PART_ONE = False
TEST = False

if TEST:
  lines = [
    "2,2,2",
    "1,2,2",
    "3,2,2",
    "2,1,2",
    "2,3,2",
    "2,2,1",
    "2,2,3",
    "2,2,4",
    "2,2,6",
    "1,2,5",
    "3,2,5",
    "2,1,5",
    "2,3,5",
  ]
else:
  lines = p.input_data.splitlines()

class Cube:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def __str__(self):
    return f"{self.x},{self.y},{self.z}"

def neighbours(c1, c2):
  if abs(c1.x - c2.x) == 1 and c1.y == c2.y and c1.z == c2.z:
    return True
  if c1.x == c2.x and abs(c1.y - c2.y) == 1 and c1.z == c2.z:
    return True
  if c1.x == c2.x and c1.y == c2.y and abs(c1.z - c2.z) == 1:
    return True

def count_inside_faces(c):
  insides = 0
  x, y, z = (c.x, c.y, c.z)
  for (nx, ny, nz) in [(x-1, y, z), (x+1, y, z),
                       (x, y-1, z), (x, y+1, z),
                       (x, y, z-1), (x, y, z+1)]:
    if (nx, ny, nz) not in cube_map:
      insides += 1
  return insides

def flood_fill(x, y, z):
  if (x, y, z) in cube_map:
    return
  logging.debug(f"Flood filling {(x, y, z)}")

  cube_map[(x, y, z)] = None

  if x - 1 >= min_x:
    flood_fill(x - 1, y, z)
  if x + 1 <= max_x:
    flood_fill(x + 1, y, z)

  if y - 1 >= min_y:
    flood_fill(x, y - 1, z)
  if y + 1 <= max_y:
    flood_fill(x, y + 1, z)

  if z - 1 >= min_z:
    flood_fill(x, y, z - 1)
  if z + 1 <= max_z:
    flood_fill(x, y, z + 1)

cubes = []
cube_map = {}

for line in lines:
  x, y, z = [int(n) for n in line.split(',')]
  cube = Cube(x, y, z)
  cubes.append(cube)
  cube_map[(x,y,z)] = cube

min_x, min_y, min_z = cubes[0].x, cubes[0].y, cubes[0].z
max_x, max_y, max_z = cubes[0].x, cubes[0].y, cubes[0].z

for cube in cubes[1:]:
  if cube.x < min_x:
    min_x = cube.x
  if cube.y < min_y:
    min_y = cube.y
  if cube.z < min_z:
    min_z = cube.z

  if cube.x > max_x:
    max_x = cube.x
  if cube.y > max_y:
    max_y = cube.y
  if cube.z > max_z:
    max_z = cube.z

logging.debug(f"Extent: {(min_x, min_y, min_z)} to {(max_x, max_y, max_z)}")
min_x -= 1
min_y -= 1
min_z -= 1
max_x += 1
max_y += 1
max_z += 1
logging.debug(f"Grown Extent: {(min_x, min_y, min_z)} to {(max_x, max_y, max_z)}")

if not PART_ONE:
  flood_fill(min_x, min_y, min_z)

# Shrink the extents back
min_x += 1
min_y += 1
min_z += 1
max_x -= 1
max_y -= 1
max_z -= 1

surface_area = 6 * len(cubes)
logging.info(f"Found {len(cubes)} cubes. Max possible surface area is {surface_area}.")
for a, cube in enumerate(cubes):
  cube_faces = 6
  for b, other_cube in enumerate(cubes):
    if a == b:
      continue
    if neighbours(cube, other_cube):
      surface_area -= 1
      cube_faces -= 1
      logging.debug(f"Cube {a} {(cube.x,cube.y,cube.z)} neighbours {b} {(other_cube.x,other_cube.y,other_cube.z)}, now has {cube_faces} exposed.")

  if not PART_ONE:
    # consider inside faces
    insides = count_inside_faces(cube)
    if insides > 0:
      logging.debug(f"Cube {cube} had {insides} inside faces. Don't count those.")
      surface_area -= insides

logging.info(f"Surface area: {surface_area}.")

if not TEST:
  if PART_ONE:
    p.answer_a = surface_area
  else:
    p.answer_b = surface_area
