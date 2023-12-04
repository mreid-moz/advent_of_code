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

# Each item is (card id, number of instances we have)
cards = [('Card 0', 0)] * len(lines)

for i, line in enumerate(lines):
    card_id, nums = line.split(': ')
    cards[i] = (card_id, cards[i][1] + 1)
    winners, haves = nums.split(' | ')
    winners = winners.strip()
    haves = haves.strip()
    win_set = set(winners.split()) # arg-free split splits on \s+, sometimes there's more than one space.
    have_set = set(haves.split())
    num_winners = len(have_set.intersection(win_set))
    for w in range(num_winners):
        # add the number of this card to each of the next cards
        cards[i+w+1] = (cards[i+w+1][0], cards[i+w+1][1] + cards[i][1])
    card_value = 0
    if num_winners > 0:
        card_value = 2 ** (num_winners - 1)
    logging.debug("line {}: {} contained {} winners for {} points. we ended up with {} copies of it".format(i, card_id, num_winners, card_value, cards[i][1]))
    card_values += card_value

logging.info("Overall value: {}".format(card_values))
total_num_cards = sum([t[1] for t in cards])
logging.info("Overall number of cards: {}".format(total_num_cards))
if not TEST:
    p.answer_a = card_values
    p.answer_b = total_num_cards
