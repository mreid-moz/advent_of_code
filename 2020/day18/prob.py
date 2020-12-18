import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

def tokenize(equation):
  equation = equation.strip()
  if equation[0] == '(':
    end = equation.index(')')
    current = compute(equation[1:end])

def find_closing_paren(equation, first_idx):
  nester = 1
  for i in range(first_idx + 1, len(equation)):
    if equation[i] == '(':
      logging.debug("Found an opening paren at {} with a nesting level of {}".format(i, nester))
      nester += 1
    elif equation[i] == ')':
      logging.debug("Found a closing paren at {} with a nesting level of {}".format(i, nester))
      nester -= 1
      if nester == 0:
        return i
  return None

def compute(total, op, equation):
  logging.debug("Calculating {} {} [{}]".format(total, op, equation))
  equation = equation.strip()
  if re.match(r'^ *\d+ *$', equation):
    logging.debug("{} was simple.".format(equation))
    if op == '+':
      return total + int(equation)
    else:
      return total * int(equation)

  if equation[0] == '(':
    end = find_closing_paren(equation, 0)
    current = compute(0, '+', equation[1:end])
    end += 2
  else:
    end = equation.index(' ')
    current = compute(0, '+', equation[:end])
    end += 1

  if op == '+':
    total += current
  else:
    total *= current
  if len(equation) <= end:
    return total

  operator = equation[end]
  return compute(total, operator, equation[end+2:])

def test():
  parens = [
    ['', 0, None],
    ['((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 0, 34],
    ['((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 15, 29],
    ['((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 1, 11],
  ]
  for equation, start, end in parens:
    actual = find_closing_paren(equation, start)
    logging.debug("equation: {}. match to start of {} is {}, computed {}".format(equation, start, end, actual))
    parens = start * ' ' + '('
    if actual is None:
      parens += 'None'
    elif actual != end:
      parens += (actual - start - 1) * ' ' + 'X'
    else:
      parens += (actual - start - 1) * ' ' + ')'
    logging.debug("          {}".format(parens))
    assert(end == actual)

  cases = [
    ['2 * 3', 6],
    ['2 + 5', 7],
    ['(4 * 5)', 20],
    ['3 + (4 * 5)', 23],
    ['2 * 3 + 4', 10],
    ['2 * 3 + (4 * 5)', 26],
    ['5 + (8 * 3 + 9 + 3 * 4 * 3)', 437],
    ['5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240],
    ['((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632],
  ]
  for equation, expected in cases:
    actual = compute(0, '+', equation)
    logging.debug("Test: {} = {}, actual was {}".format(equation, expected, actual))
    assert(expected == actual)

def test2():
  cases = [
    ['2 * 3', 6],
    ['2 + 5', 7],
    ['(4 * 5)', 20],
    ['3 + (4 * 5)', 23],
    ['2 * 3 + 4', 14],
    ['2 * 3 + (4 * 5)', 46],
    ['1 + (2 * 3) + (4 * (5 + 6))', 51],
    ['5 + (8 * 3 + 9 + 3 * 4 * 3)', 1445],
    ['5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 669060],
    ['((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 23340],
  ]
  for equation, expected in cases:
    actual = compute2(equation)
    logging.debug("Test: {} = {}, actual was {}".format(equation, expected, actual))
    assert(expected == actual)

#test()
#total = 0
#for line in my_input:
#  total += compute(0, '+', line)
#logging.info("Part 1: sum of equation values: {}".format(total))

def apply(left, op, right):
  if op == '+':
    return left + right
  return left * right

# a + b * c
def apply_op(pieces, op):
  if len(pieces) == 1:
    return pieces
  remaining_pieces = []
  left = pieces.pop(0)
  while pieces:
    cop = pieces.pop(0)
    right = pieces.pop(0)
    if cop == op:
      remaining_pieces.append(apply(left, op, right))
    else:
      remaining_pieces.append(left)
      remaining_pieces.append(cop)
      remaining_pieces.append(right)
  return remaining_pieces

def compute_simple(equation):
  pieces = []
  for piece in equation.split(" "):
    if piece == '+' or piece == '*':
      pieces.append(piece)
    else:
      pieces.append(int(piece))
  pieces = apply_op(pieces, '+')
  pieces = apply_op(pieces, '*')
  if len(pieces) == 1:
    return int(pieces[0])
  else:
    return pieces

def is_simple(equation):
  return '(' not in equation

def rseek(haystack, needle):
  l = len(haystack)
  for i in range(l):
    location = l - i - 1
    if haystack[location] == needle:
      return location
  return None

def compute2(equation):
  while not is_simple(equation):
    logging.debug("{} is not simple".format(equation))
    last_opening_paren = rseek(equation, '(')
    last_closing_paren = find_closing_paren(equation, last_opening_paren)
    sub_eq = equation[last_opening_paren + 1:last_closing_paren]
    logging.debug("Simplifying {} by solving {} separately".format(equation, sub_eq))
    if is_simple(sub_eq):
      equation = equation[:last_opening_paren] + compute_simple(sub_eq) + equation[last_closing_paren+1:]
    else:
      logging.debug("Sub eq was not simple :( {}".format(sub_eq))
  logging.debug("equation is simple: {}".format(equation))
  return compute_simple(equation)


test2()
total = 0
for line in my_input:
  total += compute2(line)
logging.info("Part 2: sum of equation values: {}".format(total))