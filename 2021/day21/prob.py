import logging
import re
import sys
from collections import defaultdict
from functools import reduce
import random

logging.basicConfig(level=logging.DEBUG)

class Die:
  def __init__(self, num_sides=100):
    self.num_sides = num_sides
    self.last_roll = num_sides
    self.num_rolls = 0

  def roll(self):
    self.last_roll += 1
    if self.last_roll > self.num_sides:
      self.last_roll = 1

    self.num_rolls += 1
    return self.last_roll

  def roll3(self):
    return (self.roll(), self.roll(), self.roll())

class FixDie:
  def __init__(self, val):
    self.val = val
    self.num_rolls = 0

  def roll(self):
    self.num_rolls += 1
    return self.val

  def roll3(self):
    return (self.roll(), self.roll(), self.roll())

class RanDie:
  def __init__(self, val):
    self.val = val
    self.num_rolls = 0

  def roll(self):
    self.num_rolls += 1
    return random.randint(1, self.val)

  def roll3(self):
    return (self.roll(), self.roll(), self.roll())

def advance(name, pos, roll, track_length=10):
  p_orig = pos
  p_new = pos + sum(roll)
  while p_new > track_length:
    p_new -= track_length
  #logging.debug(f"{name} rolled {roll}, advancing from {p_orig} to {p_new}")
  return p_new

def play(die, winning_score, p1_start, p2_start, track_length=10):
  p1 = p1_start
  p2 = p2_start
  p1_score = 0
  p2_score = 0

  while p1_score < winning_score and p2_score < winning_score:
    p1_roll = die.roll3()
    p1 = advance("P1", p1, p1_roll)
    p1_score += p1
    if p1_score >= winning_score:
      logging.debug(f"P1 won {p1_score}. P2 had {p2_score}")
      break

    p2_roll = die.roll3()
    p2 = advance("P2", p2, p2_roll)
    p2_score += p2
    #logging.debug(f"P1: {p1_score}  P2: {p2_score}")
  return p1_score, p2_score

p1_start = 8
p2_start = 4

example = True
if example:
  p1_start = 4
  p2_start = 8

#d = Die()
#p1_score, p2_score = play(d, 1000, p1_start, p2_start)
#loser = p2_score
#if p1_score < p2_score:
#  logging.debug(f"P2 won {p2_score}. P1 had {p1_score}.")
#  loser = p1_score
#logging.info(f"Loser {loser} x {d.num_rolls} rolls = {loser * d.num_rolls}")
#
#one_roller = FixDie(1)
#p1_score, p2_score = play(one_roller, 21, p1_start, p2_start)
#logging.info(f"with a die that always rolls one, it took {one_roller.num_rolls} rolls: P1={p1_score}, P2={p2_score}")
#
#two_roller = FixDie(2)
#p1_score, p2_score = play(two_roller, 21, p1_start, p2_start)
#logging.info(f"with a die that always rolls two, it took {two_roller.num_rolls} rolls: P1={p1_score}, P2={p2_score}")
#
#three_roller = FixDie(3)
#p1_score, p2_score = play(three_roller, 21, p1_start, p2_start)
#logging.info(f"with a die that always rolls three, it took {three_roller.num_rolls} rolls: P1={p1_score}, P2={p2_score}")
#
#dist = defaultdict(int)
#p1_wins = 0
#p2_wins = 0
#iterations = 0
#for i in range(iterations):
#  rando_roller = RanDie(3)
#  p1_score, p2_score = play(rando_roller, 21, p1_start, p2_start)
#  if p1_score > p2_score:
#    p1_wins += 1
#  else:
#    p2_wins += 1
#  dist[rando_roller.num_rolls] += 1
#
#logging.info(f"After {iterations} iterations, player 1 won {p1_wins} and p2 won {p2_wins}")
#for k in sorted(dist.keys()):
#  logging.info(f"It took {k} rolls {dist[k]} times.")

#             1                          2                          3
#     /       |       \          /       |       \          /       |       \
#    1        2        3        1        2        3        1        2        3
#  / | \    / | \    / | \    / | \    / | \    / | \    / | \    / | \    / | \
# 1  2  3  1  2  3  1  2  3  1  2  3  1  2  3  1  2  3  1  2  3  1  2  3  1  2  3
# ...
#  repeat between 15 and 27 times.


def apply_roll(player_position, roll, track_length=10):
  new_position = player_position + roll
  if new_position > track_length:
    new_position -= track_length
  logging.debug(f"Moving {player_position} + {roll} -> {new_position}")
  return new_position

multipliers = {
  3: 1,
  4: 3,
  5: 6,
  6: 7,
  7: 6,
  8: 3,
  9: 1,
}

three_roll_values = sorted(list(multipliers.keys()))

