#  flank.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.sequence.sequence

class Flank:

  class Overlap:

    def __init__(self):
      self.length = 0
      self.alignment = None
      self.isRevCompl = False

    def update(self, alignment, length):
      self.length = length
      self.alignment = alignment
      if self.alignment.qry.strand != self.alignment.ref.strand:
        self.isRevCompl = True

  def __init__(self, ctg, side):
    self.contig = ctg
    self.length = ctg.flank_len
    self.side = side
    self.name = "{}_{}".format(self.contig.name, self.side)
    self.start = 0
    self.stop = 0
    self.ref_overlap = 5
    self.qry_overlap = 20
    self.overlap = self.Overlap()
    self.calculate_coordinates(ctg)

  def has_extension(self):
    if self.overlap.alignment is None:
      return False
    return True

  def has_overlap(self, alignment):
    if self.check_overlap(alignment):
      return True
    return False

  def check_overlap(self, alignment):
    raise NotImplementedError("Require  check_overlap() implementation")

  def get_extension(self, reads):
    raise NotImplementedError("Require  get_extension() implementation")

  def get_fasta_sequence(self):
    raise NotImplementedError("Require get_fasta_sequence() implementation")

  def calc_extension_length(self, alignment):
    raise NotImplementedError("Require calc_extension_length() implementation")

  def calculate_coordinates(self, contig):
    raise NotImplementedError("Require calculate_coordinates() implementation")
