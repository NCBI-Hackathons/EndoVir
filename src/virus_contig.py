#  contig.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys
import shutil
import pathlib

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.blast.magicblast
import lib.process.process
import lib.vdbdump.vdbdump
import lib.sequence.sequence
import lib.fasta.parser

import flanks.flank_lhs
import flanks.flank_rhs

class AnnealUpdate:

  def __init__(self):
    self.contig = ''
    self.shift = 0


class VirusContig(lib.sequence.sequence.Sequence):

  def __init__(self, name, seq, srr, src, flank_len, screen_dir):
    super().__init__(name, seq)
    self.src = src
    self.srr = srr
    self.flank_len = flank_len
    self.iteration = 0
    self.hasRhsFlank = True
    self.wd = self.mk_wd(os.path.join(screen_dir, self.name))
    self.lhs_flank = flanks.flank_lhs.LhsFlank(self)
    self.rhs_flank = flanks.flank_rhs.RhsFlank(self)
    self.update_flanks()
    self.hasExtension = False


  def mk_wd(self, path):
    if os.path.exists(path):
      shutil.rmtree(path)
    if not os.path.isdir(path):
      os.mkdir(path)
    return path

  def update_flanks(self):
    if self.length <= self.flank_len:
      self.hasRhsFlank = False
      self.rhs_flank.length = 0
      self.lhs_flank.length = self.length

  def log_flank_extension(self, overlap):
    print("Extension: {} : {} : {} : {}".format(self.srr,
                                                overlap.alignment.ref.name,
                                                overlap.alignment.qry.sra_rowid,
                                                overlap.isRevCompl))
  def revcomp_seq(self, seq, beg, end):
    return seq[beg:end+1][::-1].translate(str.maketrans("ACTG", "TGAC"))

  def extend_rhs(self, flank, reads):
    if flank.overlap.alignment.qry.sra_rowid in reads:
      self.log_flank_extension(flank.overlap)

      if flank.overlap.isRevCompl:
        print("DOUBLE CHECK THIS")
        print("Flank: {}\t{}".format(flank.start, flank.stop))
        print("Read:  {}\t{}".format(0, flank.overlap.alignment.qry.start))
        ext = self.revcomp_seq(reads[flank.overlap.alignment.qry.sra_rowid],
                                0,
                                flank.overlap.alignment.qry.start + 1)
        self.sequence = self.sequence[:flank.stop+1] + ext
        extend_shift = len(self.sequence) - self.length
        print(extend_shift, len(self.sequence), self.length)
        self.length = len(self.sequence)
        print(extend_shift)
        return ">{}\n{}\n".format(flank.overlap.name,
                                  self.sequence[-(extend_shift+flank.length):])

      print("Flank: {}\t{}".format(flank.start, flank.stop))
      print("Read:  {}\t{}".format(flank.overlap.alignment.qry.start,
                                   flank.overlap.alignment.qry.stop))
      self.sequence = self.sequence[:flank.stop+1] + \
                      reads[flank.overlap.alignment.qry.sra_rowid][flank.overlap.alignment.qry.stop:]
      extend_shift = len(self.sequence) - self.length
      print(extend_shift, len(self.sequence), self.length)
      self.length = len(self.sequence)
      return ">{}\n{}\n".format(flank.overlap.name,
                                self.sequence[-(extend_shift+flank.length):])

  def extend_lhs(self, flank, reads):
    if flank.overlap.alignment.qry.sra_rowid in reads:
      self.log_flank_extension(flank.overlap)
      if flank.overlap.isRevCompl:
        print("DOUBLE CHECK THIS")
        print("Flank: {}\t{}".format(flank.start, flank.stop))
        print("Read:  {}\t{}".format(flank.overlap.alignment.qry.start,
                                     flank.overlap.alignment.qry.stop))

        ext = self.revcomp_seq(reads[flank.overlap.alignment.qry.sra_rowid],
                                     flank.overlap.alignment.qry.stop,
                                     flank.overlap.alignment.qry.length)
        self.sequence = ext + self.sequence[flank.start:]
        extend_shift = len(self.sequence) - self.length
        print(extend_shift, len(self.sequence), self.length)
        self.rhs_flank.shift(self.extend_shift)
        self.length = len(self.sequence)
        return ">{}\n{}\n".format(flank.overlap.name,
                                  self.seqeunce[:extend_shift + flank.length])

      print("Flank: {}\t{}".format(flank.start, flank.stop))
      print("Read:  {}\t{}".format(flank.overlap.alignment.qry.start,
                                   flank.overlap.alignment.qry.stop))
      self.sequence = reads[flank.overlap.alignment.qry.sra_rowid][:flank.overlap.alignment.qry.start] \
                      + self.sequence[flank.start:]
      extend_shift = len(self.sequence) - self.length
      print(extend_shift, len(self.sequence), self.length)
      self.rhs_flank.shift(extend_shift)
      self.length = len(self.sequence)
      return ">{}\n{}\n".format(flank.overlap.name,
                                self.sequence[:extend_shift + flank.length])

  def get_extensions(self, reads):
    extensions = ''
    if self.lhs_flank.has_extension():
      extensions += self.extend_lhs(self.lhs_flank, reads)
      self.hasExtension = True
    if self.rhs_flank.has_extension():
      extensions += self.extend_rhs(self.rhs_flank, reads)
      self.hasExtension = True
    return extensions


  def anneal_rhs(self, rsh_ctg, overlap):
    print(overlap.rhs_start, overlap.rhs_stop, overlap.lhs_start, overlap.lhs_stop)
    self.sequence = self.sequence[:overlap.rhs_stop+1] + rsh_ctg.sequence[overlap.lhs_stop:]

    nend = len(sequence)
    print(self.name, rsh_ctg.name, nend)
    return {rsh_ctg.name : self.name}

  def get_flanks(self):
    if self.hasRhsFlank:
      return self.lhs_flank.get_fasta_sequence() + self.rhs_flank.get_fasta_sequence()
    return self.lhs_flank.get_fasta_sequence()
