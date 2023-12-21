from aocd.models import Puzzle
from collections import defaultdict
from itertools import repeat
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=20)

TEST = True
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

num_iterations = 4
for i in range(num_iterations):
    current_pulses = [('button', 'broadcaster', 0)]
    current_source = 'button'
    dest = 'broadcaster'
    counter[0] += 1
    pulses = list(module_map[dest].send_pulse(0, current_source))
    current_source = dest

    while True:
        next_pulses = []
        for node, pulse in pulses:
            counter[pulse] += 1
            # logging.debug("Sending pulse {} from {} to {}".format(pulse, current_source, node))
            if node in module_map:
                current_pulses = module_map[node].send_pulse(pulse, current_source)
                for cn, cp in current_pulses:
                    logging.debug("xx {} -{}-> {}".format(node, cp, cn))
                    next_pulses.append((cn, cp))
            else:
                logging.debug("Sending pulse to dead end {}".format(node))
            # next_pulses += current_pulses
        pulses = next_pulses
        logging.debug("Setting current node from {} to {}".format(current_source, node))
        current_source = node
        if len(pulses) == 0:
            logging.debug("No pulses.")
            break

    logging.info("Sent {} low pulses and {} high pulses => {}".format(counter[0], counter[1], counter[0] * counter[1]))

if not TEST:
    p.answer_a = counter[0] * counter[1]
