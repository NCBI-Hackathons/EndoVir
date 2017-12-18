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

class ContigUpdate:

  def __init__(self, flank, shift):
    self.flank = flank
    self.shift = shift

class VirusContig(lib.sequence.sequence.Sequence):

  def __init__(self, name, seq, srr, src, flank_len, screen_dir):
    super().__init__(name, seq)
    self.src = src
    self.srr = srr
    self.flank_len = flank_len
    self.iteration = 0
    self.wd = self.mk_wd(os.path.join(screen_dir, self.name))
    self.lhs_flank = flanks.flank_lhs.LhsFlank(self)
    self.rhs_flank = flanks.flank_rhs.RhsFlank(self)
    self.update_flanks()
    self.hasExtension = False
    self.hasRhsFlank = True
    self.shift = 0

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

  def log_overlap_coords(self, flank):
    fstart = flank.start
    fstop = flank.stop
    rstart = flank.extension.alignment.read.start
    rstop = flank.extension.alignment.read.stop
    if flank.side == 'rhs' and flank.extension.isRevCompl:
      rstart = 0
      rstop = flank.extension.alignment.reads.length

    print("Flank: {}\t{}\t{}\t{}".format(fstart,fstop,  self.length,
                                         flank.extension.alignment.contig.strand))
    print("Read:  {}\t{}\t{}\t{}".format(rstart,rstop,
                                         flank.extension.alignment.read.length,
                                         flank.extension.alignment.read.strand))

  def log_flank_extension(self, extension):
    print("Extension: {} : {} : {} : {}".format(self.srr,
                                                extension.alignment.contig.name,
                                                extension.alignment.read.sra_rowid,
                                                extension.isRevCompl))
  def revcomp_seq(self, seq, beg, end):
    return seq[beg:end+1][::-1].translate(str.maketrans("ACTG", "TGAC"))

  def extend_lhs(self, flank, reads):
    if flank.extension.sra_rowid in reads:
      self.log_flank_extension(flank.extension)
      if flank.extension.isRevCompl:
        print("DOUBLE CHECK THIS")
        self.log_overlap_coords(flank)
        ext = self.revcomp_seq(reads[flank.extension.sra_rowid],
                                     flank.extension.alignment.read.stop,
                                     flank.extension.alignment.read.length)

        self.update_sequence(ext + self.sequence[flank.start:])
        return ">{}\n{}\n".format(flank.extension.name, self.seqeunce[:flank.length])
      self.update_sequence(reads[flank.extension.sra_rowid][:flank.extension.alignment.read.start+1] \
                            + self.sequence[flank.start:])
      return ">{}\n{}\n".format(flank.extension.name, self.sequence[:flank.length])

  def extend_rhs(self, flank, reads):
    if flank.extension.sra_rowid in reads:
      self.log_flank_extension(flank.extension)

      if flank.extension.isRevCompl:
        print("DOUBLE CHECK THIS")
        self.log_overlap_coords(flank)
        ext = self.revcomp_seq(reads[flank.extension.sra_rowid], 0,
                               flank.extension.alignment.read.start+1)
        self.update_sequence(self.sequence[:flank.stop+1] + ext)
        return ">{}\n{}\n".format(flank.extension.name, self.sequence[-flank.length:])

      self.log_overlap_coords(flank)
      self.update_sequence(self.sequence[:flank.stop+1] + \
                      reads[flank.extension.sra_rowid][flank.extension.alignment.read.stop:])
      return ">{}\n{}\n".format(flank.extension.name, self.sequence[-flank.length:])




  def merge_contig_rhs(self, lhs_flank, rhs_contig, coords):
    this_ctg_from = self.length - self.rhs_flank.length + coords.lhs_from
    this_ctg_to = self.length - self.rhs_flank.length + coords.lhs_to
    rhs_contig_from = coords.rhs_from
    rhs_contig_to = coords.rhs_to
    print("Src: {}\t{}".format(self.name, self.length))
    print(" RHS_flank: {}\t{}\t{}".format(self.rhs_flank.start, self.rhs_flank.stop, self.rhs_flank.length))
    print("  Extension: {}\t{}\t{}".format(self.rhs_flank.extension.start, self.rhs_flank.extension.stop, self.rhs_flank.extension.length))
    print("Dst: {}\t{}\t{}\t{}\t{}".format(rhs_contig.name, rhs_contig.length, rhs_contig_from, rhs_contig_to, rhs_contig.lhs_flank.extension.start))
    print("Brk: {}\t{}\t{}\t{}".format(self.name, this_ctg_from-1, rhs_contig.name, coords.rhs_from))
    print("-------------------")
    #fh = open(self.name+rhs_contig.name, 'w')
    #fh.write(self.sequence[:this_ctg_from]+rhs_contig[])

  def get_extensions(self, reads):
    extensions = ''
    if self.lhs_flank.has_extension():
      extensions += self.extend_lhs(self.lhs_flank, reads)
      self.hasExtension = True
    if self.rhs_flank.has_extension():
      extensions += self.extend_rhs(self.rhs_flank, reads)
      self.hasExtension = True
    return extensions

  def get_flanks(self):
    if self.hasRhsFlank:
      return self.lhs_flank.get_fasta_sequence() + self.rhs_flank.get_fasta_sequence()
    return self.lhs_flank.get_fasta_sequence()

  def update_sequence(self, new_seq):
    self.shift = len(new_seq) - self.length
    self.sequence = new_seq
    self.length = len(new_seq)
    self.lhs_flank.stop = self.lhs_flank.length
    self.lhs_flank.extension.update_lhs_coordinates()
    self.rhs_flank.update_coordinates()
    self.rhs_flank.extension.update_rhs_coordinates()
    print("Ctg\tlen\tlEbeg\tlEend\tlFbeg\tlFend\trFbeg\trFend\trEbeg\trEend")
    print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.name,
                                                          self.length,
                                                          self.lhs_flank.extension.start,
                                                          self.lhs_flank.extension.stop,
                                                          self.lhs_flank.start,
                                                          self.lhs_flank.stop,
                                                          self.rhs_flank.start,
                                                          self.rhs_flank.stop,
                                                          self.rhs_flank.extension.start,
                                                          self.rhs_flank.extension.stop))
