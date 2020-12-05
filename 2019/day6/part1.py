# --- Day 6: Universal Orbit Map ---
#
# You've landed at the Universal Orbit Map facility on Mercury. Because navigation in space often involves transferring between orbits, the orbit maps here are useful for finding efficient routes between, for example, you and Santa. You download a map of the local orbits (your puzzle input).
#
# Except for the universal Center of Mass (COM), every object in space is in orbit around exactly one other object. An orbit looks roughly like this:
#
#                   \
#                    \
#                     |
#                     |
# AAA--> o            o <--BBB
#                     |
#                     |
#                    /
#                   /
#
# In this diagram, the object BBB is in orbit around AAA. The path that BBB takes around AAA (drawn with lines) is only partly shown. In the map data, this orbital relationship is written AAA)BBB, which means "BBB is in orbit around AAA".
#
# Before you use your map data to plot a course, you need to make sure it wasn't corrupted during the download. To verify maps, the Universal Orbit Map facility uses orbit count checksums - the total number of direct orbits (like the one shown above) and indirect orbits.
#
# Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can be any number of objects long: if A orbits B, B orbits C, and C orbits D, then A indirectly orbits D.
#
# For example, suppose you have the following map:
#
# COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
#
# Visually, the above map of orbits looks like this:
#
#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I
#
#         2 - 3       5 - 6 - 7
#        /           /
# COM - 1 - 2 - 3 - 4 - 5
#                \
#                 4
#
# In this visual representation, when two objects are connected by a line, the one on the right directly orbits the one on the left.
#
# Here, we can count the total number of orbits as follows:
#
#     D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
#     L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7 orbits.
#     COM orbits nothing.
#
# The total number of direct and indirect orbits in this example is 42.
#
# What is the total number of direct and indirect orbits in your map data?

class Map:
  def __init__(self, map_data):
    self.map = {}
    for d in map_data:
      self.add_orbit(d)

  def find(self, label):
    return self.map.get(label)

  def add(self, an_orbit):
    self.map[an_orbit.label] = an_orbit

  def find_or_add(self, label):
    orbit = self.find(label)
    if orbit is None:
      orbit = Orbit(label)
      self.add(orbit)
    return orbit

  def add_orbit(self, desc):
    parent, child = desc.split(")")
    p_orbit = self.find_or_add(parent)
    c_orbit = self.find_or_add(child)
    c_orbit.set_parent(p_orbit)
    p_orbit.add_child(c_orbit)

  def show(self):
    for name, orbit in self.map.items():
      print("{}, distance {}".format(name, orbit.distance))

  def get_distance(self):
    total = 0
    for orbit in self.map.values():
      total += orbit.distance
    return total

class Orbit:
  def __init__(self, label):
    self.parent = None
    self.label = label
    self.distance = 0
    self.children = []

  def set_parent(self, an_orbit):
    self.parent = an_orbit
    self.distance = self.parent.distance + 1
    # Also update child distances.
    for child in self.children:
      child.set_parent(self)

  def add_child(self, an_orbit):
    self.children.append(an_orbit)

def direct_orbits(arr):
  pass

def test():
  #orbit_map = Map([])
  #orbit_map.show()
  #orbit_map.add(Orbit("A"))
  #print("After adding A, find(A) = {}".format(orbit_map.map.get("A")))
  #print("{}".format(orbit_map.map.get('A')))

  orbit_descriptions = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']
  orbit_map = Map(orbit_descriptions)
  orbit_map.show()
  print("Total distance: {}".format(orbit_map.get_distance()))

#test()

with open("input") as fin:
  lines = [l.strip() for l in fin.readlines()]

print("first: {}, last: {}.".format(lines[0], lines[-1]))
orbit_map = Map(lines)
#orbit_map.show()
print("Total distance: {}".format(orbit_map.get_distance()))
