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
    self.position = None
    self.possible_positions = list()
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

  def validate_all(self, values):
    for v in values:
      if not self.validate(v):
        logging.debug("Rule {} rejects value {}. {}-{} or {}-{}".format(self.name, v, self.min1, self.max1, self.min2, self.max2))
        return False
    return True

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
    your_ticket = [int(i) for i in line.split(',')]
  elif state == NEARBY_TICKETS:
    nearby_tickets.append(line)

scanning_error_rate = 0
valid_tickets = list()
for ticket in nearby_tickets:
  ticket_fields = [int(i) for i in ticket.split(',')]
  valid_ticket = True
  for f in ticket_fields:
    field_valid = False
    for r in rules.values():
      if r.validate(f):
        field_valid = True
        break
    if not field_valid:
      logging.debug("Field value {} is not valid according to any rule".format(f))
      scanning_error_rate += f
      valid_ticket = False
  if valid_ticket:
    valid_tickets.append(ticket_fields)

logging.info("Part 1: scanning error rate was {}".format(scanning_error_rate))

num_tickets = len(valid_tickets)
logging.debug("Found {} valid tickets, such as {}".format(num_tickets, valid_tickets[0]))
for rule in rules.values():
  for position in range(len(valid_tickets[0])):
    logging.debug("Testing rule '{}' at position {}".format(rule.name, position))
    position_values = [t[position] for t in valid_tickets]
    if rule.validate_all(position_values):
      logging.debug("Rule '{}' applies cleanly at position {}".format(rule.name, position))
      rule.possible_positions.append(position)

# some rules could apply in multiple locations... gotta sort that out.
taken_positions = list()
while len(taken_positions) < len(rules):
  for r in rules.values():
    if r.position is not None:
      continue
    for tp in taken_positions:
      try:
        r.possible_positions.remove(tp)
      except ValueError:
        pass
    if len(r.possible_positions) == 1:
      taken_positions.append(r.possible_positions[0])
      r.position = r.possible_positions[0]
      logging.debug("Assigning position {} to rule '{}' since it only had one possible match".format(r.position, r.name))

departure_rules = [r for r in rules.values() if r.name.startswith("departure")]
departure_values = 1
for r in departure_rules:
  v = your_ticket[r.position]
  logging.debug("Applying departure field '{}' which was at position {} and had a value of {}".format(r.name, r.position, v))
  departure_values *= v
logging.info("Part 2: departure values: {}".format(departure_values))