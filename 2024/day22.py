from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2024, day=22)

TEST = False
if TEST:
    # lines = p.examples[0].input_data.splitlines()
    lines = [
        # "123",
        "1",
        "2",
        "3",
        # "10",
        # "100",
        "2024",
    ]
else:
    lines = p.input_data.splitlines()

def mix(a, b):
    return a ^ b

def prune(a):
    return a % 16777216 # 0o100000000

def evolve(secret):
    n = prune(mix(secret, secret * 64))
    n = prune(mix(n, n // 32))
    n = prune(mix(n, n * 2048))
    return n

def get_price(seq, history, deltas):
    n_delta = len(deltas)
    last = n_delta - len(seq)
    for i, d in enumerate(deltas):
        if i == 0:
            continue
        if i > last:
            break
        if d != seq[0]:
            continue
        if seq[1] == deltas[i+1] and seq[2] == deltas[i+2] and seq[3] == deltas[i+3]:
            # logging.debug(f"Found {seq} at {i}")
            return history[i+3]
    # logging.debug(f"Never found {seq}")
    return None


nums = [int(s) for s in lines]
histories = [[n % 10] for n in nums]
deltas = [[None] for _ in nums]
# logging.debug(f"histories: {histories}, deltas: {deltas}")
iterations = 2000
for i in range(iterations):
    for j in range(len(nums)):
        nums[j] = evolve(nums[j])
        histories[j].append(nums[j] % 10)
        if i > 0:
            deltas[j].append(histories[j][i] - histories[j][i-1])

total = sum(nums)
logging.info(f"After {iterations} evolutions, total was {total}")
if not TEST:
    p.answer_a = total

# s = [-2,1,-1,3]
# total_price = 0
# for i, num in enumerate(lines):
#     price = get_price(s, histories[i], deltas[i])
#     logging.info(f"Price for {num} was {price}")
#     if price is not None:
#         total_price += price

# logging.info(f"total price for {s}: {total_price}")

all_sequences = defaultdict(set)
for i in range(len(deltas)):
    for j in range(1, len(deltas[i]) - 3):
        all_sequences[(deltas[i][j], deltas[i][j+1], deltas[i][j+2], deltas[i][j+3])].add(i)

logging.info(f"Found {len(all_sequences)} distinct sequences")

# sort them by the number of different histories they show up in (more is better)
searchables = list(all_sequences.items())
searchables.sort(key=lambda a: len(a[1]), reverse=True)

max_bananas = 0
seq_counter = 0
for searchable in searchables[0:500]:
    # logging.debug(f"Checking {searchable[0]}")
    seq_counter += 1
    if seq_counter % 50 == 0:
        logging.debug(f"We've checked {seq_counter} sequences.")
    bananas = 0
    for i in range(len(lines)):
        one_bananas = get_price(searchable[0], histories[i], deltas[i])
        if one_bananas is not None:
            bananas += one_bananas
    if bananas > max_bananas:
        logging.info(f"So far best sequence {searchable[0]} got us {bananas} bananas.")
        max_bananas = bananas

logging.info(f"Max possible bananas: {max_bananas}")
if not TEST:
    p.answer_b = max_bananas

