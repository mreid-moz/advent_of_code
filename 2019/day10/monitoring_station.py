import logging
import math
logging.basicConfig(level=logging.INFO)

class Asteroid:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.visible_count = 0
    self.angle = None
    self.distance_from_base = None

  def __str__(self):
    return "({},{})".format(self.x, self.y)

  def get_angle(self):
    return self.angle

  def set_distance(self, base):
    self.distance_from_base = math.sqrt((self.x - base.x) ** 2 + (self.y - base.y) ** 2)

  def get_distance(self):
    return self.distance_from_base

def get_asteroids(map):
  asteroids = {}
  rows = map.strip().split("\n")
  n_rows = len(rows)
  n_cols = len(rows[0])
  for r in range(n_rows):
    for c in range(n_cols):
      x = c
      y = r
      if rows[r][c] == '#':
        logging.debug("Found an asteroid at ({},{})".format(x, y))
        asteroids[(x, y)] = Asteroid(x, y)
  return asteroids

def is_between(a, b, c):
    crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)

    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) != 0:
      return False

    dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y) * (b.y - a.y)
    if dotproduct < 0:
      return False

    squaredlengthba = (b.x - a.x) * (b.x - a.x) + (b.y - a.y) * (b.y - a.y)
    if dotproduct > squaredlengthba:
      return False

    return True

def is_visible(source, dest, asteroids):
  for a in asteroids.values():
    if a == source or a == dest:
      continue
    if is_between(source, dest, a):
      return False
  return True

def find_best_location(map):
  asteroids = get_asteroids(map)

  logging.debug("Found {} asteroids".format(len(asteroids)))

  max_visible = 0
  max_asteroid = None

  for (x, y), src in asteroids.items():
    # Set the visibility levels.
    logging.info("Checking source {}".format(src))
    num_visible = 0
    for dest in asteroids.values():
      if dest != src:
        if is_visible(src, dest, asteroids):
          num_visible += 1
          logging.info("{} is the {}th visible asteroid from {}.".format(dest, num_visible, src))
        else:
          logging.info("{} is not visible from {}.".format(dest, src))
    src.visible_count = num_visible
    if num_visible > max_visible:
      max_visible = num_visible
      max_asteroid = src
  return max_asteroid

class test_case:
  def __init__(self, map, best_count, best_loc):
    self.map = map.strip()
    self.best_count = best_count
    self.best_loc = best_loc

test_cases = [
  test_case("""
.#..#
.....
#####
....#
...##
""", 8, (3,4)),
  test_case("""
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
""", 33, (5,8)),
  test_case("""
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
""", 35, (1,2)),
  test_case("""
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
""", 41, (6,3)),
  test_case("""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""", 210, (11,13))
]

def test():
  assert(is_between(Asteroid(1,1), Asteroid(3,3), Asteroid(2,2)))
  assert(is_between(Asteroid(4,4), Asteroid(4,0), Asteroid(4,2)))
  assert(is_between(Asteroid(0,0), Asteroid(4,0), Asteroid(2,0)))
  assert(not is_between(Asteroid(0,0), Asteroid(4,4), Asteroid(2,3)))

  for tc in test_cases:
    logging.info("Testing:\n{}".format(tc.map))
    best = find_best_location(tc.map)
    print("Found best: {} ({}). Expected: {}".format(best, best.visible_count, tc.best_count))
    assert(best.visible_count == tc.best_count)

#test()

with open("input") as fin:
  real_map = fin.read()

#best = find_best_location(real_map)
#print("Found best: {} = {}".format(best, best.visible_count))
print("Found best: (23,19) = 278")

## Part 2: find the angle between every one, and see when they get vapourized.

def rad2deg(rads):
  return rads * 180 / math.pi

def get_angle(source, dest):
  if source.x == dest.x and dest.y < source.y:
    return 0

  extra_angle = 0
  opp = abs(dest.x - source.x)
  adj = abs(dest.y - source.y)

  if source.x < dest.x:
    # east half
    if source.y > dest.y:
      # northeast quadrant
      logging.debug("northeast")
      extra_angle = 0
    elif source.y < dest.y:
      logging.debug("southeast")
      # southeast quadrant
      opp = abs(dest.y - source.y)
      adj = abs(dest.x - source.x)
      extra_angle = 90
    else:
      return 90
  elif source.x > dest.x:
    # west half
    if source.y < dest.y:
      # southwest quadrant
      logging.debug("southwest")
      extra_angle = 180
    elif source.y > dest.y:
      logging.debug("northwest")
      opp = abs(dest.y - source.y)
      adj = abs(dest.x - source.x)
      extra_angle = 270
    else:
      return 270
  else:
    # midpoint
    if source.y < dest.y:
      return 180
    elif source.y > dest.y:
      return 0
    else:
      return None #overlapping

  #opp = abs(dest.x - source.x)
  #adj = abs(dest.y - source.y)
  return rad2deg(math.atan(opp / adj)) + extra_angle

