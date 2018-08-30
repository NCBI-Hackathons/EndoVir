#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import io
import os
import sys

from . import flank

class VirusContig:

  def __init__(self, name, srr, flank_len, sequence):
    self.name = name
    self.srr = srr
    self.flank_len = flank_len
    self.sequence = sequence
    self.lhs_flank = flank.Flank(self.sequence, 0, self.flank_len)
    self.rhs_flank = flank.Flank(self.sequence, self.sequence.end, -self.flank_len)
