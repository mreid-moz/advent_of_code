from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2024, day=21)

TEST = False
if TEST:
    # lines = p.examples[0].input_data.splitlines()
    lines = [
        "029A",
        "980A",
        "179A",
        "456A",
        "379A",
    ]
else:
    lines = p.input_data.splitlines()

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
code_map = {
    ('A','0'): '<',
    ('A','1'): '^<<',
    ('A','2'): '^<',
    ('A','3'): '^',
    ('A','4'): '^^<<',
    ('A','5'): '^^<',
    ('A','6'): '^^',
    ('A','7'): '^^^<<',
    ('A','8'): '^^^<',
    ('A','9'): '^^^',

    ('0','A'): '>',
    ('0','1'): '^<',
    ('0','2'): '^',
    ('0','3'): '^>',
    ('0','4'): '^^<',
    ('0','5'): '^^',
    ('0','6'): '^^>',
    ('0','7'): '^^^<',
    ('0','8'): '^^^',
    ('0','9'): '^^^>',

    ('1','0'): '>v',
    ('1','A'): '>>v',
    ('1','2'): '>',
    ('1','3'): '>>',
    ('1','4'): '^',
    ('1','5'): '^>',
    ('1','6'): '^>>',
    ('1','7'): '^^',
    ('1','8'): '^^>',
    ('1','9'): '^^>>',

    ('2','0'): 'v',
    ('2','1'): '<',
    ('2','A'): '>v',
    ('2','3'): '>',
    ('2','4'): '^<',
    ('2','5'): '^',
    ('2','6'): '^>',
    ('2','7'): '^^<',
    ('2','8'): '^^',
    ('2','9'): '^^>',

    ('3','0'): 'v>',
    ('3','1'): '<<',
    ('3','2'): '<',
    ('3','A'): 'v',
    ('3','4'): '^<<',
    ('3','5'): '^<',
    ('3','6'): '^',
    ('3','7'): '<<^^',
    ('3','8'): '^^<',
    ('3','9'): '^^',

    ('4','0'): '>vv',
    ('4','1'): 'v',
    ('4','2'): '>v',
    ('4','3'): '>>v',
    ('4','A'): '>>vv',
    ('4','5'): '>',
    ('4','6'): '>>',
    ('4','7'): '^',
    ('4','8'): '^>',
    ('4','9'): '^>>',

    ('5','0'): 'vv',
    ('5','1'): 'v<',
    ('5','2'): 'v',
    ('5','3'): '>v',
    ('5','4'): '<',
    ('5','A'): '>vv',
    ('5','6'): '>',
    ('5','7'): '^<',
    ('5','8'): '^',
    ('5','9'): '^>',

    ('6','0'): 'vv<',
    ('6','1'): 'v<<',
    ('6','2'): 'v<',
    ('6','3'): 'v',
    ('6','4'): '<<',
    ('6','5'): '<',
    ('6','A'): 'vv',
    ('6','7'): '^<<',
    ('6','8'): '^<',
    ('6','9'): '^',

    ('7','0'): '>vvv',
    ('7','1'): 'vv',
    ('7','2'): '>vv',
    ('7','3'): '>>vv',
    ('7','4'): 'v',
    ('7','5'): '>v',
    ('7','6'): '>>v',
    ('7','A'): '>>vvv',
    ('7','8'): '>',
    ('7','9'): '>>',

    ('8','0'): 'vvv',
    ('8','1'): 'vv<',
    ('8','2'): 'vv',
    ('8','3'): '>vv',
    ('8','4'): 'v<',
    ('8','5'): 'v',
    ('8','6'): 'v>',
    ('8','7'): '<',
    ('8','A'): '>vvv',
    ('8','9'): '>',

    ('9','0'): 'vvv<',
    ('9','1'): 'vv<<',
    ('9','2'): 'vv<',
    ('9','3'): 'vv',
    ('9','4'): 'v<<',
    ('9','5'): 'v<',
    ('9','6'): 'v',
    ('9','7'): '<<',
    ('9','8'): '<',
    ('9','A'): 'vvv',
}
def code2instructions(code, m):
    instructions = ''
    current = 'A'
    for digit in code:
        instruction = m.get((current, digit), '')
        logging.debug(f"Moving from {current} to {digit}: [{instruction}]")
        instructions += instruction
        instructions += 'A'
        current = digit
    return instructions

#
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
pad_map = {
    ('A','>'): 'v',
    ('A','^'): '<',
    ('A','v'): 'v<',
    ('A','<'): 'v<<',

    ('>','A'): '^',
    ('>','^'): '^<',
    ('>','v'): '<',
    ('>','<'): '<<',

    ('^','>'): '>v',
    ('^','A'): '>',
    ('^','v'): 'v',
    ('^','<'): 'v<',

    ('v','>'): '>',
    ('v','^'): '^',
    ('v','A'): '>^',
    ('v','<'): '<',

    ('<','>'): '>>',
    ('<','^'): '>^',
    ('<','v'): '>',
    ('<','A'): '>>^',
}

def complexity(seq, code):
    return len(seq) * int(code[0:-1])

total_complexity = 0
for line in lines:
    # radiation bot, telling depressurized bot what to do:
    pad = code2instructions(line, code_map)

    # freezer bot, telling radiation bot what to do:
    pad2 = code2instructions(pad, pad_map)

    # You, telling freezer bot what to do:
    pad3 = code2instructions(pad2, pad_map)
    comp = complexity(pad3, line)
    total_complexity += comp
    logging.debug(f"{line} -> {pad} -> {pad2} -> {pad3} ({len(pad3)} x {int(line[0:-1])}). Complexity: {comp}")

logging.info(f"Total complexity: {total_complexity}")

# <v<A >>^A vA ^A <vA <A A >>^A A vA <^A >A A vA ^A <vA >^A A <A >A <v<A >A >^A A A vA <^A >A
#    <    A  >  A   v  < <    A A  >   ^  A A  >  A   v   A A  ^  A    <  v   A A A  >   ^  A
#         ^     A             < <         ^ ^     A       > >     A           v v v         A
#               3                                 7               9                         A

# v<<A >>^A vA ^A v<<A >>^A A v<A <A >>^A A vA A ^<A >A v<A >^A A <A >A v<A <A >>^A A A vA ^<A >A
#    <    A  >  A    <    A A   v  <    A A  > >   ^  A   v   A A  ^  A   v  <    A A A  >   ^  A
#         ^     A         ^ ^           < <           A       > >     A           v v v         A
#               3                                     7               9                         A

if not TEST:
    p.answer_a = total_complexity
