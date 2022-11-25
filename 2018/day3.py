from aocd.models import Puzzle
from collections import defaultdict
import re

pattern = re.compile(r"#\d+ @ (\d+),(\d+): (\d+)x(\d+)")

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
  left = int(m.group(1))
  top = int(m.group(2))
  width = int(m.group(3))
  height = int(m.group(4))

  for w in range(width):
    for h in range(height):
      grid[w+left][h+top] += 1

multi_claims = 0
for i in range(len(grid)):
  for j in range(len(grid[0])):
    if grid[i][j] > 1:
      multi_claims += 1

p.answer_a = multi_claims
