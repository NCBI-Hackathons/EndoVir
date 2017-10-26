#  contig.py
#
#  Author: Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0.0

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import lib.sequence.sequence
import flanker

class VirusContig(lib.sequence.sequence.Sequence):

  class Assembly:

    def __init__(self):
      self.N50 = 0

  class Source:

    def __init__(self, srr, contig):
      self.srr = srr
      self.contig = contig

  def __init__(self, name, seq, src_srr, src_contig, flank_len):
    super().__init__(name, seq)
    self.src = self.Source(src_srr, src_contig)
    self.assembly = self.Assembly()
    self.flanker = flanker.Flanker(flank_len)
    self.iteration = 0

  def extend(self, reads):
    print(self.src.srr, self.src.contig, len(reads))
    #assmeble self.seq +  reads
    #update self.length, self.assembly, sefl.flanks

  def extract_flanks(self, stdout):
    self.flanker.extract_flanks(self)
    if len(self.flanker.rhs.sequence) > 0:
      stdout.write(self.flanker.rhs.get_sequence())
    stdout.write(self.flanker.lhs.get_sequence())
