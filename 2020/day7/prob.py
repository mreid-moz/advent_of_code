import collections
import logging
import re
import sys
logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

class Bag:
  def __init__(self, spec):
    self.spec = spec

    components = spec.split(" ")
    self.contains = {}
    self.contained_by = set()

    n1 = components.pop(0)
    n2 = components.pop(0)
    self.name = "{} {}".format(n1, n2)

    t = components.pop(0)
    if t != 'bags':
      logging.warn("Malformed line: {}".format(spec))
      return

    t = components.pop(0)
    if t != 'contain':
      logging.warn("Malformed line: {}".format(spec))
      return

    while len(components) > 0:
      t = components.pop(0)
      if t == 'no':
        return
      if re.match(r'^[0-9]+$', t):
        next_name = "{} {}".format(components.pop(0), components.pop(0))
        self.contains[next_name] = int(t)
        components.pop(0)


bags = {}
target_bag = "shiny gold"

for line in my_input:
  bag = Bag(line)
  bags[bag.name] = bag

def process(bag, bags):
  #logging.debug("processing {} ({})".format(bag.name, bag.spec))
  if len(bag.contains) == 0:
    return
  for bag_name in bag.contains:
    b = bags[bag_name]
    b.contained_by.add(bag.name)
    process(b, bags)

for k, v in bags.items():
  for bag_name in v.contains:
    b = bags[bag_name]
    b.contained_by.add(k)

last_size = 0
current_set = bags.get(target_bag).contained_by
current_size = len(current_set)
while last_size != current_size:
  last_size = current_size
  new_set = set()
  for b in current_set:
    logging.debug("Adding {}".format(b))
    new_set |= bags.get(b).contained_by
  current_set |= new_set
  current_size = len(current_set)

logging.info("Part 1: {} bags can contain {}".format(current_size, target_bag))

contained_count = 0


def deep_count(bag_count, bag_type):
  total = 0
  for b, c in bags[bag_type].contains.items():
    total += deep_count(c, b)
  return bag_count + bag_count * total

# subtract one because this counts the outer bag itself.
num_bags = deep_count(1, target_bag) - 1
logging.info("Part 2: One {} bag contains {} other bags".format(target_bag, num_bags))
