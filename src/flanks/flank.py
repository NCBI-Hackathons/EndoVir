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

  class Extension:

    def __init__(self, flank):
      self.flank = flank
      self.length = 0
      self.start = 0
      self.stop = 0
      self.alignment = None
      self.isRevCompl = False
      self.name = flank.name+"_ex"
      self.sra_rowid = 0

    def is_longer_alignment(self, alignment):
      if (alignment.read.length - abs(alignment.read.stop-alignment.read.start)+1) > self.length:
        self.length = alignment.read.length - abs(alignment.read.stop-alignment.read.start)+1
        self.alignment = alignment
        self.sra_rowid = alignment.read.sra_rowid
        return True
      return False

    def update_lhs_coordinates(self):
      self.start = 0
      if self.alignment != None:
        self.stop = self.length + abs(self.alignment.read.stop-self.alignment.read.start)

    def update_rhs_coordinates(self):
      self.stop = self.flank.contig.length
      if self.alignment != None:
        self.start = self.flank.contig.length - abs(self.alignment.read.stop-self.alignment.read.start)

    def get_contig(self):
      return self.flank.contig

  def __init__(self, ctg, side):
    self.contig = ctg
    self.length = ctg.flank_len
    self.side = side
    self.name = "{}_{}".format(self.contig.name, self.side)
    self.start = 0
    self.stop = 0
    self.ref_overlap = 5
    self.qry_overlap = 20
    self.extension = self.Extension(self)
    self.calculate_coordinates(ctg)


  def has_extension(self):
    if self.extension.alignment is None:
      return False
    return True

  def is_extended(self, alignment):
    raise NotImplementedError("Require  check_overlap() implementation")

  def get_extension(self, reads):
    raise NotImplementedError("Require  get_extension() implementation")

  def get_fasta_sequence(self):
    raise NotImplementedError("Require get_fasta_sequence() implementation")

  def calc_extension_length(self, alignment):
    raise NotImplementedError("Require calc_extension_length() implementation")

  def calculate_coordinates(self, contig):
    raise NotImplementedError("Require calculate_coordinates() implementation")

  def update_coordinates(self, amount):
    raise NotImplementedError("Require shift() implementation")
