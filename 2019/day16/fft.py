import logging
import math
import itertools
logging.basicConfig(level=logging.INFO)

def get_digits(n):
  return [int(i) for i in list(str(n))]

BASE = [0, 1, 0, -1]

def get_base(i, repeat):
  # 2 -> [ 0 1 1 0 0 -1 -1]
  actual = []
  for b in BASE:
    for x in range(repeat):
      actual.append(b)

  v = actual[(i + 1) % len(actual)]
  #logging.debug("{} @ repeat {} -> {} / {}".format(BASE, repeat, actual, v))
  return v

  #i2 = math.floor(i / repeat)
  #return BASE[(i2 + 1) % len(BASE)]

def fft(n):
  logging.debug("Computing fft for {}".format(n))
  digits = n
  if isinstance(n, int):
    digits = get_digits(n)
  out = []
  for i in range(len(digits)):
    repeat = i + 1
    total = 0
    for idx, d in enumerate(digits):
      b = get_base(idx, repeat)
      total += d * b
      logging.debug("{} * {} = {}".format(d, b, d*b))
    out_digit = abs(total) % 10
    logging.debug("Total: {} ({})".format(total, out_digit))
    out.append(out_digit)
  return out

def phase(n, phase):
  for p in range(phase):
    n = fft(n)
    logging.info("After phase {}: {}".format(p+1, n))
  return n

def test():
  assert(get_base(0, 1) == 1)
  assert(get_base(1, 1) == 0)
  assert(get_base(2, 1) == -1)
  assert(get_base(3, 1) == 0)
  assert(get_base(4, 1) == 1)

  assert(get_base(0, 2) == 0)
  assert(get_base(1, 2) == 1)
  assert(get_base(2, 2) == 1)
  assert(get_base(3, 2) == 0)
  assert(get_base(4, 2) == 0)
  assert(get_base(5, 2) == -1)
  assert(get_base(6, 2) == -1)
  assert(get_base(7, 2) == 0)
  assert(get_base(8, 2) == 0)
  assert(get_base(9, 2) == 1)
  assert(get_base(10, 2) == 1)
  assert(get_base(11, 2) == 0)
  assert(get_base(12, 2) == 0)
  assert(get_base(13, 2) == -1)

  f = fft(12345678)
  logging.debug("12345678 -> {}".format(f))
  assert(f == [4,8,2,2,6,1,5,8])

  f = fft([1,2,3,4,5,6,7,8])
  logging.debug("12345678 -> {}".format(f))
  assert(f == [4,8,2,2,6,1,5,8])

  f = phase(12345678, 4)
  assert(f == [0,1,0,2,9,4,9,8])

  f = phase(80871224585914546619083218645595, 100)
  assert(f[0:8] == [2,4,1,7,6,1,7,6])


#test()

with open("input") as fin:
  source_digits = fin.read().strip()

source_digits = [int(s) for s in source_digits]

f = phase(source_digits, 100)
print("First 8: {}".format("".join(f[0:8])))