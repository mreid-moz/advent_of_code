from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2024, day=11)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
    for i in range(len(lines)):
        logging.debug(f"line {i}: {lines[i]}")
    lines = lines[1:]
else:
    lines = p.input_data.splitlines()

# Slow part 1 way
def blink(stones):
    for i in range(len(stones)):
        if stones[i] == 0:
            stones[i] = 1
        elif len(str(stones[i])) % 2 == 0:
            s = str(stones[i])
            left = int(s[0:len(s)//2])
            right = int(s[len(s)//2:])
            stones[i] = left
            # TODO: insert it instead of appending it?
            stones.append(right)
        else:
            stones[i] *= 2024

def blink_map(stones):
    blinked = {}
    for stone, count in stones.items():
        if stone == 0:
            blinked[1] = blinked.get(1, 0) + count
        elif len(str(stone)) % 2 == 0:
            s = str(stone)
            left = int(s[0:len(s)//2])
            right = int(s[len(s)//2:])
            blinked[left] = blinked.get(left, 0) + count
            blinked[right] = blinked.get(right, 0) + count
        else:
            if stone * 2024 not in blinked:
                blinked[stone * 2024] = 0

            blinked[stone * 2024] += count
    return blinked

def count_stones(stone_map):
    return sum(stone_map.values())

def print_stones(stone_map):
    items = [f"{k}x{v}" for k, v in stone_map.items()]
    return ", ".join(items)

def compare(stone_map, stones):
    compare_map = {}
    for stone in stones:
        compare_map[stone] = compare_map.get(stone, 0) + 1

    for k, v in stone_map.items():
        if k not in compare_map:
            logging.debug(f"<<< {k} was missing (should be {v} of them)")
        elif compare_map[k] != v:
            logging.debug(f"<<< {k} = {compare_map[k]}, should be {v}")

    for k, v in compare_map.items():
        if k not in stone_map:
            logging.debug(f">>> {k} was missing (should be {v} of them)")

stones = [int(s) for s in lines[0].split()]
stone_map = {}
for stone in stones:
    stone_map[stone] = 1

num_blinks = 75
for i in range(num_blinks):
    stone_map = blink_map(stone_map)
    logging.info(f"After {i + 1} blinks, there were {count_stones(stone_map)} stones")
    # blink(stones)
    # logging.info(f"After {i + 1} blinks, there were {count_stones(stone_map)} stones: {print_stones(stone_map)}")
    # logging.info("Comparing...")
    # compare(stone_map, stones)
    # if len(stones) != count_stones(stone_map):
    #     logging.info(f"Mismatch, should be {len(stones)}: {sorted(stones)}")
    if i == 24:
        if not TEST:
            p.answer_a = count_stones(stone_map)

logging.info(f"After {num_blinks} blinks, there were {count_stones(stone_map)} stones")

if not TEST:
    p.answer_b = count_stones(stone_map)
