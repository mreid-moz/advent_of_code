from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2024, day=13)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

class ClawMachine:
    def __init__(self, ax, ay, bx, by, px, py):
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.px = px
        self.py = py

    def __str__(self):
        return f"""Button A: X+{self.ax}, Y+{self.ay}
Button B: X+{self.bx}, Y+{self.by}
Prize: X={self.px}, Y={self.py}"""

    def cost(self, ai, bi):
        return ai * 3 + bi

    def win_cost(self):
        # max_a = min(self.px // self.ax, self.py // self.ay) + 1
        # max_b = min(self.px // self.bx, self.py // self.by) + 1
        max_a = 100
        max_b = 100
        # logging.debug(f"For p={self.px},{self.py}, we can have a max of {max_a} A's and {max_b} B's")
        min_cost = None
        for ai in range(max_a):
            ax = ai * self.ax
            ay = ai * self.ay
            if ax > self.px or ay > self.py:
                break
            for bi in range(max_b):
                bx = bi * self.bx
                tx = ax + bx
                by = bi * self.by
                ty = ay + by
                # logging.debug(f"Testing {ai} A's and {bi} B's (x={ax}+{bx}={tx}, y={ay}+{by}={ty}, p={self.px},{self.py}")
                if tx == self.px and ty == self.py:
                    cost = self.cost(ai, bi)
                    logging.info(f"Found a winning combo: {ai}xA and {bi}xB for cost {cost}")
                    if min_cost is None or cost < min_cost:
                        min_cost = cost
        return min_cost

# a1x + b1y = c1
# a2x + b2y = c2
def solve_linear_ints(a1, b1, c1, a2, b2, c2):
    # a1x + b1y = c1
    # -> y = (c1 - a1x) / b1
    # a2x + b2y = c2
    # -> y = (c2 - a2x) / b2
    # -> (c1 - a1x) / b1 = (c2 - a2x) / b2
    # -> b2*c1 - b2*a1x = b1*c2 - b1*a2x
    # -> b1*a2x - b2*a1x = b1*c2 - b2*c1
    # -> (b1*a2 - b2*a1)x = b1*c2 - b2*c1
    # -> x = (b1*c2 - b2*c1) / (b1*a2 - b2*a1)

    logging.debug(f"1: {a1}x + {b1}y = {c1}")
    logging.debug(f"2: {a2}x + {b2}y = {c2}")

    if b1 == 0 or b2 == 0:
        logging.debug(f"No solution: (zero b)")
        return None

    numer = (b1 * c2 - b2 * c1)
    denom = (b1 * a2 - b2 * a1)

    if numer % denom != 0:
        logging.debug(f"No int solution: (b1*c2 - b2*c1) not divisible by (b1 - b2) * (a2 - a1). {numer}%{denom}={numer%denom}")
        return None

    x = numer // denom
    y = c1 - a1 * x
    if y % b1 != 0:
        logging.debug(f"No int solution: (c1 - a1x) not divisible by b1. {y}%{b1}={y%b1}")
        return None
    y = y // b1
    return x, y


class BigMachine(ClawMachine):
    def __init__(self, ax, ay, bx, by, px, py):
        super().__init__(ax, ay, bx, by, px, py)
        self.px += 10000000000000
        self.py += 10000000000000

    def check_whole(self, num_a, num_b):
        ai = int(num_a)
        bi = int(num_b)
        return self.ax * ai + self.bx * bi == self.px and self.ay * ai + self.by * bi == self.py

    def win_cost(self):
        sol = solve_linear_ints(self.ax, self.bx, self.px, self.ay, self.by, self.py)
        if sol is None:
            return None

        num_a, num_b = sol
        logging.debug(f"solution: {num_a} As, {num_b} Bs")
        return self.cost(num_a, num_b)

def get_button_xy(xy):
    xs, ys, = xy.split(", ")
    x = int(xs[2:])
    y = int(ys[2:])

    return (x, y)

#  7x+2y= 17
# −4x+1y=−14
x, y = solve_linear_ints(7, 2, 17, -4, 1, -14)
logging.info(f"7x+2y=17, -4x+y=-14 => x={x}, y={y}")


machines =  []
big_machines = []
ax, ay, bx, by, px, py = [None]*6
for line in lines:
    if line == '':
        continue
    thing, xy = line.split(": ")
    if thing == "Button A":
        ax, ay =  get_button_xy(xy)
    elif thing == "Button B":
        bx, by = get_button_xy(xy)
    elif thing == "Prize":
        px, py = get_button_xy(xy)
        machines.append(ClawMachine(ax, ay, bx, by, px, py))
        big_machines.append(BigMachine(ax, ay, bx, by, px, py))
    else:
        logging.debug(f"unexpected line: {line}")

logging.debug(f"Found {len(machines)} machines")
total_tokens = 0
for m in machines:
    cost = m.win_cost()
    logging.info(f"Cost was {cost}")
    if cost is not None:
        total_tokens += cost

logging.info(f"Total tokens to win all prizes: {total_tokens}")
if not TEST:
    p.answer_a = total_tokens

total_tokens = 0
for m in big_machines:
    cost = m.win_cost()
    logging.info(f"Cost was {cost}")
    if cost is not None:
        total_tokens += cost

logging.info(f"Total tokens to win big prizes: {total_tokens}")
if not TEST:
    p.answer_b = total_tokens

