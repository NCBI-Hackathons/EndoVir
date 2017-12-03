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
    print(seq, beg, end)
    return seq[beg:end+1][::-1].translate(str.maketrans("ACTG", "TGAC"))

  def extend_rhs(self, flank, reads):
    if flank.overlap.alignment.qry.sra_rowid in reads:
      print("Extension: {} : {} : {} : {}".format(self.srr,
                                                  flank.overlap.alignment.ref.name,
                                                  flank.overlap.alignment.qry.sra_rowid,
                                                  flank.overlap.isRevCompl))

      if flank.overlap.isRevCompl:
        print("DOUBLE CHECK THIS")
        print("Extension:sequence\tfrom\tto")
        print("\t{}\t{}\t{}".format(flank.name, flank.start, flank.stop))
        print("\t{}\t{}\t{}".format(flank.overlap.alignment.qry.sra_rowid, 0, flank.overlap.alignment.qry.start-1))
        flk = self.sequence[flank.start:flank.stop]
        ext = self.revcomp_seq(reads[flank.overlap.alignment.qry.sra_rowid], 0, flank.overlap.alignment.qry.start-1)
        print(flk)
        print(ext)
        return lib.sequence.sequence.Sequence(self.name+flank.name, flk+ext)

      print("Extension:sequence\tfrom\tto")
      print("\t{}\t{}\t{}".format(flank.name, flank.start, flank.stop))
      print("\t{}\t{}\t{}".format(flank.overlap.alignment.qry.sra_rowid, 0, flank.overlap.alignment.qry.start-1))
      flk = self.sequence[flank.start:flank.stop]
      print(flk)
      ext = reads[flank.overlap.alignment.qry.sra_rowid][flank.overlap.alignment.qry.stop:]
      print(ext)
      return lib.sequence.sequence.Sequence(self.name+flank.name, flk+ext)


  def extend_lhs(self, flank, reads):
    if flank.overlap.alignment.qry.sra_rowid in reads:
      print("Extension: {} : {} : {} : {}".format(self.srr,
                                                  flank.overlap.alignment.ref.name,
                                                  flank.overlap.alignment.qry.sra_rowid,
                                                  flank.overlap.isRevCompl))
      if flank.overlap.isRevCompl:
        print("DOUBLE CHECK THIS")
        print("Extension:sequence\tfrom\tto")
        print("\t{}\t{}\t{}".format(flank.overlap.alignment.qry.sra_rowid,
                                    flank.overlap.alignment.qry.stop,
                                    flank.overlap.alignment.qry.length))
        print("\t{}\t{}\t{}".format(flank.name, flank.start, flank.stop))
        ext = self.revcomp_seq(reads[flank.overlap.alignment.qry.sra_rowid],
                                     flank.overlap.alignment.qry.stop,
                                     flank.overlap.alignment.qry.length)
        flk = self.sequence[flank.start:flank.stop]
        print(ext)
        print(flk)
        return lib.sequence.sequence.Sequence(self.name+flank.name, ext+flk)

      print("\t{}\t{}\t{}".format(flank.overlap.alignment.qry.sra_rowid, 0, self.overlap.alignment.qry.start))
      print("\t{}\t{}\t{}".format(flank.name, flank.start, flank.stop))
      ext = reads[self.overlap.alignment.qry.sra_rowid][:self.overlap.alignment.qry.start]
      flk = self.sequence[flank.start:flank.stop]
      print(ext)
      print(flk)
      return lib.sequence.sequence.Sequence(self.name+flank.name, ext+flk)

  def get_extensions(self, reads):
    if self.rhs_flank.has_extension():
      return self.extend_rhs(self.rhs_flank, reads)
    #if self.lhs_flank.has_extension():
    #  return self.extend_lhs(self.rhs_flank, reads)

  def get_flanks(self):
    if self.hasRhsFlank:
      return self.lhs_flank.get_fasta_sequence() + self.rhs_flank.get_fasta_sequence()
    return self.lhs_flank.get_fasta_sequence()
