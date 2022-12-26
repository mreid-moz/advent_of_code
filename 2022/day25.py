from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2022, day=25)

TEST = False
lines = p.input_data.splitlines()

def parse(snafu):
  p = 0
  decimal = 0
  for i in range(len(snafu) - 1, -1, -1):
    if snafu[i] == '-':
      v = -1
    elif snafu[i] == '=':
      v = -2
    else:
      v = int(snafu[i])
    decimal += v * (5 ** p)
    p += 1
  return decimal

def increment(v):
  if v == '0':
    return '1'
  if v == '1':
    return '2'
  if v == '2':
    return '1='
  if v == '=':
    return '-'
  if v == '-':
    return '0'

def carry(snafu):
  digits = list(snafu)
  pos = len(digits) - 1
  while pos >= 0:
    incremented = increment(digits[pos])
    digits[pos] = incremented[-1]
    if len(incremented) == 1:
      break
    pos -= 1

  digits = ''.join(digits)

  if pos < 0:
    digits = '1' + digits
  return digits

def encode(decimal):
  logging.debug(f"Encoding {decimal}")
  p = 0
  while 5 ** p <= decimal:
    p += 1

  p -= 1
  # logging.debug(f"Found max pow 5^{p}")

  multiple = decimal // (5 ** p)
  remainder = decimal - (multiple * 5 ** p)
  logging.debug(f"Multiple is {multiple}, remainder is {remainder}")
  prefix = ''
  pval = 0
  if multiple <= 2:
    prefix = str(multiple)
  elif multiple == 3:
    prefix = '1='
  elif multiple == 4:
    prefix = '1-'
  logging.debug(f"Found prefix {prefix}")

  if remainder == 0:
    return prefix + ('0' * p)

  logging.debug(f"Encoding remainder {remainder}")
  suffix = encode(remainder)

  if len(suffix) > p:
    # TODO: Carry the one
    prefix = carry(prefix)
    return prefix + suffix[1:]

  middle = '0' * (p - len(suffix))

  return prefix + middle + suffix

examples = [
('1=-0-2',     1747),
 ('12111',      906),
  ('2=0=',      198),
    ('21',       11),
  ('2=01',      201),
   ('111',       31),
 ('20012',     1257),
   ('112',       32),
 ('1=-1=',      353),
  ('1-12',      107),
    ('12',        7),
    ('1=',        3),
   ('122',       37),
   ('222',       62),
]
if TEST:
  for snafu, decimal in examples:
    parsed = parse(snafu)
    outcome = 'PASS'
    if parsed != decimal:
      outcome = 'FAIL'
    logging.info(f"{outcome} Parsing {snafu}. Expected: {decimal}. Actual {parsed}")

examples = [
          (1,              '1'),
          (2,              '2'),
          (3,             '1='),
          (4,             '1-'),
          (5,             '10'),
          (6,             '11'),
          (7,             '12'),
          (8,             '2='),
          (9,             '2-'),
         (10,             '20'),
         (15,            '1=0'),
         (20,            '1-0'),
         (63,           '1==='),
       (2022,         '1=11-2'),
      (12345,        '1-0---0'),
  (314159265,  '1121-1110-1=0'),
  (33010101016442, '2-=12=2-2-2-=0011-=2'),
]

if TEST:
  for decimal, snafu in examples:
    encoded = encode(decimal)
    outcome = 'PASS'
    if encoded != snafu:
      outcome = 'FAIL'
    logging.info(f"{outcome} Encoding {decimal}. Expected: {snafu}. Actual {encoded}")

total = 0
for line in lines:
  parsed = parse(line)
  logging.info(f"Parsed {line} -> {parsed}")
  total += parsed

encoded = encode(total)
logging.info(f"Sum was {total}, encoded that looks like {encoded}")


if not TEST:
  p.answer_a = encoded
