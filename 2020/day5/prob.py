import logging
import re
logging.basicConfig(level=logging.INFO)

class Seat:
  def __init__(self, spec):
    self.spec = spec
    self.parse_spec()

  def binary_search(self, splits, low_char, high_char):
    binary_steps = len(splits)
    target = 0
    for i in range(binary_steps):
      current_range = 2**(binary_steps-i)
      if splits[i] == low_char:
        logging.debug("Lo half of {}".format(current_range))
      else:
        logging.debug("Hi half of {}".format(current_range))
        target += int(current_range / 2)
    logging.debug("{} represents {}".format(splits, target))
    return target

  def get_row(self, spec):
    logging.debug("Checking row for {}".format(spec))
    splits = spec[0:7]
    row_num = self.binary_search(splits, 'F', 'B')
    logging.debug("{} represents row {}".format(spec, row_num))
    return row_num

  def get_col(self, spec):
    logging.debug("Checking col for {}".format(spec))
    col_num = self.binary_search(spec[-3:], 'L', 'R')
    logging.debug("{} represents col {}".format(spec, col_num))
    return col_num

  def parse_spec(self):
    self.row = self.get_row(self.spec)
    self.column = self.get_col(self.spec)
    self.seat_id = self.row * 8 + self.column
    pass

input_file = 'input'
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]


def test():
  for ss, sid in [['BFFFBBFRRR', 567], ['FFFBBBFRRR', 119], ['BBFFBBFRLL', 820]]:
    s = Seat(ss)
    result = 'PASS'
    if s.seat_id != sid:
      result = 'FAIL'
    logging.info("{}: {} -> {}, calculated {}".format(result, ss, sid, s.seat_id))

#test()

max_sid = -1
min_sid = 999
sids = []
for line in my_input:
  s = Seat(line)
  sids.append(s.seat_id)
  if s.seat_id > max_sid:
    max_sid = s.seat_id
  if s.seat_id < min_sid:
    min_sid = s.seat_id

logging.info("Found max Seat ID of {}".format(max_sid))

sids = sorted(sids)
for i in range(max_sid):
  if sids[i] != min_sid + i:
    logging.info("Found missing Seat ID {}".format(min_sid + i))
    break