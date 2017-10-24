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

  #def add_sequence(self, seq, stream=False):
    #if seq.length <= self.len_flank:
      #self.sequences[seq.header] = seq.subseq(0, seq.length, seq.name+"_lhs")
      #if stream == True:
        #return seq.get_sequence()
      #return self.Flank(seq.name)
    #else:
      #subseql = seq.subseq(0, self.len_flank, seq.name+"_lhs")
      #self.sequences[subseql.header] = subseql
      #subseqr = seq.subseq(seq.length-self.len_flank, self.len_flank, seq.name+"_rhs")
      #self.sequences[subseqr.header] = subseqr
      #if stream == True:
        #return subseql.get_sequence() + subseqr.get_sequence()
