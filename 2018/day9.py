from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2018, day=9)


TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

def parse_line(line):
	pieces = line.split()
	# for i, p in enumerate(pieces):
	# 	logging.debug(f"piece {i} is {p}")
	return int(pieces[0]), int(pieces[6])

def get_index(num_marbles, index, count, clockwise=True):
	# num_marbles = len(marbles)
	new_idx = index - count
	if clockwise:
		new_idx = index + count
		while new_idx > num_marbles:
			new_idx -= num_marbles
	else:
		while new_idx < 0:
			new_idx += num_marbles
	return new_idx


logging.debug(lines[0])
players, pieces = parse_line(lines[0])
# players = 10
# pieces = 1618
logging.info(f"{players} players, {pieces} pieces")

marbles = [0]
num_marbles = 1
current_idx = 0
player_scores = [0] * players
for i in  range(1, pieces * 100):
	if i % 5000 == 0:
		logging.info(f"placing piece {i}, highest score so far: {max(player_scores)}")
	# logging.debug(f"{marbles}, idx={current_idx}, scores={player_scores}")
	if i % 23 == 0:
		p_num = i % players
		player_scores[p_num] += i
		remove_idx = get_index(num_marbles, current_idx, 7, clockwise=False)
		removed_marble = marbles.pop(remove_idx)
		player_scores[p_num] += removed_marble
		# logging.debug(f"Removed marble {remove_idx} (val: {removed_marble}): {marbles}. Scores: {player_scores}")
		current_idx = remove_idx
		num_marbles -= 1
	else:
		insert_idx = get_index(num_marbles, current_idx, 2)
		marbles.insert(insert_idx, i)
		# logging.debug(f"Added marble {i} at {insert_idx}: {marbles}")
		current_idx = insert_idx
		num_marbles += 1

high_score = max(player_scores)
logging.info(f"Highest score: {high_score}")

if not TEST:
    # p.answer_a = high_score
    p.answer_b = high_score
