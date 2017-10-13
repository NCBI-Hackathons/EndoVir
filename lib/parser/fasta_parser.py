#  fasta_parser.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import sys
from ..sequences import fasta
class FastaParser:

  def __init__(self):
    self.sequences = []
    self.doFhClose = False

  def read(self, fil=None):
    src = sys.stdin

    if fil != None:
      src = open(fil, 'r')
      self.doFhClose = True
    seq = ''
    header = ''
    for i in src:
      if i[0] == '>':
        if len(seq) > 0:
          self.add_sequence(fasta.FastaSequence(header, seq))
          seq = ''
        header = i[1:].strip()
      else:
        seq += i.strip()
    self.add_sequence(fasta.FastaSequence(header, seq))

    if self.doFhClose == True:
      src.close()

  def write_fasta(self, fname):
    fh = open(fname, 'w')
    for i in self.sequences:
      fh.write(i.get_sequence())
    fh.close()
    return fname

  def stream_fasta(self):
    stream = io.StringIO()
    for i in self.sequences:
      print(i.get_sequence(), file=stream)
    yield stream.getvalue()

  def add_sequence(self, seq):
    self.sequences.append(seq)
