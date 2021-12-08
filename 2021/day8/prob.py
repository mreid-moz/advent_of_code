import logging
import copy
import sys
from collections import defaultdict

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

easy_counter = 0
for line in my_input:
  signals, output_value = line.split('|')
  digits = output_value.split()
  for digit in digits:
    if len(digit) in [2, 3, 4, 7]:
      easy_counter += 1

logging.info("There are {} easy values in outputs".format(easy_counter))

def decode(line):
  #  0000
  # 1    2
  # 1    2
  #  3333
  # 4    5
  # 4    5
  #  7777
  for i in range(8):
    possibilities[i] = set(['a','b','c','d','e','f'])
  signals, output_value = line.split('|')
  signal_digits = signals.split()

  known_digits = [''] * 10
  # first: easy passes
  for digit in signal_digits:
    if len(digit) == 2: # it's a one
      known_digits[1] = set(list(digit))
    elif len(digit) == 3: # it's a seven
      known_digits[7] = set(list(digit))
    elif len(digits) == 4: # it's a four
      known_digits[4] = set(list(digit))
    elif len(digits) == 7: # it's an eight
      known_digits[8] = set(list(digit))

  # Now do something with this knowledge.
  # One:
  possibilities[2] = known_digits[1]
  possibilities[5] = known_digits[1]

  # Seven:
  possibilities[0] = known_digits[7] - possibilities[2]
  # We now know the 0 position.
  zero_pos = next(iter(possibilities[0]))
  for i in range(1,8):
    possibilities[i].remove(zero_pos)

  # Four:
  possibilities[1] = known_digits[4] - possibilities[2]
  possibilities[3] = known_digits[4] - possibilities[5]

  # Next, get the ones of length 6 (0, 6, 9)
  len_six = []
  for digit in signal_digits:
    if len(digit) == 6:
      len_six.append(digit)

  for six in len_six:
    segments = set(list(six))
    # find zero:
    if len(segments - known_digits[1]) == 4 and len(segments - known_digits[4]) == 3:
      known_digits[0] = segments
      # we now know the 3 position
      possibilities[3] = known_digits[4] - segments
      three_pos = next(iter(possibilities[3]))
      for i in range(1,8):
        possibilities[i].remove(three_pos)
    elif len(segments - known_digits[1]) == 5 and len(segments - known_digits[4]) == 3:
      known_digits[6] = segments
      # we now know the 2 position
      possibilities[2] = known_digits[1] - segments
      two_pos = next(iter(possibilities[2]))
      for i in range(1,8):
        possibilities[i].remove(two_pos)
    elif len(segments - known_digits[1]) == 4 and len(segments - known_digits[4]) == 2:
      known_digits[9] = segments
      # we now know the 4 and 7 positions
      possibilities[4] = known_digits[8] - known_digits[9]
      possibilities[7] = known_digits[9] - known_digits[4] - known_digits[7]
      two_pos = next(iter(possibilities[2]))
      for i in range(1,8):
        possibilities[i].remove(two_pos)
    else:
      logging.warn("uh ok, bad codes here")

  # Now we know 0, 1, 4, 6, 7, 8, 9
  # Next: get the ones of length 5 (2, 3, 5)
  for digit in signal_digits:
    if len(digit) == 5:
      segments = set(list(digit))
      if len(segments - known_digits[9]) == 1:
        known_digits[2] = segments
      elif len(segments - known_digits[6]) == 0:
        known_digits[5] = segments
      elif len(segments - known_digits[7]) == 2:
        known_digits[3] = segments
      else:
        logging.warn("egad, more bad codes")

  # decode the output_value, return it
  code_map = {}
  for n, val in enumerate(known_digits):
    code = "".join(sorted(list(val)))
    code_map[code] = n

  # sort the strings to match our map
  output_digits = [code_map["".join(sorted(list(v)))] for v in output_value.split()]
  return int(output_digits)

total = 0
for line in my_input:
  total += decode(line)

logging.info("Total of all the codes is {}".format(total))

