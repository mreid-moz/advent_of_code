import logging
logging.basicConfig(level=logging.INFO)


input_file = 'input'
#input_file = 't1'
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

def check_slope(slope_x, slope_y):
  tree_count = 0
  current_x = slope_x
  line_length = len(my_input[0])

  skip_lines = slope_y
  for line in my_input:
    if skip_lines > 0:
      skip_lines -= 1
    else:
      skip_lines = slope_y - 1
      xmod = current_x % line_length
      if line[xmod] == '#':
        line = line[0:xmod] + 'X' + line[xmod+1:]
        tree_count += 1
      else:
        line = line[0:xmod] + 'O' + line[xmod+1:]
      current_x += slope_x
    logging.debug("checking {}[{}]".format(line, current_x))
  logging.debug("Slope ({}, {}) hits {} trees.".format(slope_x, slope_y, tree_count))
  return tree_count

def test():
  check_slope(1,1)
  check_slope(1,2)

counts = [check_slope(n, 1) for n in [1, 3, 5, 7]]

m = 1
for c in counts:
  m = m * c

m *= check_slope(1, 2)
logging.info("Product: {}".format(m))
