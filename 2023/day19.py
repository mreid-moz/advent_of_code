from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=19)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()


LT = '<'
GT = '>'

class Workflow:
    def __init__(self, line):
        self.line = line
        name, remainder = line.split('{')
        self.name = name
        remainder = remainder[:-1]
        self.rules = []
        rules = remainder.split(',')
        for rule in rules:
            if ':' in rule:
                criterion, target = rule.split(':')
                field = criterion[0]
                op = criterion[1]
                val = int(criterion[2:])
                self.rules.append((field, op, val, target))
            else:
                self.rules.append(('x',GT, 0, rule))

    def apply(self, part):
        for field, op, val, target in self.rules:
            pv = part[field]
            if op == LT:
                if pv < val:
                    return target
            elif op == GT:
                if pv > val:
                    return target

    def __str__(self):
        return self.line


def parse_part(line):
    part = {}
    fields = line[1:-1].split(',')
    for field in fields:
        k, v = field.split('=')
        v = int(v)
        part[k] = v
    return part


workflows = {}
parts = []
for line in lines:
    if line == '':
        continue

    if line[0] == '{':
        parts.append(parse_part(line))
    else:
        w = Workflow(line)
        workflows[w.name] = w

logging.info("Found {} parts and {} workflows".format(len(parts), len(workflows)))

buckets = defaultdict()
big_total = 0
for i, part in enumerate(parts):
    done = False
    dest = workflows['in'].apply(part)
    logging.debug("part {}: in -> {}".format(i, dest))
    while not done:
        if dest == 'A' or dest == 'R':
            done = True
        else:
            dest = workflows[dest].apply(part)
            logging.debug("part {}:    -> {}".format(i, dest))
    if dest == 'A':
        big_total += part['x'] + part['m'] + part['a'] + part['s']

logging.info("Overall total for accepted parts: {}".format(big_total))
if not TEST:
    p.answer_a = big_total

# px{a<2006:qkq,m>2090:A,rfg}
# pv{a>1716:R,A}
# lnx{m>1548:A,A}
# rfg{s<537:gd,x>2440:R,A}
# qs{s>3448:A,lnx}
# qkq{x<1416:A,crn}
# crn{x>2662:A,R}
# in{s<1351:px,qqz}
# qqz{s>2770:qs,m<1801:hdj,R}
# gd{a>3333:R,R}
# hdj{m>838:A,pv}

# Find any rules where everthing goes to A
# Recursively find cases where there are criteria to get to those

# A <- px{a>=2006,m>2090}
# A <- pv{a<=1716}
# A <- lnx
# A <- rfg{s>=537,x<=2440} # gd has no path to A
# A <- qs

# qs{s>3448:A,lnx}
# qkq{x<1416:A,crn}
# crn{x>2662:A,R}
# in{s<1351:px,qqz}
# qqz{s>2770:qs,m<1801:hdj,R}
# gd{a>3333:R,R}
# hdj{m>838:A,pv}
