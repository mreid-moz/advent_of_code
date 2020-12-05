import logging
from itertools import groupby
logging.basicConfig(level=logging.INFO)

class Reagent:
  def __init__(self, amount, chemical):
    self.amount = amount
    self.chemical = chemical

  def __str__(self):
    return "{} {}".format(self.amount, self.chemical)

  def __repr__(self):
    return str(self)

  def __hash__(self):
    return hash((self.amount, self.chemical))

  def __eq__(self, other):
    return (self.amount, self.chemical) == (other.amount, self.chemical)

  def is_ore(self):
    return self.chemical == 'ORE'

  def get_chemical(self):
    return self.chemical

class Nanofactory:
  def __init__(self, reactions_list):
    self.reactions = self.parse_reactions(reactions_list)

  def parse_reactions(self, reactions_list):
    logging.debug("Processing reactions:\n{}".format(reactions_list))
    lines = reactions_list.strip().split("\n")
    formulae = {}
    for line in lines:
      inputs, output = line.split(" => ")
      output_reagent = self.get_reagent(output)
      input_reagents = [ self.get_reagent(i) for i in inputs.split(", ") ]
      logging.debug("Parsed down to {} -> {}".format([str(r) for r in input_reagents], output_reagent))
      formulae[output_reagent] = input_reagents
    return formulae

  def get_reagent(self, reagent_description):
    # "10 ORE" or "7 D"
    amount, reagent = reagent_description.split(" ")
    return Reagent(int(amount), reagent)

  def all_ores(self, reagents):
    for r in reagents:
      if not r.is_ore():
        return False
    return True

  def minimum_ore(self, amount, chemical):
    desired_output = Reagent(amount, chemical)
    #if desired_output not in self.reactions:
    #  logging.error("Don't know how to make {} :(".format(desired_output))
    #  for o in self.reactions.values():
    #    logging.debug("We know how to make {}".format(o))
    #  return -1
    #lhs = self.reactions[desired_output]
    lhs = [desired_output]
    rhs = []

    logging.info("Trying to get from {} -> {}".format(lhs, rhs))

    while not self.all_ores(lhs):
      lhs, leftovers = self.simplify_general(lhs)
      if len(leftovers) > 0:
        rhs += leftovers

    logging.debug("Simplified LHS: {} -> {}".format(lhs, rhs))

    reduce_count = 0
    while not self.all_ores(rhs):
      reduce_count += 1
      rhs = self.reduce_reagents(rhs)
      rhs, leftovers = self.simplify_general(rhs, allow_create=False)
      rhs += leftovers
      #if reduce_count > 10:
      #  break
    logging.debug("Simplified RHS: {} -> {}".format(lhs, rhs))

    rhs_ore_count = sum([r.amount for r in rhs])
    logging.debug("We have {} ores on the RHS".format(rhs_ore_count))

    # Remove any un-reduced LHS entries
    uncancelled_lhs = []
    for reagent in lhs:
      if rhs_ore_count > 0 and rhs_ore_count >= reagent.amount:
        logging.debug("Canceling out {} in ores".format(reagent.amount))
        rhs_ore_count -= reagent.amount
      else:
        uncancelled_lhs.append(reagent)

    logging.debug("After canceling: {} -> {}".format(uncancelled_lhs, rhs_ore_count))

    return sum([i.amount for i in uncancelled_lhs]), rhs_ore_count

  def reduce_reagents(self, reagents):
    logging.debug("reducing {}".format(reagents))
    results = []
    for chemical, group in groupby(sorted(reagents, key=Reagent.get_chemical), key=Reagent.get_chemical):
      #print("group for {}: {}".format(chemical, list(group)))
      results.append(Reagent(sum([r.amount for r in list(group)]), chemical))
    logging.debug("reduced to {}".format(results))
    return results

  def simplify_general(self, reagents, allow_create=True):
    logging.debug("Attempting to simplify {}".format(reagents))

    reagents_out = []
    leftovers = []
    # Find something that has a reaction
    for i in range(len(reagents)):
      reagent = reagents[i]

      if reagent.is_ore():
        reagents_out.append(reagent)
        continue
      if reagent in self.reactions:
        logging.debug("Simplifying {} to {}".format(reagent, self.reactions[reagent]))
        reagents_out += self.reactions[reagent]
      else:
        # Look for one that produces more.
        for output in self.reactions.keys():
          if output.chemical == reagent.chemical:
            if output.amount > reagent.amount and allow_create:
              # This will do, but add some to the rhs.
              leftover = output.amount - reagent.amount
              reagents_out += self.reactions[output]
              leftovers.append(Reagent(leftover, output.chemical))
            elif output.amount < reagent.amount:
              # Subtract it, and try again.
              leftover = reagent.amount - output.amount
              reagents_out += self.reactions[output] + [Reagent(leftover, output.chemical)]
    return reagents_out, leftovers

class test_case:
  def __init__(self, reactions, min_ore):
    self.reactions = reactions
    self.min_ore = min_ore


test_cases = [
  test_case("""
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
""", 31),
  test_case("""
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
""", 165),
  test_case("""
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
""", 13312),
  test_case("""
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
""", 180697)

]

def test():
  factory = Nanofactory(test_cases[0].reactions)

  factory.reduce_reagents([Reagent(1, 'A'), Reagent(1, 'B'), Reagent(1, 'A'), Reagent(1, 'A'), Reagent(5, 'C')])
  #assert(factory.minimum_ore(1, 'B') == 1)
  #assert(factory.minimum_ore(1, 'FUEL') == 31)

  m, l = factory.minimum_ore(2, 'FUEL')
  print("Cost of 2 fuel: {}, with {} leftover (min {})".format(m, l, m-l))

  for t in test_cases:
    factory = Nanofactory(t.reactions)
    m, l = factory.minimum_ore(1, 'FUEL')
    logging.info("Expected: {}. Actual: min {}, leftover {}, net {}".format(t.min_ore, m, l, m - l))
    assert(m - l == t.min_ore)
    m, l = factory.minimum_ore(2, 'FUEL')
    logging.info("For 2 fuel: min {}, leftover {}, net {}".format(m, l, m - l))

test()

with open("input") as fin:
  formula = fin.read()

factory = Nanofactory(formula)

m, l = factory.minimum_ore(1, 'FUEL')
print("Minimum ore required for 1: {} with {} leftover. Net {}".format(m, l, m-l))

#m, l = factory.minimum_ore(3, 'FUEL')
#print("Minimum ore required for 3: {} with {} leftover. Net {}".format(m, l, m-l))
#
#m, l = factory.minimum_ore(10, 'FUEL')
#print("Minimum ore required for 10: {} with {} leftover. Net {}".format(m, l, m-l))

t = 1000000000000
for opf, result in [(13312,82892753), (180697,5586022), (2210736,460664)]:
  print("With ore-per-fuel {}, we get {}. Naive: {}. Ratio: {}/{}={}".format(
    opf, result, t/opf, result, t/opf, result/(t/opf)))