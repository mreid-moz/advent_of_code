from aocd.models import Puzzle
from collections import defaultdict

p = Puzzle(year=2018, day=1)

lines = p.input_data.splitlines()

total = 0
counts = defaultdict(int)
done = False
iteration = 0
while not done:
  print(f"Iteration {iteration}")
  for line in lines:
    sign = line[0]
    val = int(line)

    total += val
    counts[total] += 1
    if counts[total] > 1:
      p.answer_b = total
      done = True
      break
  if iteration == 0:
    p.answer_a = total
  iteration += 1
