from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

pattern = re.compile(r"Valve ([A-Z]+) has flow rate=(\d+); tunnel leads to valve (.+)")
pattern2 = re.compile(r"Valve ([A-Z]+) has flow rate=(\d+); tunnels lead to valves (.+)")
logging.basicConfig(level=logging.DEBUG)

puzz = Puzzle(year=2022, day=16)

TEST = True

if TEST:
  lines = [
    "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
    "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
    "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
    "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
    "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
    "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
    "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
    "Valve HH has flow rate=22; tunnel leads to valve GG",
    "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
    "Valve JJ has flow rate=21; tunnel leads to valve II",
  ]
else:
  lines = puzz.input_data.splitlines()

class Valve:
  def __init__(self, name, flow_rate, tunnels):
    self.name = name
    self.flow_rate = int(flow_rate)
    self.tunnels = tunnels.split(", ")
    self.state = 'Closed'

  def get_flow(self):
    if self.state == 'Closed':
      return 0
    return self.flow_rate

valves = {}
for line in lines:
  m = pattern.match(line)
  if not m:
    m = pattern2.match(line)
    if not m:
      logging.warning(f"Unexpected input: {line}")
      break
  valve_name = m.group(1)
  valve_rate = m.group(2)
  valve_tunnels = m.group(3)
  valves[valve_name] = Valve(valve_name, valve_rate, valve_tunnels)
  logging.debug(f"Found a valve {valve_name} with flow rate {valve_rate}, tunnels {valve_tunnels}")

logging.info(f"Found {len(valves)} valves")

def compute_flow(path, max_steps=30):
  valves_on = set()
  flow = 0
  for timer, p in enumerate(path):
    minute = timer + 1
    logging.debug(f"Minute {minute}")
    if timer > 0 and p == path[timer-1]:
      logging.debug(f"Opened valve {p}")
      valves_on.add(p)
    else:
      logging.debug(f"moved to {p}")
    for v in valves_on:
      flow += valves[v].flow_rate
    if timer >= max_steps:
      break
  return flow

if TEST:
  example_flow = [
    'AA', 'DD', 'DD', 'CC', 'BB', 'BB', 'AA', 'II', 'JJ', 'JJ', # min 1-9
    'II', 'AA', 'DD', 'EE', 'FF', 'GG', 'HH', 'HH', 'GG', 'FF', # min 10-19
    'EE', 'EE', 'DD', 'CC', 'CC', 'CC', 'CC', 'CC', 'CC', 'CC']

  logging.debug(f"computing flow for example {example_flow}")
  logging.debug(f"flow was {compute_flow(example_flow)}")

# paths = [['AA']]
# step_num = 0
# while step_num < 29:
#   step_num += 1
#   new_paths = []
#   for path in paths:
#     # logging.info(f"Current path length is {len(path)}")
#     current_valve = path[-1]
#     #if valves[current_valve].flow_rate > 0:
#     new_paths.append(path + [current_valve]) # stay in the same place
#     for tunnel in valves[current_valve].tunnels:
#       new_paths.append(path + [tunnel])
#   paths = new_paths
#   logging.info(f"After {step_num} steps, we have {len(paths)} to consider")
#   # keep the best paths
#   if len(paths) > 10000:
#     paths = sorted(paths, key=compute_flow)
#     paths = paths[-10000:]
#     logging.info(f"worst: {compute_flow(paths[0])}, best: {compute_flow(paths[-1])}")

# best_path = None
# best_flow = 0
# for p in paths:
#   f = compute_flow(p)
#   if f > best_flow:
#     best_flow = f
#     best_path = p

# logging.info(f"Best flow: {best_flow}")
# logging.info(f"Best path: {best_path}")
# if not TEST:
#   puzz.answer_a = best_flow


