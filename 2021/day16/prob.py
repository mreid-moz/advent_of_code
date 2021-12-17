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
  def __init__(self, version):
    self.version = version

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
    #self.read_position = 0
    while not re.match('^[0]*$', self.binary_packet[self.read_position:]):
      #logging.debug("Parsing more... {}".format(self.binary_packet[self.read_position:]))
      if self.read_position >= len(self.binary_packet) - 1:
        break
      self.packets += self.parse_one_packet()

  def read(self, num_bits, as_int=False):
    val = self.binary_packet[self.read_position:self.read_position+num_bits]
    self.read_position += num_bits
    return val

  def read_int(self, num_bits):
    return int(self.read(num_bits, as_int=True), 2)

  def parse_one_packet(self):
    logging.debug("Parsing one packet starting from position {}".format(self.read_position))

    # 3 bits -> version
    self.version = self.read_int(3)
    logging.debug("Packet version: {}".format(self.version))

    # 3 bits -> type id
    self.type_id = self.read_int(3)
    logging.debug("Packet type id: {}".format(self.type_id))

    if self.type_id == TYPES['LITERAL']:
      # break into chunks of 5 bits
      literal_bits = ''
      #bits_read = 0
      while True:
        literal_chunk = self.read(5)
        #bits_read += 5
        literal_bits += literal_chunk[1:]
        if literal_chunk[0] == '0':
          # last one
          ## todo: Read any leftover junk?
          #self.read(4 - (bits_read % 4))
          break
      self.literal_value = int(literal_bits, 2)
      logging.debug("Packet literal value: {}".format(self.literal_value))
      return [Packet(self.version)]
    else:
      # Operator packet
      op_start = self.read_position
      logging.debug("Begin parsing operator packet starting at {}".format(op_start))
      self.length_type_id = self.read(1)
      op = Packet(self.version)
      op_packets = [op]

      if self.length_type_id == '0':
        total_subpacket_length = self.read_int(15)
        logging.debug("Total subpacket length: {}".format(total_subpacket_length))

        subpacket_string = self.read(total_subpacket_length)

        logging.debug("Parsing subpackets from: {}".format(subpacket_string))

        subpackets = Decoder(subpacket_string, mode='binary')
        subpackets.parse()
        # TODO: do we need to adjust the read_position anywhere?
        return op_packets + subpackets.packets
      else:
        # If the length type ID is 1, then the next 11 bits are a number that
        # represents the number of sub-packets immediately contained by this packet.
        number_of_subpackets = self.read_int(11)
        logging.debug("Begin parsing {} subpackets".format(number_of_subpackets))
        for i in range(number_of_subpackets):
          op_packets += self.parse_one_packet()
        logging.debug("Finished parsing subpackets from operator starting at {}".format(op_start))
        return op_packets

for line in my_input:
  d = Decoder(line, mode='hex')
  d.parse()
  version_sum = 0
  for p in d.packets:
    logging.info("Found a packet with version {}".format(p.version))
    version_sum += p.version

logging.info("Version sum: {}".format(version_sum))
