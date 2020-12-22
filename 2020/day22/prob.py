import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

p1_cards = []
p2_cards = []
target = p1_cards
for line in my_input:
  if line == '':
    continue
  if line == 'Player 1:':
    target = p1_cards
  elif line == 'Player 2:':
    target = p2_cards
  else:
    target.append(line)

def reverse(s):
  return s[::-1]

class Player:
  def __init__(self, n, cards):
    self.player_num = n
    self.deck = [int(c) for c in cards]

  def copy(self, count):
    deck = self.deck[:count]
    return Player(self.player_num, deck)

  def deck_str(self):
    return ','.join([str(c) for c in self.deck])

  def print(self):
    logging.debug("Player {}: {}".format(self.player_num, self.deck_str()))

  def next_card(self):
    return self.deck.pop(0)

  def score(self):
    multipliers = reverse(range(1, len(self.deck)+1))
    score = 0
    for m, c in zip(self.deck, multipliers):
      score += m * c
    return score

  def collect(self, card1, card2):
    self.deck.append(card1)
    self.deck.append(card2)

  def alive(self):
    return len(self.deck) > 0

class Game:
  def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2
    self.round_count = 0

  def copy(self, player1_count, player2_count):
    p1c = self.p1.copy(player1_count)
    p2c = self.p2.copy(player2_count)
    return Game(p1c, p2c)

  def round(self):
    p1v = self.p1.next_card()
    p2v = self.p2.next_card()
    if p1v > p2v:
      self.p1.collect(p1v, p2v)
    else:
      self.p2.collect(p2v, p1v)

  def play(self):
    while self.p1.alive() and self.p2.alive():
      self.round()
      self.round_count += 1
      logging.debug("After round {}:".format(self.round_count))
      self.p1.print()
      self.p2.print()
    return self.p1.score() + self.p2.score()

  def get_state(self):
    return "{}|{}".format(self.p1.deck_str(), self.p2.deck_str())

  def play_recursive(self, seen):
    winner = None
    while self.p1.alive() and self.p2.alive():
      self.round_count += 1
      current_state = self.get_state()
      logging.debug("Start of round {}: {}".format(self.round_count, current_state))
      if current_state in seen:
        logging.debug("We've already seen this state, p1 wins!")
        winner = self.p1
        break
      seen.add(current_state)

      p1v = self.p1.next_card()
      p2v = self.p2.next_card()

      logging.debug("Player 1 plays {}, player 2 plays {}".format(p1v, p2v))

      if len(self.p1.deck) >= p1v and len(self.p2.deck) >= p2v:
        subgame_winner = self.copy(p1v, p2v).play_recursive(set())
        if subgame_winner.player_num == 1:
          winner = self.p1
        else:
          winner = self.p2
        logging.debug("Player {} won a sub-game".format(winner.player_num))
      else:
        if p1v > p2v:
          winner = self.p1
        else:
          winner = self.p2

      logging.debug("Player {} collects winning cards {} and {}".format(winner.player_num, p1v, p2v))
      if winner.player_num == 1:
        winner.collect(p1v, p2v)
      else:
        winner.collect(p2v, p1v)
      logging.debug("End of round {}: {}".format(self.round_count, self.get_state()))
    return winner

game = Game(Player(1, p1_cards), Player(2, p2_cards))
score = game.play()
logging.info("Part 1: Score was {}".format(score))

game2 = Game(Player(1, p1_cards), Player(2, p2_cards))
logging.debug("Game 2 state: {}".format(game2.get_state()))
winner = game2.play_recursive(set())
logging.info("Part 2: Score was {}".format(winner.score()))
