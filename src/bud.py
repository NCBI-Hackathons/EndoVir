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

class Flanker(lib.fasta.Fasta):

  def __init__(self):
    super().__init__()
    self.len_flank = 500

  def add_sequence(self, seq):
    if seq.length <= self.len_flank:
      seq.header += "_lhs"
      self.sequences.append(seq)
    else:
      self.sequences.append(seq.subseq(0, self.len_flank, seq.header+"_lhs"))
      self.sequences.append(seq.subseq(seq.length-self.len_flank, self.len_flank, seq.header+"_rhs"))

def contigs2blastdb(dbname, contigs, minlen=500):
  f = Flanker()
  f.read(fil=contigs)
  f.stream_fasta()
  bdb = lib.blastdb.BlastDatabase(db=dbname)
  bdb.make_db(contigs)

def main():
  contigs = 'contigs.noextend.fa'
  minlen = 500
  contigs2blastdb('ends', contigs, minlen)
  return 0

if __name__ == '__main__':
  main()
