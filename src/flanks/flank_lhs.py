#  flank_lhs.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

from . import flank

class LhsFlank(flank.Flank):

  def __init__(self, contig):
    super().__init__(contig, 'lhs')
    self.contig_overlap = 5
    self.read_overlap = 20

  def calculate_coordinates(self, contig):
    self.start = 0
    self.stop = contig.flank_len

  def get_fasta_sequence(self):
    return ">{}\n{}\n".format(self.name, self.contig.sequence[:self.length])

  def is_extended(self, alignment):
    if alignment.contig.get_ordered_coords()[0] < self.read_overlap and \
       alignment.read.get_ordered_coords()[0] > self.contig_overlap:
      return self.extension.is_longer_alignment(alignment)
    return False
