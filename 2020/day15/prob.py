import logging
import sys

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

def rseek(haystack, needle):
  l = len(haystack)
  for i in range(l):
    location = l - i - 1
    if haystack[location] == needle:
      return location
  return None

numbers = [int(s) for s in my_input[0].split(',')]
num_iterations = 2020

for i in range(num_iterations):
  if i % 5000 == 0:
    logging.info("Looking for number #{}".format(i+1))
  if i < (len(numbers)):
    logging.debug("starting value: {}".format(numbers[i]))
    continue
  last_number = numbers[i-1]
  logging.debug("Last number was {}, looking for it in {}".format(last_number, numbers[:-1]))
  location = rseek(numbers[:-1], last_number)
  if location is None:
    logging.debug("This was the first time we saw it")
    next_number = 0
  else:
    logging.debug("We last saw it at index {}".format(location))
    next_number = i - location - 1

  logging.debug("Next number {} is {}".format(i+1, next_number))
  numbers.append(next_number)
logging.info("Part 1: number {} was {}".format(i+1, numbers[-1]))
