from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2018, day=7)

#lines = p.input_data.splitlines()

lines = [
  "Step C must be finished before step A can begin.",
  "Step C must be finished before step F can begin.",
  "Step A must be finished before step B can begin.",
  "Step A must be finished before step D can begin.",
  "Step B must be finished before step E can begin.",
  "Step D must be finished before step E can begin.",
  "Step F must be finished before step E can begin.",
]

pattern = re.compile(r"Step (.) must be finished before step (.) can begin.")

dependencies = defaultdict(list)
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
  dependencies[second].append(first)
  inverse_dependencies[first].append(second)
  logging.debug(f"{first} -> {second}")


def get_node_with_fewest_deps(some_deps):
  min_deps_node = None
  min_deps = None
  for node, dependencies in some_deps:
    if min_deps_node is None:
      min_deps_node = node
      min_deps = len(dependencies)
    elif len(dependencies) < min_deps:
      min_deps_node = node
      min_deps = len(dependencies)
  return min_deps_node

final_order = []
nodes = sorted(nodes)
for node in nodes:
    if node not in dependencies:
      logging.debug(f"Adding {node} with no dependencies.")
      final_order.append(node)

while len(final_order) < len(nodes):
  for i, node in enumerate(final_order):
    if node in inverse_dependencies and len(inverse_dependencies[node]) > 0:
      next_node = sorted(inverse_dependencies[node])[0]
      inverse_dependencies[node].remove(next_node)
      logging.debug(f"Adding node {next_node} after {node}")
      final_order.insert(i + 2, next_node)
      logging.info(f"final order so far: {final_order}")
      break
    else:
      logging.debug(f"No inverse_dependencies for {node}")

logging.info(final_order)
# p.answer_a = 10
