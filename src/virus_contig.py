#  contig.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys
import pathlib

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.blast.magicblast
import lib.process.process
import lib.vdbdump.vdbdump
import lib.sequence.sequence
import lib.fasta.parser

import flanks.flank_lhs
import flanks.flank_rhs

class VirusContig(lib.sequence.sequence.Sequence):

  def __init__(self, name, seq, srr, src, flank_len, screen_dir, flankdb):
    super().__init__(name, seq)
    self.src = src
    self.srr = srr
    self.flankdb = flankdb
    self.flank_len = flank_len
    self.iteration = 0
    self.hasRhsFlank = True
#    self.wd = os.path.join(screen_dir, self.name)
    self.lhs_flank = flanks.flank_lhs.LhsFlank(self)
    self.rhs_flank = flanks.flank_rhs.RhsFlank(self)
    self.update_flanks()
    self.extension_map = {}

  def update_flanks(self):
    if self.length <= self.flank_len:
      self.hasRhsFlank = False
      self.rhs_flank.length = 0
      self.lhs_flank.length = self.length

  def revcomp_seq(self, seq, beg, end):
    revcomp_seq = seq[beg:end+1][::-1]
    return revcomp_seq.translate(str.maketrans("ACTG", "TGAC"))

  def extend(self, reads):
    #if self.lhs_flank.has_extension():
      #if self.lhs_flank.overlap.alignment.qry.sra_rowid in reads:
        #ext = self.lhs_flank.get_extension(reads)
        #self.extension_map[self.lhs_flank] = ext

    if self.rhs_flank.has_extension():
      if self.rhs_flank.overlap.alignment.qry.sra_rowid in reads:
        ext = self.rhs_flank.get_extension(reads)
        self.extension_map[self.rhs_flank] = ext

  def get_extensions(self, reads):
    self.extend(reads)
    if len(self.extension_map) == 0:
      print("No extensions for {}".format(self.name))
    else:
      exts = ''
      for i in self.extension_map:
        exts += ">{}\n{}\n".format(self.extension_map[i].name, self.extension_map[i].sequence)
      return exts

  def get_flanks(self):
    if self.hasRhsFlank:
      return self.lhs_flank.get_fasta_sequence() + self.rhs_flank.get_fasta_sequence()
    return self.lhs_flank.get_fasta_sequence()
