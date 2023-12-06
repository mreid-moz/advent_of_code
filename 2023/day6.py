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

