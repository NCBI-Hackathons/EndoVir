#-------------------------------------------------------------------------------
#  \file fasta_parser.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description Implementation of a biological sequence.
#-------------------------------------------------------------------------------

import sys
from . import sequence
from ..sequence import sequence_container

class FastaParser:

  def __init__(self):
    pass

  @classmethod
  def parse_file(cls, fil, stream=False):
    src = open(fil, 'r')
    cls.parse(src=src, stream=stream)
    src.close()

  def parse(self, src=sys.stdin, stream=False):
    seq_container = sequence_container.SequenceContainer()
    seq = ''
    header = ''
    for i in src:
      if i[0] == '>':
        if len(seq) > 0:
          self.add_sequence(sequence.Sequence(header, seq), stream)
          seq = ''
        header = i[1:].strip()
      else:
        seq += i.strip()
    self.add_sequence(sequence.Sequence(header, seq), stream)

  def write_file(self, fname):
    fh = open(fname, 'w')
    for i in self.sequences:
      fh.write(self.sequences[i].get_sequence())
    fh.close()
    return fname

  def add_sequence(self, seq, stream):
    if stream == True:
      print(seq.get_sequence())
    self.sequences[seq.header] = seq
