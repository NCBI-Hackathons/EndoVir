#  flanker.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.fasta.parser
import lib.fasta.sequence

class Flanker(lib.fasta.parser.FastaParser):

  def __init__(self, flank_len=500):
    super().__init__()
    self.len_flank = flank_len
    self.lhs = lib.fasta.sequence.FastaSequence()
    self.rhs = lib.fasta.sequence.FastaSequence()

  def extract_flanks(self, seq):
    if seq.length <= self.len_flank:
      self.lhs = lib.fasta.sequence.FastaSequence(seq.name+"_lhs", seq.subseq(0, seq.length))
    else:
      self.lhs = lib.fasta.sequence.FastaSequence(seq.name+"_lhs", seq.subseq(0, self.len_flank))
      self.rhs = lib.fasta.sequence.FastaSequence(seq.name+"_rhs", seq.subseq(seq.length-self.len_flank, self.len_flank, seq.name+"_rhs"))
