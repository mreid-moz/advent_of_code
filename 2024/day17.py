from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2024, day=17)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
    lines = [
        "Register A: 2024",
        "Register B: 0",
        "Register C: 0",
        "",
        "Program: 0,3,5,4,3,0",
    ]
else:
    lines = p.input_data.splitlines()

#...

class Computer:
    def __init__(self, a, b, c, program):
        self.a = a
        self.b = b
        self.c = c
        self.out = []
        self.program = program
        self.num_instructions = len(program)
        self.instruction = 0

    def run(self, max_steps=None):
        current_step = 0
        while self.instruction < self.num_instructions - 1:
            current_step += 1
            if max_steps is not None and current_step > max_steps:
                break
            self.step()

    def operand(self, o, combo=True):
        if not combo:
            return o

        if o <= 3:
            return o
        elif o == 4:
            return self.a
        elif o == 5:
            return self.b
        elif o == 6:
            return self.c
        else:
            logging.error(f"Unexpected operand {o}")
            return None

    def step(self):
        if self.instruction >= self.num_instructions:
            return None

        opcode = self.program[self.instruction]
        operand = self.program[self.instruction + 1]
        # logging.debug(f"ptr {self.instruction} -> code={opcode} operand={operand}")
        advance_pointer = True
        if opcode == 0: # adv
            # logging.debug(f"0 adv: a = {self.a} / 2^{self.operand(operand)}")
            self.a //= 2 ** self.operand(operand)
        elif opcode == 1: # bxl
            # logging.debug(f"1 bxl: b = {self.b} XOR {self.operand(operand, combo=False)}")
            self.b = self.b ^ self.operand(operand, combo=False)
        elif opcode == 2: # bst
            # logging.debug(f"2 bst: b = {self.operand(operand)} % 8")
            self.b = self.operand(operand) % 8
        elif opcode == 3: # jnz
            if self.a == 0:
                logging.debug(f"3 jnz: a was zero, no-op")
            else:
                # logging.debug(f"3 jnz: jump to {self.operand(operand, combo=False)}")
                self.instruction = self.operand(operand, combo=False)
                advance_pointer = False
        elif opcode == 4: # bxc
            # logging.debug(f"4 bxc: b = {self.b} XOR {self.c}")
            self.b = self.b ^ self.c
        elif opcode == 5: # out
            # logging.debug(f"5 out: outputting {self.operand(operand)} % 8")
            self.out.append(self.operand(operand) % 8)
        elif opcode == 6: # bdv
            # logging.debug(f"6 bdv: b = {self.a} / 2^{self.operand(operand)}")
            self.b = self.a // (2 ** self.operand(operand))
        elif opcode == 7: # cdv
            # logging.debug(f"7 cdv: c = {self.a} / 2^{self.operand(operand)}")
            self.c = self.a // (2 ** self.operand(operand))
        else:
            logging.error(f"{opcode} ???: unexpected opcode")

        # logging.debug(f"Advancing instruction pointer from {self.instruction} to {self.instruction + 2}")
        if advance_pointer:
            self.instruction += 2


_, sa = lines[0].split(": ")
a = int(sa)
_, sb = lines[0].split(": ")
b = int(sb)
_, sc = lines[0].split(": ")
c = int(sc)

program = [int(s) for s in lines[-1][8:].split(',')]

logging.info(f"Running program {program}")

comp = Computer(a, b, c, program)
comp.run()

result = ','.join([str(i) for i in comp.out])
logging.info(result)

if not TEST:
    p.answer_a = result

# Iterat 50000000010000 produced [3, 0, 1, 2, 5, 1, 7, 6, 7, 1, 1, 1, 1, 1, 0, 2]
# Iterat 40000000005000 produced [7, 5, 4, 6, 0, 3, 5, 4, 1, 5, 5, 2, 5, 1, 2, 2]
# Iterat 36000042401792 produced [3, 3, 3, 6, 5, 7, 7, 3, 4, 3, 1, 6, 0, 6, 3, 2]
# goal:                          [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 3, 5, 5, 3, 0]
# Iterat 36000000216841 produced [2, 4, 1, 5, 7, 1, 4, 1, 5, 1, 1, 6, 0, 6, 3, 2]
# Iterat 35000000781000 produced [5, 7, 1, 3, 7, 3, 5, 5, 3, 4, 5, 6, 3, 3, 5]
# Iterat 35000000781000 produced [5, 7, 1, 3, 7, 3, 5, 5, 3, 4, 5, 6, 3, 3, 5]
# Iterat 35000000005000 produced [7, 5, 4, 0, 5, 3, 5, 5, 3, 4, 5, 6, 3, 3, 5]
# Iterat 30000000006000 produced [0, 0, 3, 7, 3, 7, 3, 7, 3, 3, 4, 5, 5, 3, 5]
# Iterat 20000000006000 produced [0, 0, 3, 2, 3, 2, 1, 5, 1, 0, 0, 3, 4, 5, 5]
# Iteration 1239000     produced [5, 3, 3, 5, 0, 3, 5]
# Iteration 50035000    produced [2, 5, 5, 1, 1, 3, 2, 1, 1]
# Iteration 500029000   produced [1, 6, 7, 3, 3, 6, 5, 0, 3, 0]
# Iteration 50000007000 produced [1, 7, 3, 5, 6, 1, 4, 0, 5, 5, 0, 3]
current_a = 36000002930441
while True:
    comp = Computer(current_a, b, c, program)
    comp.run(max_steps=1000)
    # if current_a % 64 == 0:
    if comp.out[0:6] == [2, 4, 1, 5, 7, 5]:
        logging.info(f"Iteration {current_a} produced {comp.out}")
    if comp.out == program:
        logging.info(f"If a={current_a}, program produces itself")
        if not TEST:
            p.answer_b = current_a
        break
    current_a += 130048# 64 * 4 * 8 * 8
