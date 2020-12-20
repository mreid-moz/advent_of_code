import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

class DummyRule:
  def __init__(self, num):
    self.rule_num = num

  def is_dummy(self):
    return True

class Rule:
  def __init__(self, line):
    self.rule_num, self.rule_text = line.split(":")
    self.rule_text = self.rule_text.strip()
    self.ready = False
    self.match_target = None
    self.components = []
    if self.rule_text[0] == '"':
      self.match_target = self.rule_text[1:-1]
      self.ready = True
    else:
      for component in self.rule_text.split(" | "):
        self.components.append([DummyRule(c) for c in component.split(" ")])

  def __str__(self):
    match_text = self.match_target
    if match_text is None:
      match_text = " | ".join([" ".join([n.rule_num for n in c]) for c in self.components])
    return "Rule {}: {}".format(self.rule_num, match_text)

  def is_dummy(self):
    return False

  def match(self, message):
    if not self.ready:
      raise Exception("not ready")

    if self.match_target is not None:
      return message == self.match_target

    # TODO: implement the re stuff here instead.
    logging.debug("Match: {}".format(self))
    return message == self.match_target

  def get_dependencies(self):
    if len(self.components) == 0:
      return []

    deps = set()
    for component in self.components:
      for subcomponent in component:
        if subcomponent.is_dummy():
          deps.add(subcomponent)

    return deps

  def add_components(self, ready_rules):
    replacement_count = 0
    dummy_count = 0
    for component in self.components:
      for i, subcomponent in enumerate(component):
        logging.debug("Attempting to replace subcomponent {}".format(subcomponent.rule_num))
        if subcomponent.is_dummy() and subcomponent.rule_num in ready_rules:
          # swap in the actual rule.
          #logging.debug("subcomponent {} fits".format(subcomponent.rule_num))
          component[i] = ready_rules.get(subcomponent.rule_num)
          replacement_count += 1
        elif subcomponent.is_dummy():
          #logging.debug("subcomponent {} does not fit".format(subcomponent.rule_num))
          dummy_count += 1
        else:
          logging.debug("subcomponent {} is already not a dummy".format(subcomponent.rule_num))
    if dummy_count == 0:
      logging.debug("Rule {} is now ready!".format(self.rule_num))
      self.ready = True
    return replacement_count


input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

empty_line = my_input.index('')
rule_lines = my_input[:empty_line]
messages = my_input[empty_line+1:]

def parse_rules(rule_lines):
  rules = {}
  for line in rule_lines:
    rule = Rule(line)
    rules[rule.rule_num] = rule
  return rules

def rule_to_re(rule, r42=None, r31=None):
  be_weird = True # Set to False for part 1, True for part 2.
  if be_weird and rule.rule_num == '11':
    special = '({0}{1}|{0}{{2}}{1}{{2}}|{0}{{3}}{1}{{3}}|{0}{{4}}{1}{{4}}|{0}{{5}}{1}{{5}}|{0}{{6}}{1}{{6}})'.format(r42, r31)
    logging.debug("Special case for rule 11: {}".format(special))
    return special
  suffix = ''
  if be_weird and rule.rule_num == '8':
    logging.debug("Making 8 repeat")
    suffix = '+'

  if rule.match_target:
    return rule.match_target

  re_comps = []
  for c in rule.components:
    subs = ''.join([rule_to_re(s, r42, r31) for s in c])
    re_comps.append(subs)

  # named groups - it doesn't work because of repeated rule names.
  #XX final_re = '(?P<rule{}>'.format(rule.rule_num) + '|'.join(re_comps) + ')' + suffix
  final_re = '(' + '|'.join(re_comps) + ')' + suffix
  if suffix == '+':
    logging.debug("Rule 8: {}".format(final_re))
  return final_re


rules = parse_rules(rule_lines)
ready_rules = {}
iters = 0
while '0' not in ready_rules:
  iters += 1
  if iters == 100:
    break
  logging.debug("We have {} ready rules, and {} that aren't yet ready".format(len(ready_rules), len(rules)))
  to_delete = set()
  for n, r in rules.items():
    if r.ready:
      ready_rules[n] = r
      to_delete.add(n)
    else:
      added = r.add_components(ready_rules)
      logging.debug("Added {} components to rule {}".format(added, n))
  for n in to_delete:
    del rules[n]

# 0: 4 1 5 -> a((aa|bb)(ab|ba)|(ab|ba)(aa|bb))b
# 1: 2 3 | 3 2 -> (aa|bb)(ab|ba)|(ab|ba)(aa|bb)
# 2: 4 4 | 5 5 -> aa|bb
# 3: 4 5 | 5 4 -> ab|ba
# 4: "a" -> a
# 5: "b" -> b
# Actual: ^(a((aa|bb)(ab|ba)|(ab|ba)(aa|bb))b)$
r42 = rule_to_re(ready_rules['42'])
r31 = rule_to_re(ready_rules['31'])
r8 = rule_to_re(ready_rules['8'], r42, r31)
r11 = rule_to_re(ready_rules['11'], r42, r31)
r14 = rule_to_re(ready_rules['14'], r42, r31)
logging.debug("Rule 42: {} ({})".format(r42, ready_rules['42']))
logging.debug("Rule 31: {} ({})".format(r31, ready_rules['31']))
logging.debug("Rule 11: {} ({})".format(r11, ready_rules['11']))
logging.debug("Rule 14: {} ({})".format(r14, ready_rules['14']))
logging.debug("Rule  8: {} ({})".format(r8, ready_rules['8']))

#rule_zero_re = '^' + rule_to_re(ready_rules['0'], r42, r31) + '$'
rule_zero_re = rule_to_re(ready_rules['0'], r42, r31) + '$'
logging.debug("Rule 0: {}".format(rule_zero_re))
p = re.compile('^' + rule_zero_re)
#p = re.compile('({})({})$'.format(r8, r11))

def test():
  t = [
    'bbabbbbaabaabba',
    'babbbbaabbbbbabbbbbbaabaaabaaa',
    'aaabbbbbbaaaabaababaabababbabaaabbababababaaa',
    'bbbbbbbaaaabbbbaaabbabaaa',
    'bbbababbbbaaaaaaaabbababaaababaabab',
    'ababaaaaaabaaab',
    'ababaaaaabbbaba',
    'baabbaaaabbaaaababbaababb',
    'abbbbabbbbaaaababbbbbbaaaababb',
    'aaaaabbaabaaaaababaa',
    'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa',
    'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba',
  ]

  for m in t:
    #for i in range(1, 43):
    #  if str(i) in ready_rules:
    #    rule_re = rule_to_re(ready_rules[str(i)], r42, r31)
    #    logging.info("Checking {} against rule {} which is {}".format(m, i, rule_re))
    #    assert(re.match('.*' + rule_re, m))
    #    logging.info("  match.")
    logging.debug("Checking {} against rule 0 which is {}".format(m, rule_zero_re))
    assert(re.match('.*' + rule_zero_re, m))
    logging.debug("  match.")

if input_file == 't2':
  test()

match_count = 0
for message in messages:
  if p.match(message):
    logging.debug("Matched message: {}".format(message))
    match_count += 1

logging.info("Part 2: Rule 0 matches {} messages".format(match_count))
