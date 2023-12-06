from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2023, day=5)

TEST = False
if TEST:
    lines = p.examples[0].input_data.splitlines()
else:
    lines = p.input_data.splitlines()

_, seeds_line = lines[0].split(': ')
seeds = [int(n) for n in seeds_line.split()]

logging.debug("Found seeds: {}".format(seeds))

current_map_key = None
maps = {}

for line in lines[2:]:
    if 'map:' in line:
        current_map_key = line
    elif line == '':
        continue
    else:
        if current_map_key not in maps:
            maps[current_map_key] = {}

        dest_range, src_range, length = [int(r) for r in line.split()]
        maps[current_map_key][src_range] = (dest_range, length)

for k, v in maps.items():
    logging.debug("Found a key of {}, its sub-map had {} items".format(k, len(v)))

def apply_map(seed, the_map):
    for src, (dest, length) in the_map.items():
        if src <= seed and src + length >= seed:
            offset = seed - src
            return dest + offset
    return seed

def apply_map_range(seed_start, seed_end, the_map):
    remaining_to_check = [(seed_start, seed_end)]
    outputs = []
    while len(remaining_to_check) > 0:
        a, b = remaining_to_check.pop()
        logging.debug("Checking range {}..{}".format(a, b))
        found_an_overlap = False
        for src, (dest, length) in the_map.items():
            logging.debug("checking map entry src={}, dest={}, length={}".format(src, dest, length))
            src_start = src
            src_end = src + length - 1

            overlap_start = max(src_start, a)
            overlap_end = min(src_end, b)

            if overlap_end >= overlap_start:
                logging.debug("Found an overlap {}..{} remaps from {}..{} to {}..{}".format(overlap_start, overlap_end, src_start, src_end, dest, dest + length - 1))
                found_an_overlap = True
                if overlap_start > a:
                    logging.debug("Adding a remainder {}..{}".format(a, overlap_start - 1))
                    remaining_to_check.append((a, overlap_start - 1))
                if overlap_end < b:
                    logging.debug("Adding a remainder {}..{}".format(overlap_end + 1, b))
                    remaining_to_check.append((overlap_end + 1, b))

                offset_start = overlap_start - src_start
                offset_length = overlap_end - overlap_start
                outputs.append((dest + offset_start, dest + offset_start + offset_length))
        if not found_an_overlap:
            outputs.append((a, b))
    logging.debug("{}..{} -> {}".format(seed_start, seed_end, outputs))
    return outputs

def seed_to_location(seed):
    soil = apply_map(seed, maps["seed-to-soil map:"])
    fertilizer = apply_map(soil, maps["soil-to-fertilizer map:"])
    water = apply_map(fertilizer, maps["fertilizer-to-water map:"])
    light = apply_map(water, maps["water-to-light map:"])
    temp = apply_map(light, maps["light-to-temperature map:"])
    humidity = apply_map(temp, maps["temperature-to-humidity map:"])
    location = apply_map(humidity, maps["humidity-to-location map:"])
    return location

def seed_to_location2(seed_start, seed_end):
    # output_ranges = []
    output_ranges = apply_map_range(seed_start, seed_end, maps["seed-to-soil map:"])
    next_ranges = []
    for rs, re in output_ranges:
        next_ranges += apply_map_range(rs, re, maps["soil-to-fertilizer map:"])
    output_ranges = next_ranges

    next_ranges = []
    for rs, re in output_ranges:
        next_ranges += apply_map_range(rs, re, maps["fertilizer-to-water map:"])
    output_ranges = next_ranges

    next_ranges = []
    for rs, re in output_ranges:
        next_ranges += apply_map_range(rs, re, maps["water-to-light map:"])
    output_ranges = next_ranges

    next_ranges = []
    for rs, re in output_ranges:
        next_ranges += apply_map_range(rs, re, maps["light-to-temperature map:"])
    output_ranges = next_ranges

    next_ranges = []
    for rs, re in output_ranges:
        next_ranges += apply_map_range(rs, re, maps["temperature-to-humidity map:"])
    output_ranges = next_ranges

    next_ranges = []
    for rs, re in output_ranges:
        next_ranges += apply_map_range(rs, re, maps["humidity-to-location map:"])
    output_ranges = next_ranges

    return output_ranges

locations = [seed_to_location(a) for a in seeds]

lowest = sorted(locations)[0]
# logging.info("Lowest: {}".format(lowest))
if not TEST:
    p.answer_a = lowest

# Part 2
ranges = []
for i in range(0, len(seeds), 2):
    range_start = seeds[i]
    range_end = range_start + seeds[i+1] - 1
    ranges.append((range_start, range_end))

lowest_location = None
for ss, se in ranges:
    location_ranges = seed_to_location2(ss, se)
    for ls, le in location_ranges:
        if lowest_location is None or ls < lowest_location:
            logging.info("Found a new low location: {}".format(ls))
            lowest_location = ls

logging.info("lowest location: {}".format(lowest_location))
if not TEST:
    p.answer_b = lowest_start
    