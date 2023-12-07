from aocd.models import Puzzle
from collections import defaultdict
import functools
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2023, day=7)

card_values = {
    'A': 14, 'K': 13, 'Q': 12, 
    'J': 11, 'T': 10, '9': 9, 
    '8': 8, '7': 7, '6': 6, 
    '5': 5, '4': 4, '3': 3, '2': 2
}

wild_card_values = {
    'A': 14, 'K': 13, 'Q': 12, 
    'J': 0, 'T': 10, '9': 9, 
    '8': 8, '7': 7, '6': 6, 
    '5': 5, '4': 4, '3': 3, '2': 2
}

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

# it's sorted
def longest_repeat(hand):
    longest_seq = -1
    current_seq = 1
    for i in range(len(hand) - 1):
        if hand[i] == hand[i+1]:
            current_seq += 1
            # logging.debug("{}: Found a match at {}, current seq is {}".format(hand, i, current_seq))
        else:
            if current_seq > longest_seq:
                longest_seq = current_seq
            current_seq = 1
    if current_seq > longest_seq:
        longest_seq = current_seq

    return longest_seq

def hand_type(hand):
    distinct_cards = len(set(hand))
    logging.debug("{} had {} distinct cards".format(hand, distinct_cards))
    if distinct_cards == 1:
        return 7 # 5 of a kind

    if distinct_cards == 5:
        return 1 # high card

    if distinct_cards == 4:
        return 2 # one pair

    s = sorted(hand)
    if distinct_cards == 2:
        if s[0] != s[1] or s[-1] != s[-2]:
            # 4 of a kind
            return 6
        if s[1] != s[2] or s[-2] != s[-3]:
            # full house
            return 5

    # distinct cards is 3.
    l = longest_repeat(s)
    if l == 3:
        return 4 # three of a kind
    elif l == 2:
        return 3 # two pair
    else:
        logging.info("Longest repeat was {}".format(l))
    logging.warning("unknown hand type for {}".format(hand))
    return 100


def type_to_name(hand_type):
    return [
        'High Card',
        'One Pair',
        'Two Pair',
        'Three of a Kind',
        'Full House',
        'Four of a Kind',
        'Five of a Kind'
    ][hand_type - 1]


def compare(hand1, hand2):
    h1 = hand1[0]
    h2 = hand2[0]

    h1t = hand_type(h1)
    h2t = hand_type(h2)
    logging.debug("{} -> {}, {} -> {}".format(h1, type_to_name(h1t), h2, type_to_name(h2t)))
    if h1t < h2t:
        logging.debug("{} wins".format(h2))
        return -1
    elif h1t > h2t:
        logging.debug("{} wins".format(h1))
        return 1

    logging.debug("{} and {} are of the same type {}".format(h1, h2, type_to_name(h1t)))
    for i, card in enumerate(h1):
        c = card_values[card]
        if c < card_values[h2[i]]:
            logging.debug("{} wins".format(h2))
            return -1
        if c > card_values[h2[i]]:
            logging.debug("{} wins".format(h1))
            return 1
    return 0

def remove_wildcards(hand):
    dummies = ['V','W','X','Y','Z']
    stripped = [0,0,0,0,0]
    num_wildcards = 0
    for i, c in enumerate(hand):
        if c == 'J':
            stripped[i] = dummies[num_wildcards]
            num_wildcards += 1
        else:
            stripped[i] = c
    return stripped, num_wildcards

def upgrade_hand(hand_type, num_wildcards):
    if num_wildcards == 0:
        return hand_type

    if num_wildcards == 1:
        if hand_type == 1:
            return 2 # high card -> one pair
        if hand_type == 2:
            return 4 # one pair -> three of a kind
        if hand_type == 3:
            return 5 # two pair -> full house
        if hand_type == 4:
            return 6 # three -> four of a kind
        if hand_type == 5:
            return 6 # full house -> four of a kind (maybe not possible)
        if hand_type == 6:
            return 7 # four -> five of a kind
        if hand_type == 7:
            return 7

    if num_wildcards == 2:
        if hand_type == 1:
            return 4 # high card -> three of a kind
        if hand_type == 2:
            return 6 # one pair -> four of a kind
        if hand_type == 3:
            return 6 # two pair -> four of a kind
        if hand_type == 4:
            return 7 # three -> five of a kind
        return 7

    if num_wildcards == 3:
        if hand_type == 1:
            return 6 # high card -> four of a kind
        if hand_type == 2:
            return 7 # one pair -> five of a kind
        return 7

    if num_wildcards >= 4:
        return 7

def compare2(hand1, hand2):
    h1 = hand1[0]
    h2 = hand2[0]
    h1_no_wild, h1_wild_count = remove_wildcards(h1)
    h2_no_wild, h2_wild_count = remove_wildcards(h2)
    h1t = hand_type(h1_no_wild)
    h2t = hand_type(h2_no_wild)
    h1ut = upgrade_hand(h1t, h1_wild_count)
    h2ut = upgrade_hand(h2t, h2_wild_count)
    logging.debug("{} -> {} -> {}, {} -> {} -> {}".format(h1, type_to_name(h1t), h1ut, h2, type_to_name(h2t), h2ut))
    if h1ut < h2ut:
        logging.debug("{} wins".format(h2))
        return -1
    elif h1ut > h2ut:
        logging.debug("{} wins".format(h1))
        return 1

    logging.debug("{} and {} are of the same type {}".format(h1, h2, type_to_name(h1ut)))
    for i, card in enumerate(h1):
        c = wild_card_values[card]
        if c < wild_card_values[h2[i]]:
            logging.debug("{} wins".format(h2))
            return -1
        if c > wild_card_values[h2[i]]:
            logging.debug("{} wins".format(h1))
            return 1
    return 0

hands = []
for line in lines:
    hand, bid = line.strip().split()
    bid = int(bid)
    hands.append((hand, bid))

if not p.answered_a:
    sorted_hands = sorted(hands, key=functools.cmp_to_key(compare))

    winnings = 0
    for i, (hand, bid) in enumerate(sorted_hands):
        winnings += (i+1) * bid
        logging.info("{} ({}) with bid {} x {} = {}".format(hand, type_to_name(hand_type(hand)), bid, (i+1), bid * (i+1)))

    logging.info("Total winnings: {}".format(winnings))

    if not TEST:
        p.answer_a = winnings

sorted_hands = sorted(hands, key=functools.cmp_to_key(compare2))

winnings = 0
for i, (hand, bid) in enumerate(sorted_hands):
    winnings += (i+1) * bid
    logging.info("{} ({}) with bid {} x {} = {}".format(hand, type_to_name(hand_type(hand)), bid, (i+1), bid * (i+1)))

logging.info("Total winnings: {}".format(winnings))

if not TEST:
    p.answer_b = winnings