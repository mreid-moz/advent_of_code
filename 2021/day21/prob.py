import logging
import re
import sys
import copy
from collections import defaultdict
from functools import reduce
import random

logging.basicConfig(level=logging.INFO)

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

example = False
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

def apply_roll(name, player_position, roll, track_length=10):
  new_position = player_position + roll
  if new_position > track_length:
    new_position -= track_length
  logging.debug(f"Moving {name} {player_position} + {roll} -> {new_position}")
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
#def check_recursive(p1_pos, p1_score, p2_pos, p2_score, rolls_so_far):
#  if p1_score > 21 or p2_score > 21:
#    multiplier = reduce((lambda x, y: x * y), [multipliers[r] for r in rolls_so_far])
#  if p1_score > 21:
#    logging.debug(f"Player 1 won after {rolls_so_far}, multiplier = {multiplier}")
#    return multiplier, 0
#  if p2_score > 21:
#    logging.debug(f"Player 2 won after {rolls_so_far}, multiplier = {multiplier}")
#    return 0, multiplier
#
#  p1_wins = 0
#  p2_wins = 0
#  for r in three_roll_values:
#    if len(rolls_so_far) % 2 == 0:
#      p1_pos = apply_roll('p1', p1_pos, r)
#      p1_score += p1_pos
#    else:
#      p2_pos = apply_roll('p2', p2_pos, r)
#      p2_score += p2_pos
#    logging.debug(f"P1 score {p1_score}, P2: {p2_score}")
#    (p1w, p2w) = check_recursive(p1_pos, p1_score, p2_pos, p2_score, rolls_so_far + [r])
#    p1_wins += p1w
#    p2_wins += p2w
#  return p1_wins, p2_wins
#
#p1_wins, p2_wins = check_recursive(p1_start, 0, p2_start, 0, [])
#
#logging.info(f"Player 1 won {p1_wins}, player 2 won {p2_wins}")

memo = {}

def play_one(state, roll, modulo):
  p1_pos, p1_score, p2_pos, p2_score = state

  p1 = Player('p1', p1_pos, p1_score)
  p2 = Player('p2', p2_pos, p2_score)

  if modulo:
    p2.move(roll)
  else:
    p1.move(roll)

  return p1, p2


def play(rolls):
  t = tuple(rolls[:-1])
  if t in memo:
    #logging.info("cache hit")
    p1, p2 = play_one(memo[t], rolls[-1], len(rolls) % 2)
    memo[tuple(rolls)] = (p1.pos, p1.score, p2.pos, p2.score)
    if p1.won():
      return 'p1'
    elif p2.won():
      return 'p2'
  else:
    logging.info(f"cache miss {t}")

  p1 = Player("p1", p1_start)
  p2 = Player("p2", p2_start)
  for i, r in enumerate(rolls):
    if i % 2 == 0:
      p1.move(r)
    else:
      p2.move(r)
  memo[t] = (p1.pos, p1.score, p2.pos, p2.score)
  if p1.won():
    return 'p1'
  if p2.won():
    return 'p2'
  return None


class Game:
  def __init__(self, p1_pos, p2_pos):
    self.p1_pos = p1_pos
    self.p2_pos = p2_pos
    self.p1_score = 0
    self.p2_score = 0
    self.num_rolls = 0
    self.multiplier = 1

  def __str__(self):
    return f"after {self.num_rolls} rolls, p1: {self.p1_pos} ({self.p1_score}), p2: {self.p2_pos} ({self.p2_score})"

  def winner(self):
    if self.p1_score >= 21:
      return 'p1'
    if self.p2_score >= 21:
      return 'p2'
    return None

  def apply_roll(self, roll):
    self.multiplier *= multipliers[roll]
    if self.num_rolls % 2 == 0:
      # p1
      new_position = self.p1_pos + roll
      if new_position > 10:
        new_position -= 10
      self.p1_score += new_position
      #logging.debug(f"Moving p1 from {self.p1_pos} + {roll} -> {new_position}, score={self.p1_score}")
      self.p1_pos = new_position
    else:
      # p2
      new_position = self.p2_pos + roll
      if new_position > 10:
        new_position -= 10
      self.p2_score += new_position
      #logging.debug(f"Moving p2 from {self.p2_pos} + {roll} -> {new_position}, score={self.p2_score}")
      self.p2_pos = new_position
    self.num_rolls += 1

p1_wins = 0
p2_wins = 0
games = [Game(p1_start, p2_start)]
game_count = 0
while games:
  game_count += 1
  if game_count % 10000 == 0:
    logging.info(f"Played {game_count} games. So far: p1 {p1_wins}, p2 {p2_wins}. {len(games)} games in queue")
  current_game = games.pop(0)
  logging.debug(current_game)
  winner = current_game.winner()
  if winner == 'p1':
    logging.debug(f"p1 wins {current_game.multiplier}: {current_game}")
    p1_wins += current_game.multiplier
  elif winner == 'p2':
    logging.debug(f"p2 wins {current_game.multiplier}: {current_game}")
    p2_wins += current_game.multiplier
  else:
    for r in three_roll_values:
      new_game = copy.deepcopy(current_game)
      new_game.apply_roll(r)
      games.append(new_game)

logging.info(f"Player 1 won {p1_wins}, player 2 won {p2_wins}")


