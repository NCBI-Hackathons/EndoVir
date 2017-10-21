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

  class Flanks:

    def __init__(self):
      self.lhs = lib.sequence.sequence.Sequence()
      self.rhs = lib.sequence.sequence.Sequence()

  class Source:

    def __init__(self, srr, contig):
      self.srr = srr
      self.contig = contig

  def __init__(self, name, seq, src_srr, src_contig):
    super().__init__(name, seq)
    print(name, seq, src_srr, src_contig)
    #self.src = Source(src_srr, src_contig)
    self.assembly = self.Assembly()
    self.flanks = self.Flanks()
    self.iteration = 0

  def extend(self, reads):
    #assmeble self.seq +  reads
    #update self.length, self.assembly, sefl.flanks
    pass
