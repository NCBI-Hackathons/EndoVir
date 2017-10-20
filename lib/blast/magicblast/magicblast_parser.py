#  magicblast_parser.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


import sys

class Alignment:

  class Query:

    def __init__(self, name, start, stop, strand):
      self.name = name
      self.start = int(start)
      self.stop = int(stop)
      self.strand = 0 if strand == 'plus' else 1
      self.length = self.stop - self.start + 1
      if self.strand == 1:
        self.length = self.start - self.stop + 1

  class Reference:

    def __init__(self, name, start, stop, strand):
      self.name = name
      self.start = int(start)
      self.stop = int(stop)
      self.strand = 0 if strand == 'plus' else 1
      self.length = self.stop - self.start + 1
      if self.strand == 1:
        self.length = self.start - self.stop + 1

  def __init__(self, qry, ref, pident, qbeg, qend, rbeg, rend, qstrand, rstrand):
    self.qry = self.Query(qry, qbeg, qend, qstrand)
    self.ref = self.Reference(ref, rbeg, rend, rstrand)
    self.pident = float(pident)
    self.sra_rowid = qry.split('.')[1]

class MagicblastParser:

  def __init__(self):
    self.alignments = []

  def parse(self, src):
    for i in src:
      #cols = i.decode().strip().split('\t')
      cols = i.strip().split('\t')
      self.alignments.append(Alignment(cols[0], cols[1], cols[2], cols[6],
                                       cols[7], cols[8], cols[9], cols[13],
                                       cols[14]))
