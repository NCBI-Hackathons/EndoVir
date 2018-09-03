#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Implementation of a mapping result of a Read to a Reference.
#-------------------------------------------------------------------------------


class MappingResult:

  class Read:

    def __init__(self, name, sra_rowid, start, stop, strand, length):
      self.name = name
      self.length = int(length)
      self.sra_rowid = int(sra_rowid)
      self.start = int(start) - 1
      self.stop = int(stop) - 1
      self.strand = 1 if strand == 'minus' else 0
      self.aln_length = abs(self.stop - self.start) + 1

    def get_ordered_coords(self):
      if self.strand == 0:
        return (self.start, self.stop)
      return (self.stop, self.start)

  class Reference:

    def __init__(self, name, start, stop, strand):
      self.name = name
      self.start = int(start) - 1
      self.stop = int(stop) - 1
      self.strand = 1 if strand == 'minus' else 0
      self.aln_length = abs(self.stop - self.start) + 1

    def get_ordered_coords(self):
      if self.strand == 0:
        return (self.start, self.stop)
      return (self.stop, self.start)

  def __init__(self, read=None, flank=None):
    self.read = read
    self.flank = flank

  def add_read(self, name, start, stop, strand, length):
    self.read = self.Read(name, sra_rowid, start, stop, strand, length)

  def add_reference(self, name, start, stop, strand):
    self.reference = self.Reference(name, start, stop, strand)
