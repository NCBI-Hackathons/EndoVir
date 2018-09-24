#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Fasta parser
#-------------------------------------------------------------------------------

import sys
from . import sequence

class FastaParser:

  @classmethod
  def parse_file(cls, fil, stream=False):
    src = open(fil, 'r')
    inst = cls(src=src, stream=stream)
    inst.parse()
    src.close()
    return inst

  def __init__(self, src=sys.stdin, stream=False):
    self.sequences = {}
    self.stream = stream
    self.src = src

  def parse(self):
    seq = ''
    header = ''
    for i in self.src:
      if i[0] == '>':
        if len(seq) > 0:
          self.add_sequence(sequence.Sequence(header, seq))
          seq = ''
        header = i[1:].strip()
      else:
        seq += i.strip()
    self.add_sequence(sequence.Sequence(header, seq))

  def write_file(self, fname):
    fh = open(fname, 'w')
    for i in self.sequences:
      fh.write(self.sequences[i].get_sequence())
    fh.close()
    return fname

  def add_sequence(self, seq):
    if self.stream:
      print(seq.get_sequence())
    self.sequences[seq.name] = seq
