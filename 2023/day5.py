from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

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
        # for i in range(length):
        #     current_map[src_range + i] = dest_range + i
# maps[current_map_key] = current_map

for k, v in maps.items():
    logging.debug("Found a key of {}, its sub-map had {} items".format(k, len(v)))

def apply_map(seed, the_map):
    for src, (dest, length) in the_map.items():
        if src <= seed and src + length >= seed:
            offset = seed - src
            return dest + offset
    return seed

def reverse_map(location_start, location_end, humidity_to_location_map):
    a = location_start
    b = location_end

    # a ....... b
    #    c ........... d
    #    ^      ^

    #         a ....... b
    #    c ................. d
    #         ^         ^

    #                a ....... b
    #    c .............. d
    #                ^    ^

    #   a ....... b
    #                c .............. d
    #         X         

    min_start = None
    min_end = None
    for src, (dest, length) in humidity_to_location_map.items():
        dest_start = dest
        dest_end = dest + length - 1

        overlap_start = max(a, dest_start)
        overlap_end = min(b, dest_end)

        if overlap_end >= overlap_start:
            offset_start = overlap_start - dest
            offset_end = overlap_end - dest
            logging.debug("Found an overlap between {}..{} and {}..{}: {}..{}. Maps to start {}..{}".format(
                a, b, dest_start, dest_end, overlap_start, overlap_end, src + offset_start, src + offset_end))

            ### don't stop short, look for the lowest overlapping range ###
            if min_start is None or min_start > src + offset_start:
                min_start = src + offset_start
                min_end = src + offset_end
            return (src + offset_start, src + offset_end)
    if min_start is not None:
        return (min_start, min_end)
    return (location_start, location_end)


soils = [apply_map(a, maps["seed-to-soil map:"]) for a in seeds]
fertilizers = [apply_map(a, maps["soil-to-fertilizer map:"]) for a in soils]
waters = [apply_map(a, maps["fertilizer-to-water map:"]) for a in fertilizers]
lights = [apply_map(a, maps["water-to-light map:"]) for a in waters]
temps = [apply_map(a, maps["light-to-temperature map:"]) for a in lights]
humidities = [apply_map(a, maps["temperature-to-humidity map:"]) for a in temps]
locations = [apply_map(a, maps["humidity-to-location map:"]) for a in humidities]

lowest = sorted(locations)[0]
logging.info("Lowest: {}".format(lowest))
if not TEST:
    p.answer_a = lowest

# Part 2: work backwards from the lowest location.
lowest_location_start = None
lowest_location_end = None
for src, (dest, length) in maps["humidity-to-location map:"].items():
    if lowest_location_start is None or dest < lowest_location_start:
        lowest_location_start = dest
        lowest_location_end = dest + length - 1

logging.debug("lowest location range possible is {} to {}".format(lowest_location_start, lowest_location_end))

humidity_start, humidity_end = reverse_map(lowest_location_start, lowest_location_end, maps["humidity-to-location map:"])
logging.debug("lowest humidity range possible is {} to {}".format(humidity_start, humidity_end))

temp_start, temp_end = reverse_map(humidity_start, humidity_end, maps["temperature-to-humidity map:"])
logging.debug("lowest temp range possible is {} to {}".format(temp_start, temp_end))

light_start, light_end = reverse_map(temp_start, temp_end, maps["light-to-temperature map:"])
logging.debug("lowest light range possible is {} to {}".format(light_start, light_end))

water_start, water_end = reverse_map(light_start, light_end, maps["water-to-light map:"])
logging.debug("lowest water range possible is {} to {}".format(water_start, water_end))

fertilizer_start, fertilizer_end = reverse_map(water_start, water_end, maps["fertilizer-to-water map:"])
logging.debug("lowest fertilizer range possible is {} to {}".format(fertilizer_start, fertilizer_end))

soil_start, soil_end = reverse_map(fertilizer_start, fertilizer_end, maps["soil-to-fertilizer map:"])
logging.debug("lowest soil range possible is {} to {}".format(soil_start, soil_end))

seed_start, seed_end = reverse_map(soil_start, soil_end, maps["seed-to-soil map:"])
logging.debug("lowest seed range possible is {} to {}".format(seed_start, seed_end))

if not TEST:
    p.answer_b = seed_start

soils = [apply_map(a, maps["seed-to-soil map:"]) for a in [2499418212, 2837953084]]
fertilizers = [apply_map(a, maps["soil-to-fertilizer map:"]) for a in soils]
waters = [apply_map(a, maps["fertilizer-to-water map:"]) for a in fertilizers]
lights = [apply_map(a, maps["water-to-light map:"]) for a in waters]
temps = [apply_map(a, maps["light-to-temperature map:"]) for a in lights]
humidities = [apply_map(a, maps["temperature-to-humidity map:"]) for a in temps]
locations = [apply_map(a, maps["humidity-to-location map:"]) for a in humidities]

logging.info("those two translate to {}".format(locations))