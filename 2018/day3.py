from aocd.models import Puzzle
from collections import defaultdict
import re

pattern = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")

p = Puzzle(year=2018, day=3)

lines = p.input_data.splitlines()

grid = []

for i in range(1000):
  grid.append([0]*1000)

for line in lines:
  m = pattern.match(line)
  if m is None:
    print(f"wonky input: {line}")
    break
  left = int(m.group(2))
  top = int(m.group(3))
  width = int(m.group(4))
  height = int(m.group(5))

  for w in range(width):
    for h in range(height):
      grid[w+left][h+top] += 1

multi_claims = 0
for i in range(len(grid)):
  for j in range(len(grid[0])):
    if grid[i][j] > 1:
      multi_claims += 1

p.answer_a = multi_claims

grid = []

for i in range(1000):
  grid.append([None]*1000)

# Part B
non_overlapping_codes = set()
for line in lines:
  m = pattern.match(line)
  if m is None:
    print(f"wonky input: {line}")
    break
  code = int(m.group(1))
  left = int(m.group(2))
  top = int(m.group(3))
  width = int(m.group(4))
  height = int(m.group(5))

  overlapping = False
  for w in range(width):
    for h in range(height):
      current = grid[w+left][h+top]
      if current is None:
        grid[w+left][h+top] = code
      else:
        overlapping = True
        if current in non_overlapping_codes:
          non_overlapping_codes.remove(current)
  if not overlapping:
    non_overlapping_codes.add(code)

if len(non_overlapping_codes) == 1:
  p.answer_b = non_overlapping_codes.pop()
else:
  print(f"Found {len(non_overlapping_codes)} non-overlapping codes")