def compute_elephant_flow(path, max_steps=26):
  valves_on = set()
  flow = 0
  for i in range(len(path) // 2):
    me = path[i*2]
    elephant = path[i*2+1]
    minute = i + 1
    logging.debug(f"Minute {minute}")
    if i > 0 and me == path[(i-1)*2]:
      logging.debug(f"I Opened valve {me}")
      valves_on.add(me)
    else:
      logging.debug(f"I moved to {me}")

    if i > 0 and elephant == path[(i-1)*2 + 1]:
      logging.debug(f"Elephant Opened valve {elephant}")
      valves_on.add(elephant)
    else:
      logging.debug(f"Elephant moved to {elephant}")
    for v in valves_on:
      flow += valves[v].flow_rate
    logging.debug(f"Flow was {flow}")
  return flow

def compute_memo_flow(path, next_me, next_elephant):
  valves_on = path.valves_on
  if path.me == next_me:
    valves_on.add(next_me)
  if path.elephant == next_elephant:
    valves_on.add(next_elephant)
  flow = path.flow
  for v in valves_on:
    flow += valves[v].flow_rate
  return flow, valves_on


class PathMemo:
  def __init__(self, me, elephant, valves_on, flow=0, steps=0):
    self.full_path = [me, elephant]
    self.valves_on = valves_on
    self.me = me
    self.elephant = elephant
    self.flow = flow
    self.steps = steps

  def __str__(self):
    return f"Me: {self.me}, E: {self.elephant}, Flow: {self.flow}, steps: {self.steps}, valves: {self.valves_on}, full_path: {self.full_path}"


if TEST:
  for example_flow in [[
    'AA', 'AA',
    # you, elephant
    'II', 'DD',
    'JJ', 'DD',
    'JJ', 'EE',
    'II', 'FF',
    'AA', 'GG',
    'BB', 'HH',
    'BB', 'HH',
    'CC', 'GG',
    'CC', 'FF',
    'CC', 'EE',
    'CC', 'EE',
    'CC', 'EE',
    'CC', 'EE',
    'CC', 'EE',
    'CC', 'EE',
    'CC', 'EE',
    'CC', 'EE',
    'CC', 'EE',
    'CC', 'EE',
    'CC', 'EE',
    'CC', 'EE',
    'CC', 'EE',
    'CC', 'EE',
    'CC', 'EE',
    'CC', 'EE'],
    ['AA', 'AA', 'BB', 'BB', 'AA', 'BB', 'AA', 'AA', 'II', 'II', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ', 'AA', 'JJ'],
    ['AA', 'AA', 'AA', 'AA', 'AA', 'AA', 'AA', 'AA', 'AA', 'AA', 'AA', 'AA'],
    ]:

    logging.info(f"computing flow for example {example_flow}")
    logging.info(f"elephant flow was {compute_elephant_flow(example_flow)}")

    pm = PathMemo(example_flow[0], example_flow[1], set(), 0, 0)
    for i in range(1, len(example_flow) // 2):
      logging.debug(f"memo: After minute {i}, flow was {pm.flow}")
      next_me = example_flow[i * 2]
      next_elephant = example_flow[(i * 2) + 1]

      new_flow, new_valves_on = compute_memo_flow(pm, next_me, next_elephant)
      new_path = PathMemo(next_me, next_elephant, new_valves_on, new_flow, pm.steps + 1)
      new_path.full_path = pm.full_path + new_path.full_path
      logging.debug(new_path)
      pm = new_path
    logging.info(f"memo flow was {pm.flow}")


# Next optimization: keep the last position, "on" valves, and current flow total (rather than the whole path) or memoize
# Also: stop paths when all valves are open.

paths = [PathMemo('AA', 'AA', set(), 0, 0)]
step_num = 0
while step_num < 25:
  step_num += 1
  new_paths = []
  for path in paths:
    #if len(path.valves_on) == len(valves):
    #  # nothing left to turn on, stay in once place
    #  new_flow, new_valves_on = compute_memo_flow(path, path.me, path.elephant)
    #  new_path = PathMemo(path.me, path.elephant, new_valves_on, new_flow, path.steps + 1)
    #  new_path.full_path = path.full_path + new_path.full_path
    #  new_paths.append(new_path)
    #  continue
    logging.debug(f"Computing next paths from {path.full_path}")
    for next_me in valves[path.me].tunnels + [path.me]:
      for next_elephant in valves[path.elephant].tunnels + [path.elephant]:
        new_flow, new_valves_on = compute_memo_flow(path, next_me, next_elephant)
        new_path = PathMemo(next_me, next_elephant, new_valves_on, new_flow, path.steps + 1)
        new_path.full_path = path.full_path + new_path.full_path
        new_paths.append(new_path)
  paths = new_paths
  num_paths = len(paths)
  logging.info(f"After {step_num} steps, we have {num_paths} to consider")
  # logging.info(f"one of them is {paths[-1]}")
  # keep the best paths
  if num_paths > 10000:
    paths.sort(key=lambda x: x.flow)
    logging.info(f"worst: {paths[0].flow}, best: {paths[-1].flow}")
    logging.info(f"worst: {paths[0]}")
    logging.info(f"best: {paths[-1]}")
    paths = paths[-10000:]
    logging.info(f"worst: {paths[0].flow}, best: {paths[-1].flow}")
    logging.info(f"worst: {paths[0]}")
    logging.info(f"best: {paths[-1]}")

best_path = None
best_flow = 0
for p in paths:
  if p.flow > best_flow:
    best_flow = p.flow
    best_path = p

logging.info(f"Best flow: {best_flow}")
logging.info(f"Best path: {best_path}")
# if not TEST:
#   puzz.answer_b = best_flow
