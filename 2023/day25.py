from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.INFO)

p = Puzzle(year=2023, day=25)

BIG_NUMBER = 10000000000

TEST = False
if TEST:
    # lines = p.examples[0].input_data.splitlines()
    lines = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr""".splitlines()
else:
    lines = p.input_data.splitlines()

connections = defaultdict(set)

for line in lines:
    # logging.debug(line)
    lhs, rhs = line.split(': ')
    rhs_comps = rhs.split(' ')
    for r in rhs_comps:
        connections[lhs].add(r)
        connections[r].add(lhs)

logging.info("Found {} components with {} connections".format(len(connections), sum([len(v) for v in connections.values()]) // 2))

def dijkstra(conns, src, skips=set([])):
    dist = {}
    prev = {}
    unvisited = set()
    for dest in conns.keys():
        # logging.debug("{} <--> {}".format(src, dest))
        dist[dest] = BIG_NUMBER
        unvisited.add(dest)
    dist[src] = 0

    while unvisited:
        closest = None
        min_dist = None
        for u in unvisited:
            if min_dist is None or dist[u] < min_dist:
                min_dist = dist[u]
                closest = u
        unvisited.remove(closest)

        # logging.debug("Looking at {} (dist {})".format(closest, min_dist))

        for next_node in conns.get(closest):
            if next_node not in unvisited:
                # this also rules out invalid points and the point itself (since we removed it above)
                # logging.debug("skipping {} wasn't in unvisited.".format(next_node))
                continue

            if (next_node, closest) in skips or (closest, next_node) in skips:
                logging.debug("Skipping: {},{}".format(closest, next_node))
                continue

            next_dist = min_dist + 1
            if next_dist < dist[next_node]:
                # logging.debug("Setting distance {} to {}".format(next_node, next_dist))
                dist[next_node] = next_dist
                prev[next_node] = closest
            else:
                # logging.debug("Already had a better distance for {} ({} < current {})".format(next_node, dist[next_node], next_dist))
                pass
        logging.debug("{} remaining".format(len(unvisited)))
    return dist, prev

shortest_max = 2
if not TEST:
    shortest_max = 8

candidate_nodes = set()
if TEST:
    for node in connections.keys():
        dist, paths = dijkstra(connections, node)
        # find the shortest longest shortest path (lol)
        # - dijkstra finds the the shortest path to each node
        # - the longest of the shortest paths gives the furthest away node
        # - minimizing these should give us "central" nodes to try chopping,
        #   thus narrowing down the set of edges to try.
        longest_path = max(dist.values())
        if longest_path <= shortest_max:
            logging.info("Found a shorty: {}".format(node))
            candidate_nodes.add(node)
        # logging.info("Longest shortest path from {} was {}".format(node, longest_path))
else:
    # already ran it. use results from before since it took a couple mins.
    candidate_nodes = set(['tnr', 'krx', 'lfk', 'vzb', 'tvf', 'lmg', 'tqn'])

candidate_edges = set()
for n in candidate_nodes:
    for dest in connections[n]:
        if (dest, n) in  candidate_edges:
            continue
        candidate_edges.add((n, dest))

logging.info("Found a max of {} to try".format(len(candidate_edges)))

candidate_edges = list(candidate_edges)
for ce in candidate_edges:
    logging.debug("Candidate edge: {}".format(ce))

for i, e1 in enumerate(candidate_edges[:-2]):
    for j in range(i+1, len(candidate_edges) - 1, 1):
        e2 = candidate_edges[j]
        for k in range(j + 1, len(candidate_edges), 1):
            e3 = candidate_edges[k]
            logging.info("Attempting without edges {}={}, {}={}, {}={}".format(i, e1, j, e2, k, e3))
            # This should create a disjoint graph, so something should be unreachable from (any?) one
            # of the nodes that had a connection removed. If not, try each of the skip-nodes in turn.
            dist, paths = dijkstra(connections, e1[0], skips={e1, e2, e3})
            bigs = sum([1 for v in dist.values() if v == BIG_NUMBER])
            longest_path = max(dist.values())
            if bigs > 0:
                product = bigs * (len(connections) - bigs)
                logging.info("Found {} big numbers when removing edges {}, {}, {}. Product was {}".format(bigs, e1, e2, e3, product))
                if not TEST:
                    p.answer_a = product
                sys.exit(1)
