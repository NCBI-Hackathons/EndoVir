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

  def __init__(self, name, shift):
    self.contig = name
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
    rstart = flank.overlap.alignment.qry.start
    rstop = flank.overlap.alignment.qry.stop
    if flank.side == 'rhs' and flank.overlap.isRevCompl:
      rstart = 0
      rstop = flank.overlap.alignment.qry.length

    print("Flank: {}\t{}\t{}\t{}".format(fstart,fstop,
                                         self.length,
                                         flank.overlap.alignment.ref.strand))
    print("Read:  {}\t{}\t{}\t{}".format(rstart,rstop,
                                         flank.overlap.alignment.qry.length,
                                         flank.overlap.alignment.qry.strand))


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
        self.log_overlap_coords(flank)
        ext = self.revcomp_seq(reads[flank.overlap.alignment.qry.sra_rowid],
                                0,
                                flank.overlap.alignment.qry.stop+1)
        self.update_sequence(self.sequence[:flank.stop+1] + ext)
        return ">{}\n{}\n".format(flank.overlap.name,
                                  self.sequence[-flank.length:])

      self.log_overlap_coords(flank)
      self.update_sequence(self.sequence[:flank.stop+1] + \
                      reads[flank.overlap.alignment.qry.sra_rowid][flank.overlap.alignment.qry.stop:])
      return ">{}\n{}\n".format(flank.overlap.name,
                                self.sequence[-flank.length:])

  def extend_lhs(self, flank, reads):
    if flank.overlap.alignment.qry.sra_rowid in reads:
      self.log_flank_extension(flank.overlap)
      if flank.overlap.isRevCompl:
        print("DOUBLE CHECK THIS")
        self.log_overlap_coords(flank)
        ext = self.revcomp_seq(reads[flank.overlap.alignment.qry.sra_rowid],
                                     flank.overlap.alignment.qry.stop,
                                     flank.overlap.alignment.qry.length)

        self.update_sequence(ext + self.sequence[flank.start:])
        return ">{}\n{}\n".format(flank.overlap.name,
                                  self.seqeunce[:flank.length])
      self.update_sequence(reads[flank.overlap.alignment.qry.sra_rowid][:flank.overlap.alignment.qry.start+1] \
                            + self.sequence[flank.start:])
      return ">{}\n{}\n".format(flank.overlap.name,
                                self.sequence[:flank.length])

  def get_extensions(self, reads):
    extensions = ''
    if self.lhs_flank.has_extension():
      extensions += self.extend_lhs(self.lhs_flank, reads)
      self.hasExtension = True
    if self.rhs_flank.has_extension():
      extensions += self.extend_rhs(self.rhs_flank, reads)
      self.hasExtension = True
    return extensions


  def anneal_rhs(self, rhs_seq, overlap):
    print("Annealing {} on {} with {} on {}".format(self.name,
                                                    self.rhs_flank.side,
                                                    rhs_seq.contig.name,
                                                    rhs_seq.side))
    print("{} - {} - {}".format(self.length, self.rhs_flank.length, overlap.lhs_start))
    print("{}: from {} to {}".format(self.name, 0,
                                   self.length-self.rhs_flank.length+overlap.lhs_start))
    print("\n{}: from {} to {}".format(rhs_seq.name,overlap.lhs_start, rhs_seq.contig.length))
    fh = open(self.name+".fa", 'w')
    fh.write(">{}\n{}\n".format(self.name, self.sequence))
    fh.close()
    fh = open(rhs_seq.contig.name+".fa", 'w')
    fh.write(">{}\n{}\n".format(rhs_seq.contig.name, rhs_seq.contig.sequence))
    fh.close()
    self.sequence = self.sequence[:self.length-self.rhs_flank.length+overlap.lhs_start]  \
                    + rhs_seq.contig.sequence[overlap.rhs_stop:]
    fh = open(self.name+"_"+rhs_seq.contig.name+".fa", 'w')
    fh.write(">{}\n{}\n".format(self.name+"_"+rhs_seq.contig.name, self.sequence))
    fh.close()
    sys.exit()

  def get_flanks(self):
    if self.hasRhsFlank:
      return self.lhs_flank.get_fasta_sequence() + self.rhs_flank.get_fasta_sequence()
    return self.lhs_flank.get_fasta_sequence()

  def update_sequence(self, new_seq):
    self.shift = len(new_seq) - self.length
    self.sequence = new_seq
    self.length = len(new_seq)
    self.rhs_flank.update_coordinates()
    self.lhs_flank.stop = self.lhs_flank.length
