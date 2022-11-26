from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2018, day=4)

lines = p.input_data.splitlines()

p_time = re.compile(r"\[(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2})\] (.*)")
# [1518-11-19 23:58] Guard #1471 begins shift
p_guard = re.compile(r"Guard #(\d+) begins shift")

guards = {}
current_guard = None
currently_asleep = False
fell_asleep_min = None
for line in sorted(lines):
  base_match = p_time.match(line)
  if base_match is None:
    logging.error(f"unexpected line: '{line}'")
    continue
  day = base_match.group(1)
  hour = int(base_match.group(2))
  minute = int(base_match.group(3))

  what_do = base_match.group(4)
  if 'falls asleep' in what_do:
    logging.debug(f"current guard {current_guard} fell asleep at {hour}:{minute}.")
    currently_asleep = True
    fell_asleep_min = minute
  elif 'wakes up' in what_do:
    logging.debug(f"current guard {current_guard} woke up at {hour}:{minute}.")
    currently_asleep = False
    for i in range(fell_asleep_min, minute):
      logging.debug(f"setting guard {current_guard} asleep on minute {i}")
      guards[current_guard][i] += 1
  else:
    m = p_guard.match(what_do)
    if m:
      current_guard = m.group(1)
      logging.debug(f"new guard {current_guard} started.")
      if current_guard not in guards:
        guards[current_guard] = [0] * 60
      currently_asleep = False
      fell_asleep_min = None

    else:
        logging.error(f"unexpected line: '{line}'")

most_sleepy = None
most_sleepy_mins = 0
for guard_id, asleep_mins in guards.items():
  total_sleep = sum(asleep_mins)
  if total_sleep > most_sleepy_mins:
    most_sleepy_mins = total_sleep
    most_sleepy = guard_id

sleepiest_minute = 0
for i, sleepy_mins in enumerate(guards[most_sleepy]):
  if sleepy_mins > guards[most_sleepy][sleepiest_minute]:
    sleepiest_minute = i

logging.info(f"Guard {most_sleepy} was the sleepiest, sleeping {most_sleepy_mins} mins. Slept most ({guards[most_sleepy][sleepiest_minute]} times) during minute {sleepiest_minute}")

p.answer_a = int(most_sleepy) * sleepiest_minute

frequent_sleeper_id = None
frequent_minute = 0
frequency = 0
for guard_id, asleep_mins in guards.items():
  for i, sleepy_mins in enumerate(asleep_mins):
    if sleepy_mins > frequency:
      frequency = sleepy_mins
      frequent_minute = i
      frequent_sleeper_id = guard_id

logging.info(f"Guard {frequent_sleeper_id} slept {frequency} times during minute {frequent_minute}")

p.answer_b = int(frequent_sleeper_id) * frequent_minute

