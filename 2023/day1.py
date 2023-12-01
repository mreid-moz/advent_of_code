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
lines = p.input_data.splitlines()

written_out_nums = {
	'one': "1",
	'two': "2",
	'three': "3",
	'four': "4",
	'five': "5",
	'six': "6",
	'seven': "7",
	'eight': "8",
	'nine': "9",
}

def replace_nums(line):
	for i in range(len(line) - 1):
		for k, v in written_out_nums.items():
			if line[i:].startswith(k):
				# logging.debug("Found {} at {} in {}".format(k, i, line))
				prefix = ""
				if i > 0:
					prefix = line[0:i]
				suffix = ""
				if i + len(k) < len(line):
					suffix = line[i + len(k):]
				# logging.debug("{}/{}/{}".format(prefix, v, suffix))
				line = prefix + v + suffix
	return line

nums = []
s = 0
for line in lines:
	cleaned_line = replace_nums(line)
	num = []
	for c in cleaned_line:
		if c <= '9' and c >= '0':
			num.append(c)
	n = int(num[0] + num[-1])
	logging.debug("{} -> {}: [{}] = {}; {} + {} = {}".format(line, cleaned_line, ",".join(num), n, s, n, s+n))
	s += n

#p.answer_a = s
print(s)
p.answer_b = s