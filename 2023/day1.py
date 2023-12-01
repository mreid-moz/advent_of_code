from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=1)

lines = p.input_data.splitlines()

nums = []
s = 0
for line in lines:
	num = []
	for c in line:
		if c <= '9' and c >= '0':
			num.append(c)
	n = int(num[0] + num[-1])
	s += n

p.answer_a = s
