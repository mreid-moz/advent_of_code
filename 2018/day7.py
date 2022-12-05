from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2018, day=7)

lines = p.input_data.splitlines()

#lines = [
#  "Step C must be finished before step A can begin.",
#  "Step C must be finished before step F can begin.",
#  "Step A must be finished before step B can begin.",
#  "Step A must be finished before step D can begin.",
#  "Step B must be finished before step E can begin.",
#  "Step D must be finished before step E can begin.",
#  "Step F must be finished before step E can begin.",
#]

pattern = re.compile(r"Step (.) must be finished before step (.) can begin.")

dependencies = {}
inverse_dependencies = defaultdict(list)
nodes = []
for line in lines:
  m = pattern.match(line)
  if m is None:
    logging.error(f"Bad input: {line}")
    break
  first = m.group(1)
  second = m.group(2)
  if first not in nodes:
    nodes.append(first)
  if second not in nodes:
    nodes.append(second)
  if second not in dependencies:
    dependencies[second] = []
  dependencies[second].append(first)
  inverse_dependencies[first].append(second)
  logging.debug(f"{first} -> {second}")

final_order = []
nodes = sorted(nodes)

while len(final_order) < len(nodes):
  for node in nodes:
    if node in final_order:
      continue
    # check if node can finish (has no deps)
    if node not in dependencies or len(dependencies[node]) == 0:
      logging.debug(f"Node {node} is g2g")
      final_order.append(node)
      unblocks = inverse_dependencies[node]
      for n in unblocks:
        # remove this as a dependency of other nodes
        dependencies[n].remove(node)

      # start looking from the beginning of the list
      break

logging.info(final_order)
p.answer_a = "".join(final_order)
