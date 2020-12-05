import logging
logging.basicConfig(level=logging.INFO)

class StopIt(Exception): pass

input_file = 'input'
#input_file = 't'
with open(input_file) as fin:
  my_input = fin.readlines()

valid_passwords = 0

# Part 1
for line in my_input:
  counts, letter_colon, password = line.split(" ")
  s_minimum, s_maximum = counts.split("-")
  minimum = int(s_minimum)
  maximum = int(s_maximum)
  letter = letter_colon[0]
  letter_count = 0
  for l in password:
    if letter == l:
      letter_count += 1
  #logging.info("Found {} {}'s in {}.".format(letter_count, letter, password))
  if letter_count >= minimum and letter_count <= maximum:
    valid_passwords += 1

logging.info("Found {} valid passwords".format(valid_passwords))

# Part 2
valid_passwords = 0
for line in my_input:
  counts, letter_colon, password = line.split(" ")
  s_p1, s_p2 = counts.split("-")
  p1 = int(s_p1)
  p2 = int(s_p2)
  letter = letter_colon[0]
  letter_count = 0
  if password[p1-1] == letter:
    letter_count += 1
  if password[p2-1] == letter:
    letter_count += 1
  #logging.info("Found {} {}'s in {}.".format(letter_count, letter, password))
  if letter_count == 1:
    valid_passwords += 1

logging.info("Found {} valid passwords".format(valid_passwords))
