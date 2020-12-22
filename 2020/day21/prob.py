import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

p = re.compile('^([a-z ]+) \(contains ([a-z ,]+)\)$')

class IngredsList:
  def __init__(self, line):
    m = p.match(line)
    self.ingredients = set(m.group(1).split(' '))
    self.allergens = set(m.group(2).split(', '))

ingred_list = [IngredsList(line) for line in my_input]

all_possible_ingredients = set()
all_possible_allergens = set()
for i in ingred_list:
  all_possible_allergens.update(i.allergens)
  all_possible_ingredients.update(i.ingredients)

logging.debug("All possible ingredients: {}".format(all_possible_ingredients))
logging.debug("All possible allergens: {}".format(all_possible_allergens))

known_allergens = {}

id_count = 1
while id_count > 0:
  id_count = 0
  for allergen in all_possible_allergens:
    logging.debug("Looking for common ingredient for {}".format(allergen))
    possible_ingredients = None
    for i in ingred_list:
      if allergen in i.allergens:
        if possible_ingredients is None:
          possible_ingredients = i.ingredients.copy()
        else:
          possible_ingredients &= i.ingredients
        logging.debug("Narrowed {} down to {}".format(allergen, possible_ingredients))
    possible_ingredients -= set(known_allergens.keys())
    if len(possible_ingredients) == 1:
      winner = possible_ingredients.pop()
      known_allergens[winner] = allergen
      logging.debug("Ingredient {} has allergen {}".format(winner, allergen))
      id_count += 1

safe_count = 0
for il in ingred_list:
  if len(il.allergens - set(known_allergens.values())) == 0:
    remaining_ingreds = len(il.ingredients - set(known_allergens.keys()))
    logging.debug("After removing known allergens we had {} left".format(remaining_ingreds))
    safe_count += remaining_ingreds
logging.info("Part 1: there are {} allergen-free ingredients".format(safe_count))

sorted_ingredients = sorted(known_allergens.keys(), key=lambda x: known_allergens[x])
logging.info("Part 2: canonical danger: {}".format(','.join(sorted_ingredients)))