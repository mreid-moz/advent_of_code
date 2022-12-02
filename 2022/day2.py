from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2022, day=2)

lines = p.input_data.splitlines()

# rock=1, paper=2, scissors=3
# loss=0, tie=3,   win=6
points = {
  "A X": 4,
  "A Y": 8,
  "A Z": 3,

  "B X": 1,
  "B Y": 5,
  "B Z": 9,

  "C X": 7,
  "C Y": 2,
  "C Z": 6,
}

total = 0
for line in lines:
  total += points[line]

p.answer_a = total

def win_against(rps):
  if rps == 'A':
    return 'Y'
  elif rps == 'B':
    return 'Z'
  return 'X'

def tie_against(rps):
  if rps == 'A':
    return 'X'
  elif rps == 'B':
    return 'Y'
  return 'Z'

def lose_against(rps):
  if rps == 'A':
    return 'Z'
  elif rps == 'B':
    return 'X'
  return 'Y'

total = 0
for line in lines:
  opponent = line[0]
  outcome = line[-1]
  you = opponent
  if outcome == 'X':
    you = lose_against(opponent)
  elif outcome == 'Y':
    you = tie_against(opponent)
  else:
    you = win_against(opponent)
  total += points[f"{opponent} {you}"]

p.answer_b = total