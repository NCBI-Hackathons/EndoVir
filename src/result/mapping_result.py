#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Implementation of a mapping result of a Read to a Reference.
#                Grouping creates uninterupted ranges to fetch reads
#                using ranges, not singles. Assumes that mappings are
#                sorted ascending by their rowids.
#                ToDo: Add sorted mapping
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

    def dump(self):
      return '\t'.join(str(x) for x in [self.name, self.length, self.sra_rowid, self.start, self.stop, self.strand, self.aln_length])

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

    def dump(self):
      return '\t'.join(str(x) for x in [self.name, self.start, self.stop, self.strand, self.aln_length])
  def __init__(self):
    self.srr = None
    self.mappings = []
    self.count = 0
    self.groups = []

  def add_mapping(self, read=None, reference=None):
    self.mappings.append([read, reference])
    self.update_groups()
    self.count += 1

  def add_read(self, read):
    self.add_mapping(read=read)

  def add_reference(self, reference):
    self.add_mapping(reference=reference)

  def update_groups(self):
    if self.isNewGroup():
      self.groups.append([self.mappings[-1][0].sra_rowid, 0])
    else:
      self.groups[-1][1] += 1

  def isNewGroup(self):
    if len(self.groups) == 0:
      return True
    if self.mappings[-1][0].sra_rowid - 1 == self.mappings[-2][0].sra_rowid:
      return False
    return True
