import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

def step_between(v, min_value, max_value, increment):
  n = v + increment
  if n < min_value:
    return max_value
  if n > max_value:
    return min_value
  return n

class Node:
  def __init__(self, value):
    self.value = value
    self.next = self
    self.prev = self

class LinkedList:
  def __init__(self, value):
    self.n_before = 0
    self.n_after = 0
    self.current = Node(value)
    self.values = {
      value: self.current
    }

  def advance(self):
    self.current = self.current.next
    self.n_before += 1
    if self.n_before >= len(self.values):
      self.n_before = 0

  def find(self, value):
    return self.values[value]

  def insert(self, node, after):
    # ... after <node> after.next
    after.next.prev = node
    node.prev = after
    node.next = after.next
    after.next = node
    self.values[node.value] = node

  def insert_list(self, first, last, after):
    # ... after <first ... last> after.next
    after.next.prev = last
    last.next = after.next
    after.next = first
    first.prev = after

  def remove(self, after, length):
    first = after.next
    last = first
    for i in range(length-1):
      last = last.next

    after.next = last.next
    last.next.prev = after

    first.prev = None
    last.next = None
    return first, last

  def label(self, value, count=20, separator=''):
    node = self.find(value)
    values = []
    n = node.next
    for i in range(count):
      values.append(n.value)
      n = n.next
      if n == node:
        break
    return separator.join([str(v) for v in values])

  def __str__(self):
    values = ['(' + str(self.current.value) + ')']
    tn = self.current
    tp = self.current
    for i in range(self.n_before):
      tp = tp.prev
      values.insert(0, str(tp.value))
    for i in range(len(self.values)):
      tn = tn.next
      if tn == tp:
        break
      values.append(str(tn.value))

    return ' '.join(values)


input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

cup_idx = [int(s) for s in my_input[0]]
cups = LinkedList(cup_idx[0])
end = cups.current
min_cup = cup_idx[0]
max_cup = cup_idx[0]

for c in cup_idx[1:]:
  cups.insert(Node(c), end)
  end = end.next
  if c > max_cup:
    max_cup = c
  if c < min_cup:
    min_cup = c

logging.debug("before starting: {}".format(cups))

def run(cups, iterations):
  move_num = 0
  for i in range(iterations):
    move_num += 1
    if move_num % 100000 == 0:
      logging.info("-- move {} --".format(move_num))
    #logging.debug("Cups: {}".format(cups))
    destination_value = step_between(cups.current.value, min_cup, max_cup, -1)
    first, last = cups.remove(cups.current, 3)
    #logging.debug("pick up: {}, {}, {}".format(first.value, first.next.value, last.value))
    #logging.debug("after picking up: {}".format(cups))
    while destination_value == first.value or destination_value == first.next.value or destination_value == last.value:
      destination_value = step_between(destination_value, min_cup, max_cup, -1)
    #logging.debug("destination: {}".format(destination_value))
    cups.insert_list(first, last, cups.find(destination_value))
    #logging.debug("after replacing: {}".format(cups))
    cups.advance()
  #logging.debug("Final: {}".format(cups))
  #return cups

def get_cups_after(cups, n):
  node = cups.find(n)

  return cups[idx+1:] + cups[:idx]

run(cups, 100)
logging.info("Part 1: After 100 moves, cups look like {}".format(cups.label(1)))

# 38756249

cup_idx = [int(s) for s in my_input[0]]
max_cup = max(cup_idx)

cups2 = LinkedList(cup_idx[0])
end = cups2.current

for c in cup_idx[1:]:
  cups2.insert(Node(c), end)
  end = end.next

logging.info("Before setting up all the cups: {}".format(cups2))

for i in range(max_cup + 1, 1000001):
  cups2.insert(Node(i), end)
  end = end.next

logging.info("After setting up all these cups, we have current is {}, left is {}, next 20 are: {}".format(
  cups2.current.value, cups2.current.prev.value, cups2.label(cup_idx[0], separator=',')))

part_two_iterations = 10000000
run(cups2, part_two_iterations)
one = cups2.find(1)
two = one.next.value
three = one.next.next.value
cup_prod = two * three
logging.info("Part 2: After {} moves, cup product was {}*{}={}".format(part_two_iterations, two, three, cup_prod))

left = one.prev.prev.prev.prev.prev
logging.info("Other intel. Current was {}, and the neighbourhood of 1 was {}".format(cups2.current.value, cups2.label(left.value, separator=',')))

# 663374593630 is too high

