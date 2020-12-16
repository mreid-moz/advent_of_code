import logging
import sys

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

class Rule:
  def __init__(self, line):
    self.name, ranges = line.split(":")
    low_range, hi_range = [r.strip() for r in ranges.split("or")]
    self.min1, self.max1 = [int(m) for m in low_range.split("-")]
    self.min2, self.max2 = [int(m) for m in hi_range.split("-")]

  def validate(self, val):
    if val >= self.min1 and val <= self.max1:
      return True
    if val >= self.min2 and val <= self.max2:
      return True
    return False

COLLECTING_RULES = "collecting rules"
YOUR_TICKET = "your ticket:"
NEARBY_TICKETS = "nearby tickets:"
state = COLLECTING_RULES

rules = {}
your_ticket = None
nearby_tickets = list()

for line in my_input:
  if line == YOUR_TICKET:
    state = YOUR_TICKET
    continue
  elif line == NEARBY_TICKETS:
    state = NEARBY_TICKETS
    continue
  elif len(line) == 0:
    continue

  if state == COLLECTING_RULES:
    rule = Rule(line)
    rules[rule.name] = rule
  elif state == YOUR_TICKET:
    your_ticket = line
  elif state == NEARBY_TICKETS:
    nearby_tickets.append(line)

scanning_error_rate = 0
for ticket in nearby_tickets:
  ticket_fields = [int(i) for i in ticket.split(',')]
  for f in ticket_fields:
    field_valid = False
    for r in rules.values():
      if r.validate(f):
        field_valid = True
        break
    if not field_valid:
      logging.debug("Field value {} is not valid according to any rule".format(f))
      scanning_error_rate += f

logging.info("Part 1: scanning error rate was {}".format(scanning_error_rate))