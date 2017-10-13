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
import lib.blastdb.blastdb
import lib.fasta.parser
import lib.magicblast.magicblast
import lib.vdbdump.vdbdump
import lib.megahit.megahit


class Flanker(lib.fasta.parser.FastaParser):

  def __init__(self):
    super().__init__()
    self.len_flank = 500
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

def magicblast(db=None, srr=None):
  mgb = lib.magicblast.magicblast.Magicblast()
  return mgb.run('ebola', srr)

def megahit(alignments, srr):
  print("Fetching flanking sequences", file=sys.stderr)
  flanks = 'flanks.fq'
  vdbd = lib.vdbdump.vdbdump.VdbDump()
  fh_flanks = open(flanks, 'w')
  seqs = vdbd.run(srr, alignments, fh_flanks)
  fh_flanks.close()
  print("Running meggahit with flanking sequences", file=sys.stderr)
  mgh = lib.megahit.megahit.Megahit()
  mgh.out_prefix = srr
  mgh.out_dir = srr+"_megahit"
  mgh.run(flanks)

def contigs2blastdb(dbname, contigs, minlen=500):
  print("Creating BLAST DB of flanking sequences", file=sys.stderr)
  f = Flanker()
  f.read(fil=contigs)
  bdb = lib.blastdb.blastdb.BlastDatabase(path=dbname)
  bdb.make_db(f.write_fasta('tmp.fa'))


def main():
  contigs = 'contigs.noextend.fa'
  minlen = 500
  srr = 'SRR5150787'
  iteration = 0
  db = 'ends'

  while True:
    contigs2blastdb(db, contigs, minlen)
    alignments = magicblast(db, srr)
    megahit(alignments, srr)
    iteration += 1
    if iteration == 1: # only for initial testing  purposes.
      break
  return 0

if __name__ == '__main__':
  main()
