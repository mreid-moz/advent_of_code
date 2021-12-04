import logging
import copy
import sys

logging.basicConfig(level=logging.INFO)

class  BingoBoard:
  def __init__(self, lines):
    self.grid = []
    for line in lines:
      self.grid.append([item.strip() for item in line.split()])

  def print(self):
    logging.debug("--- start ---")
    for row in self.grid:
      logging.debug(row)
    logging.debug("---  end  ---")

  def score(self):
    sum = 0
    for row in self.grid:
      for v in row:
        if v != 'x':
          sum += int(v)
    return sum

  def winning(self, row, col):
    l = len(self.grid)
    # check row
    winning = True
    for i in range(l):
      if self.grid[i][col] != 'x':
        winning = False
        break
    if winning:
      return winning

    # check column
    winning = True
    for i in range(l):
      if self.grid[row][i] != 'x':
        winning = False
        break
    if winning:
      return winning

    # I could've sworn it said diagonals _do_ count...

    #if row == col:
    #  winning = True
    #  # check diagonal
    #  for i in range(l):
    #    #logging.debug("checking diag ({},{})".format(i, i))
    #    if self.grid[i][i] != 'x':
    #      winning = False
    #      break
    #  if winning:
    #    return winning

    #if row == l - col - 1:
    #  winning = True
    #  # check other diagonal
    #  for i in range(l):
    #    #logging.debug("checking other diag ({},{})".format(i, l - i - 1))
    #    if self.grid[i][l - i - 1] != 'x':
    #      winning = False
    #      break

    return winning

  def apply(self, target):
    for i, row in enumerate(self.grid):
      for j, v in enumerate(row):
        if v == target:
          self.grid[i][j] = 'x'
          # check if we're winning now.
          if self.winning(i, j):
            return self.score()
    return None

boards_orig = []

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  lines = fin.readlines()
  bingo_nums = lines[0].strip().split(',')
  for i in range(1, len(lines) - 1, 6):
    boards_orig.append(BingoBoard(lines[i+1:i+6]))

boards = copy.deepcopy(boards_orig)
for n in bingo_nums:
  logging.info("Calling bingo number {}!".format(n))
  win = False
  for b in boards:
    result = b.apply(n)
    if result is not None:
      logging.info("Found a winner with score {}".format(result * int(n)))
      win = True
      break
  if win:
    break

# Part 2
max_moves_to_win = 0
max_moves_score = None
boards = copy.deepcopy(boards_orig)

for i, b in enumerate(boards):
  for j, n in enumerate(bingo_nums):
    result = b.apply(n)
    logging.debug("Board {} after {} moves:".format(i, j+1))
    b.print()
    if result is not None:
      current_moves = j + 1
      current_score = result * int(n)
      logging.info("Board {} wins after {} moves with score {}".format(i, current_moves, current_score))
      if current_moves > max_moves_to_win:
        max_moves_to_win = current_moves
        max_moves_score = current_score
      break

logging.info("Last board wins after {} moves with score {}".format(max_moves_to_win, max_moves_score))
