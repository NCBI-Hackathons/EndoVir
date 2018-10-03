#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Fasta parser
#-------------------------------------------------------------------------------

import sys
from utils import sequence

class FastaParser:

  def __init__(self, stream=False):
    self.sequences = {}
    self.stream = stream

  def parse(self, src=None):
    if src != None:
      self.parse_file_source(src)
    else:
      self.parse_source(sys.stdin)
    return [self.sequences[x] for x in self.sequences]

  def parse_source(self, src):
    seq = ''
    header = ''
    for i in src:
      if i[0] == '>':
        if len(seq) > 0:
          self.add_sequence(sequence.Sequence(header, seq))
          seq = ''
        header = i[1:].rstrip()
      else:
        seq += i.rstrip()
    self.add_sequence(sequence.Sequence(header, seq))

  def write_file(self, fname):
    fh = open(fname, 'w')
    for i in self.sequences:
      fh.write(self.sequences[i].sequence)
    fh.close()
    return fname

  def add_sequence(self, seq):
    if self.stream:
      print(seq.sequence)
    self.sequences[seq.name] = seq

  def parse_file_source(self, src):
    fh = open(src, 'r')
    self.parse_source(fh)
    fh.close()
