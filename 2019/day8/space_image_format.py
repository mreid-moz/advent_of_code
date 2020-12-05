with open("input") as fin:
  data = fin.readline().strip()

layers = []
for i in range(int(len(data) / 150)):
  layers.append(data[i*150:(i+1)*150])

#print("{}".format(layers))

def count_digits(s, d):
  n = 0
  for c in list(s):
    if c == d:
      n += 1
  return n

min_zero_count = 200
min_zero_layer = -1

for i in range(len(layers)):
  n = count_digits(layers[i], '0')
  if n < min_zero_count:
    min_zero_count = n
    min_zero_layer = i

num_ones = count_digits(layers[min_zero_layer], '1')
num_twos = count_digits(layers[min_zero_layer], '2')
print("Found {} layers".format(len(layers)))
print("First Layer: {}".format(layers[0]))
print("Last Layer:  {}".format(layers[-1]))
print("Fewest 0s:   {}".format(layers[min_zero_layer]))

print("Layer {} had the fewest zeroes ({}). On that layer there were {} ones x {} twos = {}.".format(
  min_zero_layer, min_zero_count,  num_ones, num_twos, num_ones * num_twos
))

def show(g):
  rows = len(g[0])
  cols = len(g)

  for y in range(rows):
    for x in range(cols):
      print(g[x][y], end="")
    print("")
  print("")

def apply(g, layer):
  rows = []
  for i in range(int(len(layer) / 25)):
    rows.append(layer[i*25:(i+1)*25])

  #for row in rows:
  #  print(row.replace('2', ' ').replace('1', 'O').replace('0','.'))

  #print("There were {} rows".format(len(rows)))

  #print("Before:")
  #show(g)
  for y in range(len(rows)):
    for x in range(len(rows[0])):
      pixel = rows[y][x]
      if pixel != '2':
        g[x][y] = 'o' if pixel == '1' else '.'
  #print("After:")
  #show(g)


grid = [[' '] * 6 for i in range(25)]

#grid[13][4] = 'x'

#show(grid)
for layer in reversed(layers):
  apply(grid, layer)

#apply(grid, layers[0])
#apply(grid, layers[12])

show(grid)

