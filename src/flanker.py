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

  class Flank(lib.fasta.sequence.FastaSequence):

    def __init__(self, name, seq, location, contig):
      super().__init__(name, seq)
      self.location = location
      self.contig = contig

  def __init__(self, flank_len):
    super().__init__()
    self.len_flank = flank_len
    self.lhs = lib.fasta.sequence.FastaSequence()
    self.rhs = lib.fasta.sequence.FastaSequence()

  def extract_flanks(self, seq):
    if seq.length <= self.len_flank:
      self.lhs = lib.fasta.sequence.FastaSequence(seq.name+":lhs", seq.subseq(0, seq.length))
    else:
      self.lhs = lib.fasta.sequence.FastaSequence(seq.name+":lhs", seq.subseq(0, self.len_flank))
      self.rhs = lib.fasta.sequence.FastaSequence(seq.name+":rhs", seq.subseq(seq.length-self.len_flank, self.len_flank, seq.name+"_rhs"))
