from aocd.models import Puzzle

def all_different(some_chars):
  return len(set(some_chars)) == len(some_chars)

def find_marker(signal, n):
  for i in range(len(signal) - n):
    if all_different(signal[i:i+n]):
      return i + n

p = Puzzle(year=2022, day=6)
signal = p.input_data
p.answer_a = find_marker(signal, 4)
p.answer_b = find_marker(signal, 14)