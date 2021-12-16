import logging
import copy
import re
import sys
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)

input_file = 'input'
if len(sys.argv) >= 2:
  input_file = sys.argv[1]
with open(input_file) as fin:
  my_input = [l.strip() for l in fin.readlines()]

TYPES = {
  'LITERAL': 4,
}

class Packet:
  def __init__(self, input_string, mode='hex'):
    self.raw_packet = input_string
    self.parse(mode)

  def parse(self, mode='hex'):
    # turn hex into binary
    if mode == 'binary':
      self.binary_packet = self.raw_packet
    else:
      self.binary_packet = "{0:b}".format(int(self.raw_packet, 16))
      if self.raw_packet[0] < '8':
        self.binary_packet = '0' + self.binary_packet
      if self.raw_packet[0] < '4':
        self.binary_packet = '0' + self.binary_packet
      if self.raw_packet[0] < '2':
        self.binary_packet = '0' + self.binary_packet
      if self.raw_packet[0] < '1':
        self.binary_packet = '0' + self.binary_packet
    logging.debug("Binary packet:  {}".format(self.binary_packet))
    self.read_position = 0
    while not re.match('^0*$', self.binary_packet[self.read_position:]):
      self.parse_one_packet()

  def read(self, num_bits):
    val = self.binary_packet[self.read_position:self.read_position+num_bits]
    self.read_position += num_bits
    return val

  def parse_one_packet(self):
    # 3 bits -> version
    self.version = int(self.read(3), 2)
    logging.debug("Packet version: {}".format(self.version))

    # 3 bits -> type id
    self.type_id = int(self.read(3), 2)
    logging.debug("Packet type id: {}".format(self.type_id))

    if self.type_id == TYPES['LITERAL']:
      # break into chunks of 5 bits
      literal_string = self.binary_packet[6:]
      literal_bits = ''
      for i in range(0, len(literal_string), 5):
        literal_chunk = literal_string[i:i+5]
        literal_bits += literal_chunk[1:]
        if literal_chunk[0] == '0':
          # last one
          break
      self.literal_value = int(literal_bits, 2)
      logging.debug("Packet literal value: {}".format(self.literal_value))
    else:
      # Operator packet
      self.length_type_id = self.binary_packet[6]

      if self.length_type_id == '0':
        total_subpacket_length = int(self.binary_packet[7:22], 2)
        logging.debug("Total subpacket length: {}".format(total_subpacket_length))

        subpacket_string = self.binary_packet[22:22+total_subpacket_length]
        subpackets = Packet(subpacket_string, mode='binary')
        subpackets.parse()



for line in my_input:
  p = Packet(line)
