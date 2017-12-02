#  magicblast_flank_parser.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

from . import magicblast_parser
from . import magicblast_alignment

class MagicblastFlankParser(magicblast_parser.MagicblastParser):

  def __init__(self, flankmap):
    super().__init__()
    self.flankmap = flankmap
    self.overlaps = {}

  """
    This is a  weak test considering partial mappings onto the flank
  """
  def check_single_overlap(self, flank, alignment):
    if alignment.qry.get_ordered_coords()[0] < 1:
      if flank.update_extension(alignment):
        self.overlaps[flank.name] = alignment
        #print("{}: LHS Overlap {} :: Len: {}".format(flank.name,
                                                     #flank.overlap.rowid,
                                                     #flank.overlap.length))

    if alignment.qry.get_ordered_coords()[1] < alignment.qry.length:
      if flank.update_extension(alignment):
        self.overlaps[flank.name] = alignment
        #print("{}: RHS Overlap {} :: Len: {}".format(flank.name,
                                                     #flank.overlap.rowid,
                                                     #flank.overlap.length))

  def identify_overlaps(self, cols, flank):
    a = magicblast_alignment.MagicblastAlignment(cols)
    #print("Aligned:", a.ref.name, a.qry.name, a.qry.aln_length, a.qry.aln_length, flank.contig.hasRhsFlank)
    #print("Qry\t{}\t{}\t{}\t{}".format(a.qry.start, a.qry.stop, a.qry.strand, a.qry.length))
    #print("Ref\t{}\t{}\t{}".format(a.ref.start, a.ref.stop, a.ref.strand))
    if not flank.contig.hasRhsFlank:
      if flank.name not in self.extensions:
        self.overlaps[flank.name] = None
      self.check_single_overlap(flank, a)
    else:
      if flank.has_overlap(a):
        self.overlaps[flank.name] = a

  def parse(self, src, contigs):
    alignments = []
    read_count = 0
    for i in src:
      #print(i.rstrip())
      if i[0] != '#':
        cols = i.strip().split('\t')
        if cols[1] in self.flankmap:
          if self.flankmap[cols[1]].contig.name in contigs:
            self.identify_overlaps(cols, self.flankmap[cols[1]])
        read_count += 1
    for i in self.overlaps:
      print(i, self.overlaps[i].qry.sra_rowid)
      alignments.append(self.overlaps[i])
    print("Overlapping reads: {}/{}".format(len(alignments), read_count))
    return alignments
