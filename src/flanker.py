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
import lib.blast.blastdb.makeblastdb

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
