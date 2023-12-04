from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=4)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

card_values = 0

for line in lines:
    card_id, nums = line.split(': ')
    winners, haves = nums.split(' | ')
    winners = winners.strip()
    haves = haves.strip()
    win_set = set(winners.split())
    have_set = set(haves.split())
    num_winners = len(have_set.intersection(win_set))
    card_value = 0
    if num_winners > 0:
        card_value = 2 ** (num_winners - 1)
    logging.debug("{} contained {} winners for {} points.".format(card_id, num_winners, card_value))
    card_values += card_value

logging.info("Overall value: {}".format(card_values))
if not TEST:
    p.answer_a = card_values
