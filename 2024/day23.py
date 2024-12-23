from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

puzz = Puzzle(year=2024, day=23)

TEST = False
if TEST:
    lines = puzz.examples[0].input_data.splitlines()
else:
    lines = puzz.input_data.splitlines()

connections = defaultdict(set)
for line in lines:
    a, b = line.split('-')
    connections[a].add(b)
    connections[b].add(a)

triples = set()
for comp, neighbours in connections.items():
    for neighbour in neighbours:
        other_comps = connections[neighbour]
        common = neighbours & other_comps
        if common:
            if comp.startswith('t'):
                for third in common:
                    triples.add(','.join(sorted([comp, neighbour, third])))
                # logging.info(f"{comp} and {neighbour} had {len(neighbours & other_comps)} in common: {}")

logging.info(f"Found {len(triples)} triples")

if not TEST:
    puzz.answer_a = len(triples)

# https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
def bron_kerbosch(r, p, x, collector):
    if not p and not x:
        collector.append(list(r))
        return

    skips = set()
    for v in p:
        bron_kerbosch(r.union(set([v])), (p - skips) & connections[v], x & connections[v], collector)
        skips.add(v)
        x.add(v)

cliques = []
bron_kerbosch(set(), set(connections.keys()), set(), cliques)
largest = None
for clique in cliques:
    # logging.info(f"Checking: {clique}")
    if largest is None or len(clique) > len(largest):
        largest = clique

key = ','.join(sorted(largest))
logging.info(f"Largest clique: {len(largest)} -> {key}")

if not TEST:
    puzz.answer_b = key
