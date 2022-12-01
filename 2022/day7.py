from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2022, day=7)

lines = p.input_data.splitlines()

#...

# p.answer_a = 10
