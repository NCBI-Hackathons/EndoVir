#  magicblast_alignment.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


class MagicblastAlignment:


  class Query:

    def __init__(self, name, start, stop, strand, qlen):
      self.name = name
      self.length = int(qlen)
      self.sra_rowid = name.split('.')[1]
      self.start = int(start) - 1
      self.stop  = int(stop) - 1
      if strand == 'plus':
        self.strand = 0
      else:
        self.strand = 1
      self.aln_length = self.stop - self.start + 1
      if self.strand == 1:
        self.aln_length *= -1

  class Reference:

    def __init__(self, name, start, stop, strand):
      self.name = name
      self.start = int(start) - 1
      self.stop  = int(stop) - 1
      if strand == 'plus':
        self.strand = 0
      else:
        self.strand = 1
      self.aln_length = self.stop - self.start + 1
      if self.strand == 1:
        self.aln_length *= -1

  def __init__(self, cols):
    self.qry = self.Query(cols[0], cols[6], cols[7], cols[13], cols[15])
    self.ref = self.Reference(cols[1], cols[8], cols[9], cols[14])

    self.pident = float(cols[2])
    self.btop = cols[16]
    self.isLhsFlank = None
    self.isRhsFlank = None
