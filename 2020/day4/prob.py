import logging
import re
logging.basicConfig(level=logging.INFO)


input_file = 'input'
#input_file = 't1'
#input_file = 't2'
#input_file = 't3'
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]


expected_fields = [
  'byr',
  'iyr',
  'eyr',
  'hgt',
  'hcl',
  'ecl',
  'pid',
#  'cid',
]

def check_year(y, min, max):
  if len(y) != 4:
    return False
  yi = int(y)
  if yi < min or yi > max:
    return False
  return True

def bad_year(y, min, max):
  return not check_year(y, min, max)

def check_height(h):
  n = int(h[0:-2])
  unit = h[-2:]
  min_h = -1
  max_h = -1
  if unit == 'cm':
    min_h = 150
    max_h = 193
  elif unit == 'in':
    min_h = 59
    max_h = 76
  else:
    return False

  if min_h < 0:
    return False

  if n < min_h or n > max_h:
    return False
  return True

def bad_height(h):
  return not check_height(h)

def check_hair_colour(c):
  return re.search('^#[0-9a-f]{6}$', c) is not None

def check_eye_colour(c):
  return c in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

def check_pid(p):
  return re.search('^[0-9]{9}$', p) is not None

def check_passport(p):
  for f in expected_fields:
    if f not in p:
      return False
  if bad_year(p['byr'], 1920, 2002):
    return False
  if bad_year(p['iyr'], 2010, 2020):
    return False
  if bad_year(p['eyr'], 2020, 2030):
    return False
  if bad_height(p['hgt']):
    return False
  if not check_hair_colour(p['hcl']):
    return False
  if not check_eye_colour(p['ecl']):
    return False
  if not check_pid(p['pid']):
    return False


  return True

all_passports = []
current = {}

for line in my_input:
  if line == '':
    all_passports.append(current)
    current = {}
  else:
    fields = line.split(' ')
    for f in fields:
      k, v = f.split(':')
      current[k] = v

if len(current) > 0:
  all_passports.append(current)

valid = 0
for p in all_passports:
  if check_passport(p):
    valid += 1

logging.info("Found {} valid passports".format(valid))