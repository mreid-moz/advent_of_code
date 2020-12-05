
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

orbit_map = Map(lines)
#orbit_map.show()
#print("Total distance: {}".format(orbit_map.get_distance()))

you = orbit_map.find('YOU')
santa = orbit_map.find('SAN')

def get_tree(orbit):
  tree = []
  while orbit.parent is not None:
    tree.append(orbit.parent)
    orbit = orbit.parent
  return tree

you_labels = [o.label for o in get_tree(you)]
santa_labels = [o.label for o in get_tree(santa)]
print("YOU {}".format("<-".join(you_labels)))
print("SAN {}".format("<-".join(santa_labels)))

common_tree = []
while you_labels[-1] == santa_labels[-1]:
  common_tree.append(you_labels.pop())
  santa_labels.pop()

print("Common: {}".format("<-".join(common_tree)))

print("YOU {}".format("<-".join(you_labels)))
print("SAN {}".format("<-".join(santa_labels)))

print("Number of required jumps: {} + {} = {}".format(len(you_labels), len(santa_labels), len(you_labels) + len(santa_labels)))