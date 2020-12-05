import itertools
import logging

logging.basicConfig(level=logging.INFO)

class Moon:
  def __init__(self, x, y, z, vx=0, vy=0, vz=0, name="Moon"):
    self.name = name
    self.x = x
    self.y = y
    self.z = z
    self.vx = vx
    self.vy = vy
    self.vz = vz

  def __str__(self):
    return "{}: pos = ({},{},{}), vel = ({},{},{})".format(
      self.name, self.x, self.y, self.z, self.vx, self.vy, self.vz)

  def potential(self):
    return abs(self.x) + abs(self.y) + abs(self.z)

  def kinetic(self):
    return abs(self.vx) + abs(self.vy) + abs(self.vz)

  def total_energy(self):
    return self.potential() * self.kinetic()

class System:
  def __init__(self, moons):
    self.moons = moons

  def apply_gravity(self):
    for a, b in itertools.combinations(self.moons, 2):
      logging.debug("Applying gravity between {} and {}".format(a, b))
      if a.x > b.x:
        logging.debug(" x: {} > {}, -1 for {}, +1 for {}".format(a.x, b.x, a.name, b.name))
        a.vx -= 1
        b.vx += 1
      elif a.x < b.x:
        logging.debug(" x: {} < {}, -1 for {}, +1 for {}".format(a.x, b.x, b.name, a.name))
        a.vx += 1
        b.vx -= 1

      if a.y > b.y:
        logging.debug(" y: {} > {}, -1 for {}, +1 for {}".format(a.y, b.y, a.name, b.name))
        a.vy -= 1
        b.vy += 1
      elif a.y < b.y:
        logging.debug(" y: {} < {}, -1 for {}, +1 for {}".format(a.y, b.y, b.name, a.name))
        a.vy += 1
        b.vy -= 1

      if a.z > b.z:
        logging.debug(" z: {} > {}, -1 for {}, +1 for {}".format(a.z, b.z, a.name, b.name))
        a.vz -= 1
        b.vz += 1
      elif a.z < b.z:
        logging.debug(" z: {} < {}, -1 for {}, +1 for {}".format(a.z, b.z, a.name, b.name))
        a.vz += 1
        b.vz -= 1

  def update_velocity(self):
    for m in self.moons:
      m.x += m.vx
      m.y += m.vy
      m.z += m.vz

  def step(self):
    self.apply_gravity()
    self.update_velocity()

  def show(self):
    for m in self.moons:
      print(m)

  def __str__(self):
    return "\n".join([str(m) for m in self.moons])

def test_one(m, x, y, z, vx, vy, vz):
  exp = Moon(x, y, z, vx, vy, vz, name=m.name)
  if str(exp) != str(m):
    logging.info("Actual '{}' != Expected '{}'".format(m, exp))
  assert(str(m) == str(exp))

def test():
  m1 = Moon(-1, 0, 2, name="m1")
  m2 = Moon(2, -10, -7, name="m2")
  m3 = Moon(4, -8, 8, name="m3")
  m4 = Moon(3, 5, -1, name="m4")

  s = System([m1, m2, m3, m4])
  test_one(m1, -1,  0,  2,  0,  0,  0)
  s.step()
  logging.debug("After one step:")
  s.show()
  test_one(m1,  2, -1,  1,  3, -1, -1)
  test_one(m2,  3, -7, -4,  1,  3,  3)
  test_one(m3,  1, -7,  5, -3,  1, -3)
  test_one(m4,  2,  2,  0, -1, -3,  1)
  s.step()
  logging.debug("After two steps:")
  s.show()
  test_one(m1,  5, -3, -1,  3, -2, -2)
  test_one(m2,  1, -2,  2, -2,  5,  6)
  test_one(m3,  1, -4, -1,  0,  3, -6)
  test_one(m4,  1, -4,  2, -1, -6,  2)
  s.step()
  logging.debug("After three steps:")
  s.show()
  test_one(m1,  5, -6, -1,  0, -3,  0)
  test_one(m2,  0,  0,  6, -1,  2,  4)
  test_one(m3,  2,  1, -5,  1,  5, -4)
  test_one(m4,  1, -8,  2,  0, -4,  0)
  s.step()
  logging.debug("After four steps:")
  s.show()
  test_one(m1,  2, -8,  0, -3, -2,  1)
  test_one(m2,  2,  1,  7,  2,  1,  1)
  test_one(m3,  2,  3, -6,  0,  2, -1)
  test_one(m4,  2, -9,  1,  1, -1, -1)

#test()

m1 = Moon(3, 15, 8, name="m1")
m2 = Moon(5, -1, -2, name="m2")
m3 = Moon(-10, 8, 2, name="m3")
m4 = Moon(8, 4, -5, name="m4")

s = System([m1, m2, m3, m4])
for i in range(1000):
  s.step()

print("Total energy: {}".format(sum([ m.total_energy() for m in s.moons ])))

def test2():
  m1 = Moon(-1,  0,  2)
  m2 = Moon( 2,-10, -7)
  m3 = Moon( 4, -8,  8)
  m4 = Moon( 3,  5, -1)
  s = System([m1, m2, m3, m4])
  states = set()
  states.add(str(s))

  counter = 0
  while True:
    s.step()
    counter += 1
    new_state = str(s)
    if new_state in states:
      print("Found a repeated state after {} steps".format(counter))
      break
    if counter % 1000 == 0:
      logging.info("We've now seen {} states".format(counter))

#test2()

m1 = Moon(3, 15, 8, name="m1")
m2 = Moon(5, -1, -2, name="m2")
m3 = Moon(-10, 8, 2, name="m3")
m4 = Moon(8, 4, -5, name="m4")

def find_repeat(moons):
  s = System(moons)
  states = set()
  states.add(str(s))
  counter = 0
  while True:
    s.step()
    counter += 1
    new_state = str(s)
    if new_state in states:
      return counter
    if counter % 5000 == 0:
      logging.info("We've now seen {} states".format(counter))

def gcd(a,b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / gcd(a, b)

# Find X:
m1 = Moon(3, 0, 0, name="x1")
m2 = Moon(5, 0, 0, name="x2")
m3 = Moon(-10, 0, 0, name="x3")
m4 = Moon(8, 0, 0, name="x4")

x_period = find_repeat([m1, m2, m3, m4])

# Find Y:
m1 = Moon(0, 15, 0, name="y1")
m2 = Moon(0, -1, 0, name="y2")
m3 = Moon(0, 8, 0, name="y3")
m4 = Moon(0, 4, 0, name="y4")
y_period = find_repeat([m1, m2, m3, m4])

# Find Z:
m1 = Moon(0, 0, 8, name="z1")
m2 = Moon(0, 0, -2, name="z2")
m3 = Moon(0, 0, 2, name="z3")
m4 = Moon(0, 0, -5, name="z4")
z_period = find_repeat([m1, m2, m3, m4])

print("X period: {}, Y Period: {}, Z period: {}. Overall: {}".format(x_period, y_period, z_period, lcm(lcm(x_period, y_period), z_period)))

