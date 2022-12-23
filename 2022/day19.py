from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

puzz = Puzzle(year=2022, day=19)

lines = puzz.input_data.splitlines()


pattern = re.compile(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")

# strategy:
# build one of each robot
#   see what becomes the limiting factor
#   go back in time and make another robot of that kind to unblock

# strategy:
# as soon as you have enough materials to build any kind of robot
# look at surplus, make sure we'd catch up before we could make another geode robot, otherwise spend it.

class Blueprint:
  def __init__(self, line):
    m = pattern.match(line)
    if not m:
      logging.warning(f"Unexpected line: {line}")
    self.id = int(m.group(1))
    self.costs = {}
    # ore, clay, obsidian
    self.costs['ore'] = (int(m.group(2)), 0, 0)
    self.costs['clay'] = (int(m.group(3)), 0, 0)
    self.costs['obsidian'] = (int(m.group(4)), int(m.group(5)), 0)
    self.costs['geode'] = (int(m.group(6)), 0, int(m.group(6)))

class Session:
  def __init__(self, blueprint):
    self.blueprint = blueprint
    self.robots = defaultdict(int)
    self.robots['ore'] = 1

    self.resources = defaultdict(int)

blueprints = []
for line in lines:
  logging.debug(line)
  blueprints.append(Blueprint(line))

def max_geodes(blueprint):

# puzz.answer_a = 10
