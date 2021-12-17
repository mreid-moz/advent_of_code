import logging
import copy
import re
import sys
from collections import defaultdict
from functools import reduce

logging.basicConfig(level=logging.INFO)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

TYPES = {
  'SUM': 0,
  'PRODUCT': 1,
  'MINIMUM': 2,
  'MAXIMUM': 3,
  'LITERAL': 4,
  'GT': 5,
  'LT': 6,
  'EQ': 7,
}

class Packet:
  def __init__(self, version, type_id, literal_value, subpackets=None):
    self.version = version
    self.type_id = type_id
    self.literal_value = literal_value
    self.subpackets = subpackets

  def version_sum(self):
    if self.type_id == TYPES['LITERAL']:
      return self.version
    return self.version + sum([p.version_sum() for p in self.subpackets])

  def eval(self):
    if self.type_id == TYPES['LITERAL']:
      return self.literal_value
    if self.type_id == TYPES['SUM']:
      return sum([p.eval() for p in self.subpackets])
    if self.type_id == TYPES['PRODUCT']:
      return reduce((lambda x, y: x * y), [p.eval() for p in self.subpackets])
    if self.type_id == TYPES['MINIMUM']:
      return min([p.eval() for p in self.subpackets])
    if self.type_id == TYPES['MAXIMUM']:
      return max([p.eval() for p in self.subpackets])

    a = self.subpackets[0].eval()
    b = self.subpackets[1].eval()
    if self.type_id == TYPES['GT']:
      if a > b:
        return 1
      return 0
    if self.type_id == TYPES['LT']:
      if a < b:
        return 1
      return 0
    if self.type_id == TYPES['EQ']:
      if a == b:
        return 1
      return 0
    return None

class Decoder:
  def __init__(self, input_string, mode='hex'):
    self.raw_packet = input_string
    self.packets = []
    self.decode_raw(mode)
    self.read_position = 0

  def decode_raw(self, mode='hex'):
    # turn hex into binary if needed
    if mode == 'binary':
      self.binary_packet = self.raw_packet
    else:
      self.binary_packet = ''.join(['{:04b}'.format(int(x, 16)) for x in self.raw_packet])
    logging.debug("Binary packet:  {}".format(self.binary_packet))

  def parse(self, mode='hex'):
    while not re.match('^[0]*$', self.binary_packet[self.read_position:]):
      if self.read_position >= len(self.binary_packet) - 1:
        break
      self.packets += self.parse_one_packet()

  def read(self, num_bits, as_int=False):
    val = self.binary_packet[self.read_position:self.read_position+num_bits]
    self.read_position += num_bits
    return val

  def read_int(self, num_bits):
    return int(self.read(num_bits, as_int=True), 2)

  def eval(self):
    logging.debug(f"Evaluating {len(self.packets)} packets")
    return self.packets[0].eval()


  def parse_one_packet(self):
    logging.debug("Parsing one packet starting from position {}".format(self.read_position))

    # 3 bits -> version
    version = self.read_int(3)
    logging.debug("Packet version: {}".format(version))

    # 3 bits -> type id
    type_id = self.read_int(3)
    logging.debug("Packet type id: {}".format(type_id))

    if type_id == TYPES['LITERAL']:
      # break into chunks of 5 bits
      literal_bits = ''
      while True:
        literal_chunk = self.read(5)
        literal_bits += literal_chunk[1:]
        if literal_chunk[0] == '0':
          # last one
          break
      literal_value = int(literal_bits, 2)
      logging.debug("Packet literal value: {}".format(literal_value))
      return [Packet(version, type_id, literal_value)]
    else:
      # Operator packet
      op_start = self.read_position
      logging.debug("Begin parsing operator packet starting at {}".format(op_start))
      length_type_id = self.read(1)

      if length_type_id == '0':
        total_subpacket_length = self.read_int(15)
        logging.debug("Total subpacket length: {}".format(total_subpacket_length))

        subpacket_string = self.read(total_subpacket_length)

        logging.debug("Parsing subpackets from: {}".format(subpacket_string))

        subpackets = Decoder(subpacket_string, mode='binary')
        subpackets.parse()
        return [Packet(version, type_id, None, subpackets.packets)]
      else:
        # If the length type ID is 1, then the next 11 bits are a number that
        # represents the number of sub-packets immediately contained by this packet.
        number_of_subpackets = self.read_int(11)
        logging.debug("Begin parsing {} subpackets".format(number_of_subpackets))
        subpackets = []
        for i in range(number_of_subpackets):
          subpackets += self.parse_one_packet()
        logging.debug("Finished parsing subpackets from operator starting at {}".format(op_start))
        return [Packet(version, type_id, None, subpackets)]

d = Decoder(my_input[0], mode='hex')
d.parse()

logging.info("Version sum: {}".format(d.packets[0].version_sum()))

result = d.eval()
logging.info("Result: {}".format(result))
