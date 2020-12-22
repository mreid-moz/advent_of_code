import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

p1 = []
p2 = []
target = p1
for line in my_input:
  if line == '':
    continue
  if line == 'Player 1:':
    target = p1
  elif line == 'Player 2:':
    target = p2
  else:
    target.append(line)

def reverse(s):
  return s[::-1]

class Player:
  def __init__(self, n, cards):
    self.player_num = n
    self.deck = [int(c) for c in cards]

  def print(self):
    logging.debug("Player {}: {}".format(self.player_num, self.deck))

  def next_card(self):
    return self.deck.pop(0)

  def score(self):
    multipliers = reverse(range(1, len(self.deck)+1))
    score = 0
    for m, c in zip(self.deck, multipliers):
      score += m * c
    return score

  def collect(self, card1, card2):
    self.deck.append(max(card1, card2))
    self.deck.append(min(card1, card2))

  def alive(self):
    return len(self.deck) > 0

class Game:
  def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2
    self.round_count = 0

  def round(self):
    p1v = self.p1.next_card()
    p2v = self.p2.next_card()
    if p1v > p2v:
      self.p1.collect(p1v, p2v)
    else:
      self.p2.collect(p1v, p2v)

  def play(self):
    while self.p1.alive() and self.p2.alive():
      self.round()
      self.round_count += 1
      logging.debug("After round {}:".format(self.round_count))
      self.p1.print()
      self.p2.print()
    return self.p1.score() + self.p2.score()

player1 = Player(1, p1)
player2 = Player(2, p2)
game = Game(player1, player2)
score = game.play()
logging.info("Part 1: Score was {}".format(score))
