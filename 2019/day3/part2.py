# --- Part Two ---
#
# It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal delay.
#
# To do this, calculate the number of steps each wire takes to reach each intersection; choose the intersection where the sum of both wires' steps is lowest. If a wire visits a position on the grid multiple times, use the steps value from the first time it visits that position when calculating the total value of a specific intersection.
#
# The number of steps a wire takes is the total number of grid squares the wire has entered to get to that location, including the intersection being considered. Again consider the example from above:
#
# ...........
# .+-----+...
# .|.....|...
# .|..+--X-+.
# .|..|..|.|.
# .|.-X--+.|.
# .|..|....|.
# .|.......|.
# .o-------+.
# ...........
#
# In the above example, the intersection closest to the central port is reached after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second wire for a total of 20+20 = 40 steps.
#
# However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.
#
# Here are the best steps for the extra examples from above:
#
#     R75,D30,R83,U83,L12,D49,R71,U7,L72
#     U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
#     R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
#     U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps
#
# What is the fewest combined steps the wires must take to reach an intersection?

from collections import defaultdict

class loc:
	def __init__(self):
		self.s1 = None
		self.s2 = None

	def cross(self):
		return self.s1 is not None and self.s2 is not None

	def steps(self):
		return self.s1 + self.s2

	def add1(self, steps):
		if self.s1 is None:
			self.s1 = steps

	def add2(self, steps):
		if self.s2 is None:
			self.s2 = steps

def apply(grid, wire, label):
	x = 0
	y = 0
	steps = 0

	for d in wire:
		#print("Location: ({}, {})".format(x, y))
		direction = d[0]
		distance = int(d[1:])
		#print("Moving {} to the {} from ({},{})".format(distance, direction, x, y))

		for i in range(distance):
			if direction == 'R':
				cx = x+i
				cy = y
				dx = distance
				dy = 0
			elif direction == 'L':
				cx = x-i
				cy = y
				dx = -distance
				dy = 0
			elif direction == 'U':
				cx = x
				cy = y+i
				dx = 0
				dy = distance
			elif direction == 'D':
				cx = x
				cy = y-i
				dx = 0
				dy = -distance

			if label == 1:
				grid[(cx, cy)].add1(steps)
			else:
				grid[(cx, cy)].add2(steps)
			steps += 1
		x += dx
		y += dy

def closest_intersection(w1, w2):
	# make a grid
	grid = defaultdict(loc)
	# lay out wire 1
	apply(grid, w1, 1)
	# lay out wire 2
	apply(grid, w2, 2)
	# identify closest intersection
	min_x = -1
	min_y = -1
	min_loc = None
	for (x, y), v in grid.items():
		if x == 0 and y == 0:
			continue
		if v.cross():
			steps = v.steps()
			print("found a cross at ({}, {}), steps = {}".format(x, y, steps))
			if min_loc is None or min_loc.steps() > steps:
				min_x = x
				min_y = y
				min_loc = v
	return (min_x, min_y, min_loc)

with open('input') as fin:
	wire1 = fin.readline().strip().split(',')
	wire2 = fin.readline().strip().split(',')

#print("closest: {}".format(closest_intersection(wire1, wire2)))

# = 10
#rid = [[0] * n for i in range(n)]
#pply(grid, ['R8','U5','L5','D3'], 1, 'x')
#pply(grid, ['U7','R6','D4','L4'], 2, 'x')
#rint_grid(grid)

#min_x = n
#min_y = n
#for x in range(n):
#	for y in range(n):
#		if x == 0 and y == 0:
#			continue
#		if grid[x][y] == 'x':
#			#print("found a cross at ({}, {})".format(x, y))
#			if (min_x + min_y) > (x + y):
#				min_x = x
#				min_y = y
#print("found minimal cross at ({}, {})".format(min_x, min_y))

x, y, l = closest_intersection(
	['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
	['U62','R66','U55','R34','D71','R55','D58','R83'])
print("Closest: ({}, {}) ({}=610?)".format(x, y, l.steps()))

x, y, l = closest_intersection(
	['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
	['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7'])
print("Closest: ({}, {}) ({}=410?)".format(x, y, l.steps()))


x, y, l = closest_intersection(wire1, wire2)

print("Closest: ({}, {}) = {}".format(x, y, l.steps()))

