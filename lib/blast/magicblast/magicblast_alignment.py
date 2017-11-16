#  magicblast_alignment.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0


class MagicblastAlignment:

  class Query:

    def __init__(self, name, start, stop, strand):
      self.name = name
      self.sra_rowid = name.split('.')[1]
      self.start = int(start)
      self.stop = int(stop)
      self.strand = 0 if strand == 'plus' else 1
      self.aln_length = self.stop - self.start + 1
      if self.strand == 1:
        self.aln_length *= 1

  class Reference:

    def __init__(self, name, start, stop, strand):
      self.name = name
      self.start = int(start)
      self.stop = int(stop)
      self.strand = 0 if strand == 'plus' else 1
      self.aln_length = self.stop - self.start + 1
      if self.strand == 1:
        self.aln_length *= 1

  def __init__(self, cols):
    self.qry = self.Query(cols[0], cols[6], cols[7], cols[13])
    self.ref = self.Reference(cols[1], cols[7], cols[8], cols[14])
    self.pident = float(cols[2])
    self.btop = cols[16]
