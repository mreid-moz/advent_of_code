from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=6)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

times = [int(s) for s in lines[0].split()[1:]]
distances = [int(s) for s in lines[1].split()[1:]]

def ways_to_win(time, distance):
    win_count = 0
    for i in range(time):
        # charge for i seconds
        speed = i
        my_distance = speed * (time - i)
        logging.debug("t={}, d={}. Charging for {} -> {}".format(time, distance, i, my_distance))
        if my_distance > distance:
            win_count += 1
    return win_count

product = 1
for i in range(len(times)):
    time = times[i]
    distance = distances[i]
    logging.debug("Looking for ways to win with time {} and distance {}".format(time, distance))
    w = ways_to_win(time, distance)
    logging.debug("With time {} and distance {}: {}".format(time, distance, w))
    product *= w
    
logging.info("Final product: {}".format(product))
if not TEST:
    p.answer_a = product

# Part 2
time = int("".join(lines[0].split()[1:]))
distance = int("".join(lines[1].split()[1:]))

logging.debug("looking for ways to beat t={}, d={}".format(time, distance))
# could do a binary search to find the first value that doesn't win...
win_count = 1 # the one at exactly half wins for sure
for i in range((time // 2) - 1, 0, -1):
    speed = i
    my_distance = speed * (time - i)
    if i % 1000 == 0:
        logging.debug("t={}, d={}. Charging for {} -> {}".format(time, distance, i, my_distance))
    if my_distance > distance:
        win_count += 2
    else:
        # there won't be any more winners once we start losing
        break

logging.info("Number of ways to beat t={}, d={}: {}".format(time, distance, win_count))
if not TEST:
    p.answer_b = win_count
