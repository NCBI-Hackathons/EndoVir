#  flank_rhs.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

from . import flank

class RhsFlank(flank.Flank):

  def __init__(self, contig):
    super().__init__(contig, 'rhs')
    self.contig_overlap = 20
    self.read_overlap = 20

  def calculate_coordinates(self, contig):
    self.start = contig.length - contig.flank_len
    self.stop = contig.length


  def get_fasta_sequence(self):
    return ">{}\n{}\n".format(self.name, self.contig.sequence[-self.length:])

  def is_extended(self, alignment):
    if (alignment.contig.get_ordered_coords()[1] > (self.length - self.contig_overlap)) and \
       (alignment.read.get_ordered_coords()[1] < alignment.read.length - self.read_overlap):
      return self.extension.is_longer_alignment(alignment)
    return False

  def update_coordinates(self):
    self.start = self.contig.length - self.length
    self.stop = self.contig.length
