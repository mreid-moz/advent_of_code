from aocd.models import Puzzle
from collections import defaultdict

p = Puzzle(year=2018, day=2)

lines = p.input_data.splitlines()

def count_letters(code):
  counts = defaultdict(int)
  for letter in code:
    counts[letter] += 1
  return counts

def n_letters(code, n=2, counts=None):
  if counts is None:
    counts = count_letters(code)

  if n in counts.values():
    return True
  return False

two_counts = 0
three_counts = 0
for code in lines:
  counts = count_letters(code)
  if n_letters(code, 2, counts):
    two_counts += 1
  if n_letters(code, 3, counts):
    three_counts += 1

p.answer_a = two_counts * three_counts

def diff_by_one(c1, c2):
  diff_count = 0
  for i in range(len(c1)):
    if c1[i] != c2[i]:
      diff_count += 1
    if diff_count > 1:
      return False
  return diff_count == 1

def get_sames(c1, c2):
  out = ''
  for i in range(len(c1)):
    if c1[i] == c2[i]:
      out += c1[i]
  return out

for i in range(len(lines) - 1):
  for j in range(i+1, len(lines)):
    if diff_by_one(lines[i], lines[j]):
      result = get_sames(lines[i], lines[j])
      p.answer_b = result
      break