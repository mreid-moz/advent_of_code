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
  signals, output_value = line.split('|')
  signal_digits = signals.split()

  known_digits = [''] * 10
  # first: easy passes
  for digit in signal_digits:
    if len(digit) == 2: # it's a one
      known_digits[1] = set(list(digit))
      logging.debug("Found one: {}".format(digit))
    elif len(digit) == 3: # it's a seven
      known_digits[7] = set(list(digit))
      logging.debug("Found seven: {}".format(digit))
    elif len(digit) == 4: # it's a four
      known_digits[4] = set(list(digit))
      logging.debug("Found four: {}".format(digit))
    elif len(digit) == 7: # it's an eight
      known_digits[8] = set(list(digit))
      logging.debug("Found eight: {}".format(digit))

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
      logging.debug("Found zero: {}".format(six))
      # we now know the 3 position
    elif len(segments - known_digits[1]) == 5 and len(segments - known_digits[4]) == 3:
      known_digits[6] = segments
      logging.debug("Found six: {}".format(six))
      # we now know the 2 position
    elif len(segments - known_digits[1]) == 4 and len(segments - known_digits[4]) == 2:
      known_digits[9] = segments
      logging.debug("Found nine: {}".format(six))
      # we now know the 4 and 7 positions
    else:
      logging.warning("uh ok, bad codes here: {}. Diff with 1 = {}, diff with 4 = {}".format(
        six, len(segments - known_digits[1]), len(segments - known_digits[4])))

  # Now we know 0, 1, 4, 6, 7, 8, 9
  # Next: get the ones of length 5 (2, 3, 5)
  for digit in signal_digits:
    if len(digit) == 5:
      segments = set(list(digit))
      if len(segments - known_digits[9]) == 1:
        known_digits[2] = segments
        logging.debug("Found two: {}".format(digit))
      elif len(segments - known_digits[6]) == 0:
        known_digits[5] = segments
        logging.debug("Found five: {}".format(digit))
      elif len(segments - known_digits[7]) == 2:
        known_digits[3] = segments
        logging.debug("Found three: {}".format(digit))
      else:
        logging.warning("egad, more bad codes")

  # decode the output_value, return it
  code_map = {}
  for n, val in enumerate(known_digits):
    code = "".join(sorted(list(val)))
    code_map[code] = str(n)

  # sort the strings to match our map
  output_digits = [code_map["".join(sorted(list(v)))] for v in output_value.split()]
  return int(''.join(output_digits))

total = 0
for line in my_input:
  total += decode(line)

logging.info("Total of all the codes is {}".format(total))

