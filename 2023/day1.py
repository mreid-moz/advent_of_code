from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=1)

# lines = """two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen""".splitlines()
TEST=True

if TEST:
	examples = p.examples
	logging.debug("TEST mode, found {} examples".format(len(examples)))
	logging.debug("First one: {}".format(examples[0]))
	lines = examples[0].input_data.splitlines()
	# sys.exit(-1)
else:
	lines = p.input_data.splitlines()

written_out_nums = {
	'one': "o1e",
	'two': "t2o",
	'three': "th3ee",
	'four': "f4ur",
	'five': "f5ve",
	'six': "s6x",
	'seven': "se7en",
	'eight': "ei8ht",
	'nine': "n9ne",
}

def replace_nums(line):
	for i in range(len(line) - 1):
		for k, v in written_out_nums.items():
			if line[i:].startswith(k):
				logging.debug("Found {} at {} in {}".format(k, i, line))
				prefix = ""
				if i > 0:
					prefix = line[0:i]
				suffix = ""
				if i + len(k) < len(line):
					suffix = line[i + len(k):]
				logging.debug("{}/{}/{}".format(prefix, v, suffix))
				line = prefix + v + suffix
	return line

nums = []
s = 0
for line in lines:
	if p.answered_a:
		logging.debug("Already did part 1, doing part 2.")
		cleaned_line = replace_nums(line)
	num = []
	for c in cleaned_line:
		if c <= '9' and c >= '0':
			num.append(c)
	n = int(num[0] + num[-1])
	logging.debug("{} -> {}: [{}] = {}; {} + {} = {}".format(line, cleaned_line, ",".join(num), n, s, n, s+n))
	s += n

print("Sum: {}".format(s))

if not TEST:
	if not p.answered_a:
		p.answer_a = s

	if not p.answered_b:
		p.answer_b = s