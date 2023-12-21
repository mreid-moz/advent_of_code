from aocd.models import Puzzle
from collections import defaultdict
from itertools import repeat
from utils import lcm
import logging
import re
import sys

logging.basicConfig(level=logging.WARNING)

p = Puzzle(year=2023, day=20)

TEST = False
if TEST:
    # lines = p.examples[0].input_data.splitlines()
    lines = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""".splitlines()
else:
    lines = p.input_data.splitlines()

class Module:
    def __init__(self, line):
        name, downstream = line.split (' -> ')
        if name == 'broadcaster':
            self.t = 'b'
            self.name = name
        else:
            self.t = name[0]
            self.name = name[1:]
        self.destinations = downstream.split(', ')
        if self.t == '&':
            self.last_pulse = defaultdict(int)
        if self.t == '%':
            self.state = 'off'
        self.inputs = []

    def add_input(self, upstream):
        self.inputs.append(upstream)

    def flipflop(self, pulse):
        if pulse == 1:
            return []
        else:
            if self.state == 'off':
                logging.debug("Flipflop '{}' was {}, sending 1".format(self.name, self.state))
                self.state = 'on'
                return zip(self.destinations, repeat(1))
            else:
                logging.debug("Flipflop '{}' was {}, sending 0".format(self.name, self.state))
                self.state = 'off'
                return zip(self.destinations, repeat(0))

    def conjunction(self, pulse, from_input):
        logging.debug("Conjunction {}: setting last input from {} to {}".format(self.name, from_input, pulse))
        self.last_pulse[from_input] = pulse
        for node in self.inputs:
            last_val = self.last_pulse[node]
            logging.debug("Conjunction {}: last input from {} was {}".format(self.name, node, last_val))
            if last_val == 0:
                logging.debug("Conjunction {} inputs were not all high, sending 1".format(self.name))
                return zip(self.destinations, repeat(1))
        logging.debug("Conjunction {} inputs were all high, sending 0".format(self.name))
        return zip(self.destinations, repeat(0))

    def broadcast(self, pulse):
        return zip(self.destinations, repeat(pulse))

    def send_pulse(self, pulse, from_input):
        logging.info(" {} -{}-> {}".format(from_input, pulse, self.name))
        if self.t == '%':
            return self.flipflop(pulse)
        elif self.t == '&':
            return self.conjunction(pulse, from_input)
        elif self.t == 'b':
            return self.broadcast(pulse)
        else:
            logging.error("Unhandled module type {}".format(self.t))

module_map = {}
modules = []
for line in lines:
    m = Module(line)
    logging.debug("Found a module {}".format(m.name))
    module_map[m.name] = m
    modules.append(m)

for m in modules:
    for d in m.destinations:
        if d in module_map:
            module_map[d].add_input(m.name)

counter = defaultdict(int)
num_iterations = 1000
for i in range(num_iterations):
    current_pulses = [('button', 'broadcaster', 0)]

    while True:
        more_pulses = []
        logging.debug("Processing {} pulses".format(len(current_pulses)))
        for src, dest, pulse in current_pulses:
            # logging.debug("TODO1: {} -{}-> {}".format(src, pulse, dest))
            counter[pulse] += 1
            if dest in module_map:
                next_pulses = module_map[dest].send_pulse(pulse, src)
                for next_dest, next_pulse in next_pulses:
                    # logging.debug("TODO2: {} -{}-> {}".format(dest, next_pulse, next_dest))
                    more_pulses.append((dest, next_dest, next_pulse))
            else:
                logging.info(" {} -{}-> {} (dead end)".format(src, pulse, dest))
        logging.debug("Queueing up {} more pulses".format(len(more_pulses)))
        current_pulses = more_pulses
        if len(current_pulses) == 0:
            logging.debug("No pulses.")
            break

    logging.info("Sent {} low pulses and {} high pulses => {}".format(counter[0], counter[1], counter[0] * counter[1]))

if not TEST:
    p.answer_a = counter[0] * counter[1]

# Part 2
# counter = defaultdict(int)
# interesting_modules = set(['sg','lm','dh','db'])
# last_seen = defaultdict(int)
# # Note: 76_765_638_939_687 is too low o_O
# num_iterations = 50_000_000
# for i in range(num_iterations):
#     if i % 1000 == 1:
#         logging.warning("Ran {} iterations so far".format(i+1))
#     current_pulses = [('button', 'broadcaster', 0)]

#     while True:
#         more_pulses = []
#         logging.debug("Processing {} pulses".format(len(current_pulses)))
#         for src, dest, pulse in current_pulses:
#             if pulse == 1 and src in interesting_modules:
#                 logging.warning("{} received a 1 on iteration {}, last seen on {}, diff={}".format(src, i+1, last_seen[src], i+1-last_seen[src]))
#                 last_seen[src] = i+1
#             # logging.debug("TODO1: {} -{}-> {}".format(src, pulse, dest))
#             counter[pulse] += 1
#             if dest in module_map:
#                 next_pulses = module_map[dest].send_pulse(pulse, src)
#                 for next_dest, next_pulse in next_pulses:
#                     # logging.debug("TODO2: {} -{}-> {}".format(dest, next_pulse, next_dest))
#                     more_pulses.append((dest, next_dest, next_pulse))
#             else:
#                 logging.info(" {} -{}-> {} (dead end)".format(src, pulse, dest))
#                 if dest == 'rx' and pulse == 0:
#                     logging.warning("Found a low pulse to rx on iteration {}".format(i+1))
#                     if not TEST:
#                         p.answer_b = i + 1
#                     sys.exit(-1)
#         logging.debug("Queueing up {} more pulses".format(len(more_pulses)))
#         current_pulses = more_pulses
#         if len(current_pulses) == 0:
#             logging.debug("No pulses.")
#             break

#     logging.info("Sent {} low pulses and {} high pulses => {}".format(counter[0], counter[1], counter[0] * counter[1]))

ones = [2851, 2889, 3027, 3079]
deltas = [3851, 3889, 4027, 4079]
# 246006621492687

ones[0] = ((246006621492687 - ones[0]) // deltas[0]) * deltas[0]
ones[1] = ((246006621492687 - ones[1]) // deltas[1]) * deltas[1]
ones[2] = ((246006621492687 - ones[2]) // deltas[2]) * deltas[2]
ones[3] = ((246006621492687 - ones[3]) // deltas[3]) * deltas[3]

# This is gonna take forever...
# WARNING:root:ran 544000000 iterations to get to [538459115243, 538459116440, 538459116994, 538459113612]

so_many = 0
while ones[0] != ones[1] or ones[0] != ones[2] or ones[0] != ones[3]:
    so_many += 1
    if so_many % 200000 == 0:
        logging.warning("ran {} iterations to get to {}".format(so_many, ones))
    smallest = ones[0]
    smallest_idx = 0
    for i in [1, 2, 3]:
        if ones[i] < smallest:
            smallest = ones[i]
            smallest_idx = i
    ones[smallest_idx] += deltas[smallest_idx]

logging.warning("Everyone happily matched after {}".format(ones[0]))
if not TEST:
    p.answer_b = ones[0]

# Initial deltas:
# lm received a 1 on iteration 2851, last seen on 0, diff=2851
# dh received a 1 on iteration 2889, last seen on 0, diff=2889
# sg received a 1 on iteration 3027, last seen on 0, diff=3027
# db received a 1 on iteration 3079, last seen on 0, diff=3079

# Stable deltas:
# lm received a 1 on iteration 6702, last seen on 2851, diff=3851
# dh received a 1 on iteration 6778, last seen on 2889, diff=3889
# sg received a 1 on iteration 7054, last seen on 3027, diff=4027
# db received a 1 on iteration 7158, last seen on 3079, diff=4079

# Is it (3851 * 3889 * 4027 * 4079) - 1000 ?  Nope, too low.
# Is it (3851 * 3889 * 4027 * 4079) + (2851 * 2889 * 3027 * 3079) ? Nope, too high
