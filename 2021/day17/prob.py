import logging

logging.basicConfig(level=logging.DEBUG)


#target area: x=241..275, y=-75..-49

target_x_min = 241
target_x_max = 275

target_y_min = -75
target_y_max = -49

test = False

if test:
  #target area: x=20..30, y=-10..-5
  target_x_min = 20
  target_x_max = 30

  target_y_min = -10
  target_y_max = -5

def in_target_area(x, y):
  return x >= target_x_min and x <= target_x_max and y >= target_y_min and y <= target_y_max

def behind_target_area(x, y):
  return x > target_x_max or y < target_y_min

def get_max_y_value(velocity):
  y = 0
  points = []
  while y >=target_y_min:
    y += velocity
    velocity -= 1
    points.append(y)

  # print(points)
  if any([y >= target_y_min and y <= target_y_max for y in points]):
    return max(points)

  return None

def hits_target(x_vel, y_vel):
  step = 0
  x = 0
  y = 0
  xv = x_vel
  yv = y_vel
  while x <= target_x_max and y >= target_y_min:
    step += 1
    x += xv
    y += yv
    if xv > 0:
      xv -= 1
    if xv < 0:
      xv += 1
    yv -= 1
    if in_target_area(x, y):
      logging.debug(f"Found a hit starting from {x_vel},{y_vel} at ({x},{y})")
      return True
  #logging.debug(f"Found a miss... the nearest point from {x_vel},{y_vel} is ({x},{y})")
  return False

# print(max_y)
number_of_hits = 0
# The x velocity can't be more than the max x
for x in range(276):
  for y in range(-100,1000):
    if hits_target(x, y):
      number_of_hits += 1

print(f"Number of hits {number_of_hits}")

