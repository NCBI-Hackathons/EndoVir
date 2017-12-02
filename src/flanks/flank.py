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

  class Extension(lib.sequence.sequence.Sequence):

    def __init__(self, name, seq, flank_to, read_to):
      super().__init__(name, seq)
      self.flank_to = flank_to
      self.read_to = read_to

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
    self.ref_overlap = 5
    self.qry_overlap = 20
    self.overlap = self.Overlap()

  def has_extension(self):
    if self.overlap.alignment is None:
      return False
    return True

  def has_overlap(self, alignment):
    if self.check_overlap(alignment):
      return True
    return False

  def mk_revcompl(self, seq, beg, end):
    return seq[beg:end+1][::-1].translate(str.maketrans("ACTG", "TGAC"))

  def check_overlap(self, alignment):
    raise NotImplementedError("Require  check_overlap() implementation")

  def get_extension(self, reads):
    raise NotImplementedError("Require  get_extension() implementation")

  def get_fasta_sequence(self):
    raise NotImplementedError("Require get_fasta_sequence() implementation")

  def calc_extension_length(self, alignment):
    raise NotImplementedError("Require calc_extension_length() implementation")
