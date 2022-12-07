from aocd.models import Puzzle
from collections import defaultdict
import logging
import re
import sys

logging.basicConfig(level=logging.DEBUG)

p = Puzzle(year=2022, day=7)

lines = p.input_data.splitlines()
#lines = [
#  "$ cd /",
#  "$ ls",
#  "dir a",
#  "14848514 b.txt",
#  "8504156 c.dat",
#  "dir d",
#  "$ cd a",
#  "$ ls",
#  "dir e",
#  "29116 f",
#  "2557 g",
#  "62596 h.lst",
#  "$ cd e",
#  "$ ls",
#  "584 i",
#  "$ cd ..",
#  "$ cd ..",
#  "$ cd d",
#  "$ ls",
#  "4060174 j",
#  "8033020 d.log",
#  "5626152 d.ext",
#  "7214296 k",
#]

p_cd = re.compile(r"^\$ cd (.+)$")
p_ls = re.compile(r"^\$ ls$")
p_subdir = re.compile(r"^dir (.+)")
p_file = re.compile(r"^(\d+) (.+)")

class Directory:
  def __init__(self, name):
    self.name = name
    self.size = 0
    self.subdirs = []
    self.parent = None
    self.path = name

root = None
pwd = None
sizes = defaultdict(int)

for line in lines:
  m = p_cd.match(line)
  if m:
    #logging.debug(f"Found a dir change: {line}")
    dir_name = m.group(1)
    if dir_name == '..':
      pwd = pwd.parent
    else:
      new_wd = Directory(dir_name)
      if pwd is not None:
        new_wd.parent = pwd
        new_wd.path = pwd.path + '/' + dir_name
        if new_wd.path in sizes:
          logging.warn(f"We've already seen this path: {new_wd.path}")
        pwd.subdirs.append(new_wd)
      else:
        root = new_wd
      pwd = new_wd
    continue
  m = p_ls.match(line)
  if m:
    #logging.debug(f"Found a ls: {line}")
    # nothing to do?
    continue
  m = p_subdir.match(line)
  if m:
    #logging.debug(f"Found a subdir: {m.group(1)}")
    # nothing to do?
    continue
  m = p_file.match(line)
  if m:
    #logging.debug(f"Found a file: {m.group(2)} of size {m.group(1)} in {pwd.path}")
    file_size = int(m.group(1))
    pwd.size += file_size
    sizes[pwd.path] += file_size
    continue
  logging.warn(f"Unhandled input line: {line}")

memo = {}

def recurse_size(directory):
  if len(directory.subdirs) == 0:
    memo[directory.path] = directory.size
    return directory.size

  total = directory.size
  for sd in directory.subdirs:
    total += recurse_size(sd)
  memo[directory.path] = total
  return total

used_space = recurse_size(root)
logging.info(f"Total size: {used_space}")

total_size = 0
for d, size in memo.items():
  if size <= 100000:
    total_size += size

logging.info(f"Part A: {total_size}")
p.answer_a = total_size

available_space = 70000000
needed_space = 30000000
unused_space = available_space - used_space
space_to_reclaim = needed_space - unused_space

smallest = used_space
for d, size in memo.items():
  if size >= space_to_reclaim and size < smallest:
    smallest = size

logging.info(f"Part B: {smallest}")
p.answer_b = smallest

