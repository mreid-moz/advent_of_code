import logging
import copy
import sys
from collections import defaultdict
from functools import reduce

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

closes = {
  ')': '(',
  ']': '[',
  '}': '{',
  '>': '<'
}
opens = {v: k for k, v in closes.items()}

scores_corrupt = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137
}

scores_incomplete = {
  '(': 1,
  '[': 2,
  '{': 3,
  '<': 4
}

def score_line(line, score_incomplete=False):
  open_stack = []
  for c in list(line):
    if c in opens:
      open_stack.append(c)
    elif c in closes:
      if closes[c] != open_stack[-1]:
        if score_incomplete:
          return 0
        else:
          return scores_corrupt[c]
      else:
        # it matched
        open_stack.pop()
    else:
      logging.warn("Unknown character '{}'".format(c))

  if not score_incomplete:
    return 0

  open_stack.reverse()
  score = 0
  for o in open_stack:
    score *= 5
    score += scores_incomplete[o]
  return score

logging.info("Score: {}".format(sum([score_line(x) for x in my_input])))

scores = [score_line(line, True) for line in my_input]
scores = sorted([s for s in scores if s > 0])
logging.info("Middle Score: {}".format(scores[int(len(scores)/2)]))


