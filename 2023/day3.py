from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2023, day=3)

TEST = False

if TEST:
	lines = p.examples[0].input_data.splitlines()
	print(p.examples[0].input_data)
else:
	lines = p.input_data.splitlines()

nums = []
num_positions = {}
symbol_positions = {}

for row in range(len(lines)):
	current_num = ''
	positions = []
	for col in range(len(lines[0])):
		if lines[row][col] >= '0' and lines[row][col] <= '9':
			current_num += lines[row][col]
			positions.append((col, row))
		else: # it's a '.' or a symbol, finish the current number
			if lines[row][col] != '.':
				logging.debug("Found a symbol {} at ({},{})".format(lines[row][col], col, row))
				symbol_positions[(col, row)] = lines[row][col]
			if current_num == '':
				continue
			current_num = int(current_num)
			nums.append(current_num)
			for position in positions: 
				num_positions[position] = (current_num, positions[0])
			current_num = ''
			positions = []
			
num_vals = len(set(num_positions.values()))
logging.info("Found {} numbers, {} distinct numbers ({} vals), {} symbols. Largest was {}".format(len(nums), len(set(nums)), num_vals, len(symbol_positions), max(nums)))

# .111....
# .x......
# ........

part_numbers = set()
for position, symbol in symbol_positions.items():
	x, y = position
	adjacent_nums = set()
	adj_count = 0
	for xd in [-1, 0, 1]:
		for yd in [-1, 0, 1]:
			if xd == 0 and yd == 0:
				continue
			nx = x + xd
			ny = y + yd
			if (nx, ny) in num_positions:
				part_numbers.add(num_positions[(nx, ny)])
				adj_count += 1
				adjacent_nums.add(num_positions[(nx, ny)])
				logging.debug("Found a number adjacent to ({},{})={}: ({},{})={}".format(
					x, y, symbol, nx, ny, num_positions[(nx, ny)]))
	logging.info("Symbol {} at {} was adjacent to {} digits comprising {} unique numbers: {}".format(
		symbol, position, adj_count, len(adjacent_nums), sorted(adjacent_nums)))

part_sum = sum([i[0] for i in part_numbers])

logging.info("Sum of engine part numbers: {}".format(part_sum))

part_numbers = set()
for position, num in num_positions.items():
	x, y = position
	had_neighbours = False
	for xd in [-1, 0, 1]:
		for yd in [-1, 0, 1]:
			if xd == 0 and yd == 0:
				# logging.warn("boo")
				continue
			nx = x + xd
			ny = y + yd
			if (nx, ny) in symbol_positions:
				part_numbers.add(num)
				had_neighbours = True
				logging.debug("Found a symbol adjacent to ({},{})={}: ({},{})={}".format(
					x, y, num, nx, ny, symbol_positions[(nx, ny)]))

for n, pos in sorted(set(num_positions.values()), key=lambda x: (x[1][1], x[1][0])):
	if (n, pos) not in part_numbers:
		logging.info("{} at {} didn't have a symbol nearby :(".format(n, pos))

part_sum = sum([i[0] for i in part_numbers])

logging.info("Sum of engine part numbers: {}".format(part_sum))

if not TEST:
	p.answer_a = part_sum
