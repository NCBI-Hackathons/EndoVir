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
    self.ref_overlap = 5
    self.qry_overlap = 20

  def calculate_coordinates(self, contig):
    self.start = 0
    self.stop = contig.flank_len

  def get_fasta_sequence(self):
    return ">{}\n{}\n".format(self.name, self.contig.sequence[:self.length])

  def calc_extension_length(self, alignment):
    return alignment.qry.start + 1

  def update_extension(self, alignment):
    if self.calc_extension_length(alignment) > self.overlap.length:
      self.overlap.update(alignment, self.calc_extension_length(alignment))
      self.stop = alignment.ref.stop
      self.start = alignment.ref.start
      return True
    return False

  def check_overlap(self, alignment):
    if alignment.ref.get_ordered_coords()[0] < self.ref_overlap and \
       alignment.qry.get_ordered_coords()[0] > self.qry_overlap:
      return self.update_extension(alignment)
    return False
