# --- Part Two ---
#
# The Elves in accounting are thankful for your help; one of them even
# offers you a starfish coin they had left over from a past vacation.
# They offer you a second one if you can find three numbers in your
# expense report that meet the same criteria.
#
# Using the above example again, the three entries that sum to 2020
# are 979, 366, and 675. Multiplying them together produces the
# answer, 241861950.
#
# In your expense report, what is the product of the three entries
# that sum to 2020?


import logging
logging.basicConfig(level=logging.INFO)

class StopIt(Exception): pass

input_file = 'input'
#input_file = 't'
with open(input_file) as fin:
  my_input = fin.readlines()

input_length = len(my_input)

try:
  for i in range(input_length):
    for j in range(i+1, input_length):
      logging.info("checking ({i}, {j})".format(i=i, j=j))
      ii = int(my_input[i])
      ji = int(my_input[j])
      if ii + ji >= 2020:
        continue
      for k in range(j+1, input_length):

        ki = int(my_input[k])
        s = ii + ji + ki
        if s == 2020:
          raise StopIt
        else:
          logging.info("found a mismatch {ii} + {ji} + {ki} = {s}".format(ii=ii, ji=ji, ki=ki, s=s))
except StopIt:
  logging.info("Line {i} ({ii}) + line {j} ({ji})  + line {k} ({ki}) = {ii} + {ji} + {ki} = 2020, Product = {p}".format(i=i, ii=ii, j=j, ji=ji, k=k, ki=ki, p=ii * ji * ki))
