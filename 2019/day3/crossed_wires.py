# --- Day 3: Crossed Wires ---
#
# The gravity assist was successful, and you're well on your way to the Venus refuelling station. During the rush back on Earth, the fuel management system wasn't completely installed, so that's next on the priority list.
#
# Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port and extend outward on a grid. You trace the path each wire takes as it leaves the central port, one wire per line of text (your puzzle input).
#
# The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to find the intersection point closest to the central port. Because the wires are on a grid, use the Manhattan distance for this measurement. While the wires do technically cross right at the central port where they both start, this point does not count, nor does a wire count as crossing with itself.
#
# For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), it goes right 8, up 5, left 5, and finally down 3:
#
# ...........
# ...........
# ...........
# ....+----+.
# ....|....|.
# ....|....|.
# ....|....|.
# .........|.
# .o-------+.
# ...........
#
# Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:
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
# These wires cross at two locations (marked X), but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.
#
# Here are a few more examples:
#
#     R75,D30,R83,U83,L12,D49,R71,U7,L72
#     U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
#     R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
#     U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135

def print_grid(grid):
	for row in grid:
		print("{}".format(row))


def apply(grid, wire, label, cross):
	x = 0
	y = 0

	for d in wire:
		print("Location: ({}, {})".format(x, y))
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

			if (cx, cy) in grid and grid[(cx, cy)] != label:
				grid[(cx, cy)] = cross
			else:
				grid[(cx, cy)] = label
		x += dx
		y += dy

def dist(x, y):
	return abs(x) + abs(y)

def closest_intersection(w1, w2):
	# make a grid
	grid = {}
	# lay out wire 1
	apply(grid, w1, 'a', 'x')
	# lay out wire 2
	apply(grid, w2, 'b', 'x')
	# identify closest intersection

	min_x = -1
	min_y = -1
	min_dist = None
	for (x, y), v in grid.items():
		if x == 0 and y == 0:
			continue
		if v == 'x':
			print("found a cross at ({}, {})".format(x, y))
			if min_dist is None or min_dist > dist(x, y):
				min_x = x
				min_y = y
				min_dist = dist(x, y)
	return (min_x, min_y)

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

x, y = closest_intersection(
	['R75','D30','R83','U83','L12','D49','R71','U7','L72'],
	['U62','R66','U55','R34','D71','R55','D58','R83'])
print("Closest: ({}, {}) ({}=159?)".format(x, y, dist(x, y)))
#
#print("Closest: {} (135?)".format(closest_intersection(
#	['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
#	['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']
#	)))


x, y = closest_intersection(wire1, wire2)

print("Closest: ({}, {}) = {}".format(x, y, dist(x, y)))
