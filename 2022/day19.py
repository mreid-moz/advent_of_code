from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys
from copy import deepcopy

logging.basicConfig(level=logging.INFO)

puzz = Puzzle(year=2022, day=19)

TEST = True
if TEST:
  lines = [
    "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.",
    "Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."
  ]
else:
  lines = puzz.input_data.splitlines()


pattern = re.compile(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")

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
    self.costs['geode'] = (int(m.group(6)), 0, int(m.group(7)))

class State:
  RESOURCE_TYPES = ['geode', 'obsidian', 'clay', 'ore']
  def __init__(self, blueprint):
    self.blueprint = blueprint
    self.robots = defaultdict(int)
    self.robots['ore'] = 1
    self.resources = defaultdict(int)
    self.time = 0
    self.purchases = []

  def tick(self):
    self.time += 1
    for resource, count in self.robots.items():
      self.resources[resource] += count
      #logging.debug(f"Collected {count} {resource}. New total: {self.resources[resource]}")
    for p in self.purchases:
      self.robots[p] += 1
    self.purchases = []

  def get_resources(self):
    return [self.resources[t] for t in State.RESOURCE_TYPES]

  def get_robots(self):
    return [self.robots[t] for t in State.RESOURCE_TYPES]

  def get_both(self):
    return [(self.resources[t], self.robots[t]) for t in State.RESOURCE_TYPES]

  def get_affordables(self):
    affordables = set()
    for robot, costs in self.blueprint.costs.items():
      ore, clay, obsidian = costs
      if self.resources['ore'] >= ore and self.resources['clay'] >= clay and self.resources['obsidian'] >= obsidian:
        affordables.add(robot)
    return affordables

  def buy(self, robot):
    ore, clay, obsidian = self.blueprint.costs[robot]
    logging.debug(f"Buying a {robot} robot for {ore} ore, {clay} clay and {obsidian} obsidian")
    self.resources['ore'] -= ore
    self.resources['clay'] -= clay
    self.resources['obsidian'] -= obsidian
    self.purchases.append(robot)

  def clone(self):
    cloned = State(self.blueprint)
    cloned.robots = deepcopy(self.robots)
    cloned.resources = deepcopy(self.resources)
    cloned.purchases = deepcopy(self.purchases)
    return cloned

  def __str__(self):
    return f"🤖={self.get_robots()}; ⛏️={self.get_resources()}"

blueprints = []
for line in lines:
  #logging.debug(line)
  blueprints.append(Blueprint(line))

def max_geodes(blueprint, max_ticks=24):
  outcomes = [State(blueprint)]
  for i in range(max_ticks):
    logging.info(f"Time {i+1}, considering {len(outcomes)} states.")
    #max_resources_so_far = outcomes[0].get_both()
    #max_state = outcomes[0]
    new_outcomes = []
    for oi, outcome in enumerate(outcomes):
      if oi > 0 and oi % 100000 == 0:
        logging.info(f"Processing outcome {oi} of {len(outcomes)}")
      #if outcome.get_both() > max_resources_so_far:
      #  max_resources_so_far = outcome.get_both()
      #  max_state = outcome
      # If we can afford a geode robot, always buy it ASAP.
      affordables = outcome.get_affordables()
      if 'geode' in affordables:
        outcome.buy('geode')
        new_outcomes.append(outcome)
      # Always buy at least one clay robot ASAP too. Unless:
      # If neither obsidian nor geode robots require clay, then this isn't important.
      # I checked the input and they all require clay.
      #elif 'clay' in affordables and outcome.robots['clay'] == 0 and something_needs_clay:
      #  outcome.buy('clay')
      #  new_outcomes.append(outcome)
      else:
        # Otherwise, append all paths.
        # First, don't buy anything (unless *everything* is affordable, in which case don't wait)
        if len(affordables) < 4:
          logging.debug("Queueing next step: don't buy")
          new_outcomes.append(outcome)
        # Then buy each of the possible things
        for purchase in outcome.get_affordables():
          another = outcome.clone()
          logging.debug(f"Queueing next step: buy {purchase}")
          another.buy(purchase)
          new_outcomes.append(another)
    outcomes = []
    distinct_states = set()
    # Only keep one state for each distinct outcome. Blueprint is the same for all states.
    for o in new_outcomes:
      o.tick()
      os = str(o)
      if os not in distinct_states:
        outcomes.append(o)
        distinct_states.add(os)
    # logging.info(f"In {len(new_outcomes)} there were {len(distinct_states)} distinct states")
    logging.info(f"So far, max resources was with {max_state}")

  logging.info(f"Checking {len(outcomes)} possible outcomes")
  max_geodes = 0
  for oi, o in enumerate(outcomes):
    if oi > 0 and oi % 100000 == 0:
      logging.info(f"Processing outcome {oi} of {len(outcomes)}")
    geodes = o.resources['geode']
    if geodes > max_geodes:
      max_geodes = geodes
      logging.debug(f"Found a new max: {o}")
  return max_geodes
  #return max_state.resources['geode']

quality_levels = 0
for blueprint in blueprints:
  m = max_geodes(blueprint)
  logging.info(f"Max geodes for blueprint {blueprint.id}: {m}")
  quality_levels += (m * blueprint.id)

logging.info(f"Quality level sum: {quality_levels}")
if not TEST:
  puzz.answer_a = quality_levels
# puzz.answer_a = 10
