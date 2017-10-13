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
import lib.blastdb
import lib.fasta
import lib.magicblast
import lib.vdbdump

class Flanker(lib.fasta.Fasta):

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

def magicblast(db=None, sra=None):
  mgb = lib.magicblast.Magicblast()
  return mgb.run('ebola', sra)

def megahit(alignments, sra):
  vdbd = lib.vdbdump.VdbDump()
  vdbd.run(sra, alignments)

def contigs2blastdb(dbname, contigs, minlen=500):
  f = Flanker()
  f.read(fil=contigs)
  bdb = lib.blastdb.BlastDatabase(path=dbname)
  bdb.make_db(f.write_fasta('tmp.fa'))


def main():
  contigs = 'contigs.noextend.fa'
  minlen = 500
  sra = 'SRR5150787'
  iteration = 0
  db = 'ends'

  while True:
    contigs2blastdb(db, contigs, minlen)
    alignments = magicblast(db, sra)
    megahit(alignments, sra)
    iteration += 1
    if iteration == 1: # only for initial testing  purposes.
      break
  return 0

if __name__ == '__main__':
  main()
