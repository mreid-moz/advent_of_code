import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [int(l.strip()) for l in fin.readlines()]

card_pub_key, door_pub_key = my_input

logging.debug("Card key: {}. Door key: {}".format(card_pub_key, door_pub_key))

def transform_subject(subject, loop_size):
  v = 1
  for i in range(loop_size):
    v *= subject
    v = v % 20201227
  return v

def find_loop_size(subject, target_key, max_loop=1000000000):
  v = 1
  for i in range(max_loop):
    v *= subject
    v = v % 20201227
    if v == target_key:
      return i + 1

card_loop = find_loop_size(7, card_pub_key)
logging.debug("Card loop size: {}".format(card_loop))

door_loop = find_loop_size(7, door_pub_key)
logging.debug("Door loop size: {}".format(door_loop))

encryption_key = transform_subject(door_pub_key, card_loop)
logging.info("Part 1: Encryption key: {}".format(encryption_key))

