from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys
from copy import deepcopy

logging.basicConfig(level=logging.INFO)

puzz = Puzzle(year=2022, day=19)

TEST = False
PART_ONE = False
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
    self.ore_bot_ore = int(m.group(2))
    self.clay_bot_ore = int(m.group(3))
    self.obsidian_bot_ore = int(m.group(4))
    self.obsidian_bot_clay = int(m.group(5))
    self.geode_bot_ore = int(m.group(6))
    self.geode_bot_obsidian = int(m.group(7))

class State:
  RESOURCE_TYPES = ('geode', 'obsidian', 'clay', 'ore')
  def __init__(self, ore_bots=1, clay_bots=0, obsidian_bots=0, geode_bots=0,
                     ore=0, clay=0, obsidian=0, geode=0):
    self.ore_bots = ore_bots
    self.clay_bots = clay_bots
    self.obsidian_bots = obsidian_bots
    self.geode_bots = geode_bots
    self.ore = ore
    self.clay = clay
    self.obsidian = obsidian
    self.geode = geode

  def accumulate(self):
    self.ore += self.ore_bots
    self.clay += self.clay_bots
    self.obsidian += self.obsidian_bots
    self.geode += self.geode_bots

  def get_resources(self):
    return (self.geode, self.obsidian, self.clay, self.ore)

  def get_robots(self):
    return (self.geode_bots, self.obsidian_bots, self.clay_bots, self.ore_bots)

  def get_both(self):
    return ((self.geode, self.geode_bots),(self.obsidian, self.obsidian_bots),(self.clay, self.clay_bots),(self.ore, self.ore_bots))

  def get_affordables(self, blueprint):
    affordables = []
    if self.ore >= blueprint.ore_bot_ore:
      affordables.append(3)
    if self.ore >= blueprint.clay_bot_ore:
      affordables.append(2)
    if self.ore >= blueprint.obsidian_bot_ore and self.clay >= blueprint.obsidian_bot_clay:
      affordables.append(1)
    if self.ore >= blueprint.geode_bot_ore and self.obsidian >= blueprint.geode_bot_obsidian:
      affordables.append(0)
    return affordables

  def buy(self, blueprint, robot):
    ore_cost = 0
    clay_cost = 0
    obsidian_cost = 0
    if robot == 0:
      ore_cost = blueprint.geode_bot_ore
      obsidian_cost = blueprint.geode_bot_obsidian
      self.geode_bots += 1
    elif robot == 1:
      ore_cost = blueprint.obsidian_bot_ore
      clay_cost = blueprint.obsidian_bot_clay
      self.obsidian_bots += 1
    elif robot == 2:
      ore_cost = blueprint.clay_bot_ore
      self.clay_bots += 1
    else:
      ore_cost = blueprint.ore_bot_ore
      self.ore_bots += 1
    # logging.debug(f"Buying a {State.RESOURCE_TYPES[robot]} robot for {ore_cost} ore, {clay_cost} clay, {obsidian_cost} obsidian")
    self.ore -= ore_cost
    self.clay -= clay_cost
    self.obsidian -= obsidian_cost

  def clone(self):
    return State(self.ore_bots, self.clay_bots, self.obsidian_bots, self.geode_bots,
                 self.ore, self.clay, self.obsidian, self.geode)

  def __str__(self):
    return f"🤖={self.get_robots()}; ⛏️={self.get_resources()}"

  def __hash__(self):
    return hash(self.get_both())

blueprints = []
for line in lines:
  #logging.debug(line)
  blueprints.append(Blueprint(line))

def add_if_new(state, target, memo):
  b = state.get_both()
  if b not in memo:
    memo.add(b)
    target.append(state)

def max_geodes(blueprint, max_ticks=24):
  outcomes = [State()]
  most_needed = [10000000000, blueprint.geode_bot_obsidian, blueprint.obsidian_bot_clay,
                 max([blueprint.ore_bot_ore, blueprint.clay_bot_ore, blueprint.obsidian_bot_ore, blueprint.geode_bot_ore])]
  max_geodes = 0
  for i in range(max_ticks):
    logging.info(f"Time {i+1}, considering {len(outcomes)} states.")
    new_outcomes = []
    seen_states = set()
    for oi, outcome in enumerate(outcomes):
      if oi > 0 and oi % 100000 == 0:
        logging.info(f"Processing outcome {oi} of {len(outcomes)}")
        # logging.info(f"State: {outcome}")
      affordables = outcome.get_affordables(blueprint)
      # logging.debug(f"Found {len(affordables)} affordables")

      # accumulate resources:
      outcome.accumulate()
      if outcome.geode > max_geodes:
        max_geodes = outcome.geode

      # First, don't buy anything (unless *everything* is affordable, in which case don't wait)
      if len(affordables) < 4:
        # logging.debug("Queueing next step: don't buy")
        add_if_new(outcome, new_outcomes, seen_states)

      # don't buy stuff on the last round.
      # if i + 1 == max_ticks:
      #   continue

      # Then buy each of the possible things
      for purchase in affordables:
        # don't buy more of the thing if we already get enough per turn.
        if purchase == 1 and outcome.obsidian_bots > most_needed[purchase]:
          # logging.debug(f"Already have {outcome.obsidian_bots} obsidian bots. Most we need is {most_needed[purchase]}. Not buying more.")
          continue
        elif purchase == 2 and outcome.clay_bots > most_needed[purchase]:
          # logging.debug(f"Already have {outcome.clay_bots} clay bots. Most we need is {most_needed[purchase]}. Not buying more.")
          continue
        elif purchase == 3 and outcome.ore_bots > most_needed[purchase]:
          # logging.debug(f"Already have {outcome.ore_bots} ore bots. Most we need is {most_needed[purchase]}. Not buying more.")
          continue

        another = outcome.clone()
        # logging.debug(f"Queueing next step: buy {purchase}")
        another.buy(blueprint, purchase)
        add_if_new(another, new_outcomes, seen_states)

    outcomes = new_outcomes
    # outcomes = []
    # distinct_states = set()
    # # Only keep one state for each distinct outcome. Blueprint is the same for all states.
    # for oi, o in enumerate(new_outcomes):
    #   # o.tick()
    #   # os = str(o)
    #   os = o.get_both()
    #   if os not in distinct_states:
    #     outcomes.append(o)
    #     distinct_states.add(os)

  # logging.info(f"Checking {len(outcomes)} possible outcomes")
  # max_geodes = 0
  # max_state = None
  # for oi, o in enumerate(outcomes):
  #   if oi > 0 and oi % 200000 == 0:
  #     logging.info(f"Processing outcome {oi} of {len(outcomes)}")
  #   geodes = o.geode
  #   if geodes > max_geodes:
  #     max_geodes = geodes
  #     max_state = o
  #     # logging.debug(f"Found a new max: {o}")
  # logging.info(f"Max state: {max_state}")
  return max_geodes
  #return max_state.resources['geode']

if PART_ONE:
  quality_levels = 0
  for blueprint in blueprints:
    m = max_geodes(blueprint)
    logging.info(f"Max geodes for blueprint {blueprint.id}: {m}")
    quality_levels += (m * blueprint.id)

  logging.info(f"Quality level sum: {quality_levels}")
  if not TEST:
    puzz.answer_a = quality_levels
else:
  product = 1
  for blueprint in blueprints[0:3]:
    m = max_geodes(blueprint, max_ticks=32)
    logging.info(f"Max geodes for blueprint {blueprint.id}: {m}")
    product *= m

  logging.info(f"Product was {product}")
  if not TEST:
    puzz.answer_b = product
