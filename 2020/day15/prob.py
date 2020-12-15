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



def run(num_iterations):
  numbers = [int(s) for s in my_input[0].split(',')]
  last_seen_cache = {}
  penultimate_seen_cache = {}
  for i in range(num_iterations):
    if i % 5000 == 0:
      logging.info("Looking for number #{}".format(i+1))
    else:
      logging.debug("Looking for number #{}".format(i+1))
    if i < (len(numbers)):
      logging.debug("starting value: {}".format(numbers[i]))
      penultimate_seen_cache[numbers[i]] = last_seen_cache.get(numbers[i])
      last_seen_cache[numbers[i]] = i
      continue
    last_number = numbers[i-1]
    location = penultimate_seen_cache.get(last_number)
    if location is None:
      logging.debug("This was the first time we saw {}".format(last_number))
      next_number = 0
    else:
      logging.debug("We last saw it at index {}".format(location))
      next_number = i - location - 1

    logging.debug("Next number {} is {}".format(i+1, next_number))
    numbers.append(next_number)
    penultimate_seen_cache[next_number] = last_seen_cache.get(next_number)
    last_seen_cache[next_number] = i
  return (i+1, numbers[-1])

n, val = run(2020)
logging.info("Part 1: number {} was {}".format(n, val))
n, val = run(30000000)
logging.info("Part 2: number {} was {}".format(n, val))
