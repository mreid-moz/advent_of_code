from aocd.models import Puzzle
from collections import defaultdict
from utils import draw_map
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2024, day=14)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
    max_x = 11
    max_y = 7
else:
    lines = p.input_data.splitlines()
    max_x = 101
    max_y = 103


class Robot:
    def __init__(self, px, py, vx, vy):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy

    def get_position(self, num_seconds):
        nx = (self.px + num_seconds * self.vx) % max_x
        ny = (self.py + num_seconds * self.vy) % max_y
        return nx, ny

robots = []
for line in lines:
    pos, v = line.split(" ")
    px, py = [int(s) for s in pos[2:].split(',')]
    vx, vy = [int(s) for s in v[2:].split(',')]
    robots.append(Robot(px, py, vx, vy))

def get_quadrant(x, y):
    mx = max_x // 2
    my = max_y // 2
    if x == mx or y == my:
        return None
    if x < mx and y < my:
        return 0
    elif x > mx and y < my:
        return 1
    elif x < mx:
        return 2
    return 3

quadrants = [0, 0, 0, 0]
num_seconds = 100
for robot in robots:
    nx, ny = robot.get_position(num_seconds)
    q = get_quadrant(nx, ny)
    # logging.debug(f"After {num_seconds}, robot at {robot.px},{robot.py} moved to {nx},{ny} (in quadrant {q})")
    if q is not None:
        quadrants[q] += 1

safety_factor = quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]
logging.info(f"Safety factor: {safety_factor}")
if not TEST:
    p.answer_a = safety_factor

x_mid = max_x // 2
high_score = 0
for i in range(100000):
    m = {}
    for r in robots:
        nx, ny = r.get_position(i)
        m[(nx, ny)] = 'X'
    drawn = draw_map(m, max_x, max_y, print_now=False)
    lets_see = False
    for draw_line in drawn:
        if "XXXXXXXXXX" in draw_line:
            lets_see = True
    if lets_see:
        logging.info(f"======={i}=======")
        for draw_line in drawn:
            logging.debug(draw_line)
