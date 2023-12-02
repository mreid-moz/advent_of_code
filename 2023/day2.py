from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=2)

lines = p.input_data.splitlines()

max_colours = {
	'red': 12,
	'green': 13,
	'blue': 14
}

sum_of_ids = 0
total_game_power = 0
for line in lines:
	good_game = True
	game_maxes = defaultdict(int)
	game, selections = line.split(':')
	_, game_id_str = game.strip().split(' ')
	game_id = int(game_id_str)
	for selection in selections.split(';'):
		colours = selection.strip().split(',')
		for colour in colours:
			n, c = colour.strip().split(' ')
			c = c.strip()
			n = int(n)
			if n > game_maxes[c]:
				game_maxes[c] = n
			m = max_colours[c]
			if n > m:
				good_game = False
	if good_game:
		sum_of_ids += game_id
	game_power = game_maxes['red'] * game_maxes['green'] * game_maxes['blue']
	total_game_power += game_power

p.answer_a = sum_of_ids
p.answer_b = total_game_power