class Player:
  def __init__(self, name, pos, score=0):
    self.name = name
    self.pos = pos
    self.score = 0
    self.wins = 0

  def move(self, roll):
    new_position = self.pos + roll
    if new_position > 10:
      new_position -= 10
    self.score += new_position
    logging.debug(f"Moving {self.name} from {self.pos} + {roll} -> {new_position}, score={self.score}")
    self.pos = new_position

  def won(self):
    if self.score >= 21:
      return True
    return False

p1 = Player("p1", p1_start)
p2 = Player("p2", p2_start)


def check_recursive(p1_pos, p1_score, p2_pos, p2_score, rolls_so_far):
  if p1_score > 21 or p2_score > 21:
    multiplier = reduce((lambda x, y: x * y), [multipliers[r] for r in rolls_so_far])
  if p1_score > 21:
    logging.debug(f"Player 1 won after {rolls_so_far}, multiplier = {multiplier}")
    return multiplier, 0
  if p2_score > 21:
    logging.debug(f"Player 2 won after {rolls_so_far}, multiplier = {multiplier}")
    return 0, multiplier

  p1_wins = 0
  p2_wins = 0
  for r in three_roll_values:
    if len(rolls_so_far) % 2 == 0:
      p1_pos = apply_roll(p1_pos, r)
      p1_score += p1_pos
    else:
      p2_pos = apply_roll(p2_pos, r)
      p2_score += p2_pos
    (p1w, p2w) = check_recursive(p1_pos, p1_score, p2_pos, p2_score, rolls_so_far + [r])
    p1_wins += p1w
    p2_wins += p2w
  return p1_wins, p2_wins

p1_wins, p2_wins = check_recursive(p1_start, 0, p2_start, 0, [])

logging.info(f"Player 1 won {p1_wins}, player 2 won {p2_wins}")

#for a in three_roll_values:
#  win_multiplier = multipliers[a]
#  p1.move(a)
#  for b in three_roll_values:
#    logging.debug(f"looking at rolls starting with {a}, {b}")
#    win_multiplier *= multipliers[b]
#    p2.move(b)
#    for c in three_roll_values:
#      win_multiplier *= multipliers[c]
#      p1.move(c)
#      for d in three_roll_values:
#        win_multiplier *= multipliers[d]
#        p2.move(d)
#        for e in three_roll_values:
#          win_multiplier *= multipliers[e]
#          p1.move(e)
#          if p1.won():
#            logging.debug(f"Player 1 won with score {p1.score} after {(a, b, c, d, e)}, p2 score was {p2.score}")
#            p1.wins += win_multiplier
#            break
#          for f in three_roll_values:
#            win_multiplier *= multipliers[f]
#            p2.move(f)
#            if p2.won():
#              logging.debug(f"Player 2 won with score {p2.score} after {(a, b, c, d, e, f)}, p1 score was {p1.score}")
#              p2.wins += win_multiplier
#              break
#            for g in three_roll_values:
#              win_multiplier *= multipliers[g]
#              p1.move(g)
#              if p1.won():
#                logging.debug(f"Player 1 won with score {p1.score} after {(a, b, c, d, e, f, g)}, p2 score was {p2.score}")
#                p1.wins += win_multiplier
#                break
#              for h in three_roll_values:
#                win_multiplier *= multipliers[h]
#                p2.move(h)
#                if p2.won():
#                  logging.debug(f"Player 2 won with score {p2.score} after {(a, b, c, d, e, f, g, h)}, p1 score was {p1.score}")
#                  p2.wins += win_multiplier
#                  break
#                for i in three_roll_values:
#                  win_multiplier *= multipliers[i]
#                  p1.move(i)
#                  if p1.won():
#                    logging.debug(f"Player 1 won with score {p1.score} after {(a, b, c, d, e, f, g, h, i)}, p2 score was {p2.score}")
#                    p1.wins += win_multiplier
#                    break
#                  for j in three_roll_values:
#                    win_multiplier *= multipliers[j]
#                    p2.move(j)
#                    if p2.won():
#                      logging.debug(f"Player 2 won with score {p2.score} after {(a, b, c, d, e, f, g, h, i, j)}, p1 score was {p1.score}")
#                      p2.wins += win_multiplier
#                      break
#                    for k in three_roll_values:
#                      win_multiplier *= multipliers[k]
#                      p1.move(k)
#                      if p1.won():
#                        logging.debug(f"Player 1 won with score {p1.score} after {(a, b, c, d, e, f, g, h, i, j, k)}, p2 score was {p2.score}")
#                        p1.wins += win_multiplier
#                        break
#                      else:
#                        logging.warning("Neither player won after like 11 rolls, wtf.")

#logging.info(f"Player 1 won {p1.wins}, player 2 won {p2.wins}")



