#  magicblast_parser.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#  https://ncbi.github.io/magicblast/doc/output.html
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

  NESTED = 1
  LHS_OL = 2
  RHS_OL = 4

  def __init__(self):
    self.alignments = []

  def classify_overlap(self, cols): # qbeg, qend, rbeg, rend, qstrand, rstrand):
    if col[13] == 'minus':    # query is minus, reference is plus
      if
    elif col[14] == 'minus':  # Reference is minus , query is plus
      if col[6]
    else:                     # both should be plus
      rend = col[6]
      rbeg = col[7]


  def parse(self, src):
    self.alignments = []
    for i in src:
      cols = i.strip().split('\t')
      print(cols)
      self.alignments.append(Alignment(cols[0], cols[1], cols[2], cols[6],
                                       cols[7], cols[8], cols[9], cols[13],
                                       cols[14]))
      # 0: query
      # 1: reference
      # 2: pident
      # 6: alignment start position on the query sequence
      # 7: alignment stop  position on the query sequence
      # 8: alignment start position on the reference sequence
      # 9: alignment stop  position on the reference sequence
