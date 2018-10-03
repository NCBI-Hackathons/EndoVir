#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import io
import os
import sys

from . import rhs_flank
from . import lhs_flank

class VirusContig:

  def __init__(self, sequence, screen):
    self.name = sequence.name
    self.srr = screen.srr
    self.flank_len = screen.flank_len
    self.location = os.path.join(screen.ctg_dir, self.name)
    self.lhs_flank = lhs_flank.LhsContigFlank(sequence, 0, screen.flank_len)
    self.rhs_flank = rhs_flank.RhsContigFlank(sequence, sequence.length, self.flank_len)
    self.write_sequence(sequence.sequence)
    self.length = sequence.length

  def write_sequence(self, sequence):
    fh = open(self.location+'.sequence', 'w')
    fh.write(sequence)
    fh.close()