def test_angle(x1, y1, x2, y2, expected):
  angle = get_angle(Asteroid(x1, y1), Asteroid(x2, y2))
  logging.debug("Angle from ({},{}) to ({},{}) is {} (expected {})".format(
    x1, y1, x2, y2, angle, expected))

  if expected is None:
    return angle is None
  else:
    return angle == expected

def get_two_hundredth(a_map, base, two_hundred):
  asteroids = get_asteroids(a_map)

  base = asteroids[base]

  not_base = [ a for a in asteroids.values() if a != base ]
  for a in not_base:
    theta = get_angle(base, a)
    logging.debug("Angle between {} and {} is {}".format(base, a, theta))
    a.angle = theta
    a.set_distance(base)

  ordered_by_angle = sorted(not_base, key=Asteroid.get_angle)

  ordered_and_stacked = []

  for i in range(len(ordered_by_angle)):
    asteroid = ordered_by_angle[i]
    current_angle = asteroid.get_angle()
    if len(ordered_and_stacked) == 0:
      ordered_and_stacked.append([asteroid])
    else:
      lasteroid = ordered_and_stacked[-1][0]
      if lasteroid.angle == asteroid.angle:
        ordered_and_stacked[-1].append(asteroid)
      else:
        ordered_and_stacked.append([asteroid])

  for i in range(len(ordered_and_stacked)):
    if len(ordered_and_stacked[i]) > 1:
      ordered_and_stacked[i] = sorted(ordered_and_stacked[i], key=Asteroid.get_distance)

  counter = 0
  two_hundredth = None
  while True:
    for i in ordered_and_stacked:
      if len(i) == 0:
        continue
      a = i.pop(0)
      counter += 1
      logging.info("Blast #{} @ {}, angle {}, distance {}, there are {} more behind here".format(counter, a, a.angle, a.get_distance(), len(i)))
      if counter == two_hundred:
        return a

def test2():
  assert(test_angle(0,0,  5,5,  135))
  assert(test_angle(0,0,  0,5,  180))
  assert(test_angle(0,0,  5,0,  90))
  assert(test_angle(0,0,  0,0,  None))
  assert(test_angle(5,5,  6,4,  45))
  assert(test_angle(5,5,  6,6,  135))
  assert(test_angle(5,5,  4,6,  225))
  assert(test_angle(5,5,  4,4,  315))
  assert(test_angle(5,5,  0,0,  315))
  assert(test_angle(11,13, 8,2,  344.74488129694225))

  r = get_two_hundredth(test_cases[-1].map, (11,13), 1)
  assert(r.x == 11 and r.y == 12)
  r = get_two_hundredth(test_cases[-1].map, (11,13), 20)
  assert(r.x == 16 and r.y == 0)
  r = get_two_hundredth(test_cases[-1].map, (11,13), 50)
  assert(r.x == 16 and r.y == 9)
  r = get_two_hundredth(test_cases[-1].map, (11,13), 100)
  assert(r.x == 10 and r.y == 16)
  r = get_two_hundredth(test_cases[-1].map, (11,13), 299)
  assert(r.x == 11 and r.y == 1)
  r = get_two_hundredth(test_cases[-1].map, (11,13), 199)
  assert(r.x == 9 and r.y == 6)
  r = get_two_hundredth(test_cases[-1].map, (11,13), 200)
  assert(r.x == 8 and r.y == 2)
  r = get_two_hundredth(test_cases[-1].map, (11,13), 201)
  assert(r.x == 10 and r.y == 9)
  print("Test2 tests all pass.")

#test2()

two_hundredth = get_two_hundredth(real_map, (23,19), 200)
print("200th asteroid was {} => {}".format(two_hundredth, two_hundredth.x * 100 + two_hundredth.y))
