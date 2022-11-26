from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2018, day=5)

reacts = re.compile(r"aA|bB|cC|dD|eE|fF|gG|hH|iI|jJ|kK|lL|mM|nN|oO|pP|qQ|rR|sS|tT|uU|vV|wW|xX|yY|zZ|Aa|Bb|Cc|Dd|Ee|Ff|Gg|Hh|Ii|Jj|Kk|Ll|Mm|Nn|Oo|Pp|Qq|Rr|Ss|Tt|Uu|Vv|Ww|Xx|Yy|Zz")

polymer = p.input_data

def reduce(polymer):
  return reacts.sub("", polymer)

def fully_reduce(polymer):
  current = reduce(polymer)
  while True:
    len_before = len(current)
    current = reduce(current)
    len_after = len(current)
    if len_before == len_after:
      return current

p.answer_a = len(fully_reduce(polymer))

shortest = len(polymer)

for pair in ["[aA]", "[bB]", "[cC]", "[dD]", "[eE]", "[fF]", "[gG]", "[hH]", "[iI]", "[jJ]", "[kK]", "[lL]", "[mM]", "[nN]", "[oO]", "[pP]", "[qQ]", "[rR]", "[sS]", "[tT]", "[uU]", "[vV]", "[wW]", "[xX]", "[yY]", "[zZ]"]:
  logging.debug(f"Trying with removed {pair}")
  modded_polymer = re.sub(pair, "", polymer)
  reduced = fully_reduce(modded_polymer)
  if len(reduced) < shortest:
    shortest = len(reduced)

p.answer_b = shortest



