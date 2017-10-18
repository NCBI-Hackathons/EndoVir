#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  bud.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#   The Python implementation of ViruSpy [0] to allow better control of
#   MagicBLAST [1].
#
# [0] https://github.com/NCBI-Hackathons/ViruSpy
# [1] ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/1.0.0
#  Version: 0.0

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.blastdb.makeblastdb
import lib.fasta.parser
import lib.magicblast.magicblast
import lib.vdbdump.vdbdump
import lib.megahit.megahit

class Flanker(lib.fasta.parser.FastaParser):

  def __init__(self, flank_len):
    super().__init__()
    self.len_flank = flank_len
    self.lhs_count = 0
    self.rhs_count = 0

  def add_sequence(self, seq):
    if seq.length <= self.len_flank:
      seq.name += "_lhs"
      self.sequences.append(seq)
      self.lhs_count += 1
    else:
      self.sequences.append(seq.subseq(0, self.len_flank, seq.name+"_lhs"))
      self.sequences.append(seq.subseq(seq.length-self.len_flank, self.len_flank, seq.name+"_rhs"))
      self.lhs_count += 1
      self.rhs_count += 1

class Buddy:

  def __init__(self):
    self.len_flank = 500
    self.srascreener = lib.magicblast.magicblast.Magicblast()
    self.vbddump =  lib.vdbdump.vdbdump.VdbDump()
    self.assembler = lib.megahit.megahit.Megahit()

  def screen_srr(self, db=None, srr=None):
    return self.srascreener.run(db, srr)

  def get_flanks(self, alignments, srr):
    print("Fetching flanking sequences", file=sys.stderr)
    flanks = 'flanks.fq'
    fh_flanks = open(flanks, 'w')
    seqs = self.vbddump.run(srr, alignments, fh_flanks)
    fh_flanks.close()
    return flanks

  def assemble(self, flanks)
    print("Running meggahit with flanking sequences", file=sys.stderr)
    self.assembler.out_prefix = srr
    mgh.out_dir = srr+"_megahit"
    mgh.run(flanks)

  def contigs2blastdb(dbname, contigs, minlen=500):
    print("Creating BLAST DB of flanking sequences", file=sys.stderr)
    f = Flanker(minlen)
    f.read(fil=contigs)
    tmpdb = 'tmp.fa'
    bdb = lib.blastdb.makeblastdb.Makeblastdb(tmpdb, 'nucl')
    f.write_fasta(tmpdb)
    bdb.make_db(f.write_fasta(tmpdb))

  def bud(self, srr, contigs):
    while True:
      contigs2blastdb(db, contigs, minlen)
      alignments = magicblast(db, srr)
      megahit(alignments, srr)
      iteration += 1
      if iteration == 1: # only for initial testing  purposes.
        break

def main():
  contigs = 'contigs.noextend.fa'
  minlen = 500
  srr = 'SRR5150787'
  iteration = 0
  db = 'ends'


  return 0

if __name__ == '__main__':
  main()
