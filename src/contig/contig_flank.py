#-------------------------------------------------------------------------------
# \author Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
# \copyright 2017,2018 The University of Sydney
# \description
#-------------------------------------------------------------------------------

import os
import sys

from utils import sequence

class ContigFlank:

  def __init__(self, name_prefix, ctg_sequence, start=0, flank_len=500):
    self.start = start
    self.name = name_prefix + ctg_sequence.name
    self.flank_len = flank_len
    self.sequence = self.setup_flank(start, flank_len, ctg_sequence)

  def get_length(self):
    return self.sequence.length

  def setup_flank(self, start, flank_len, ctg_sequence):
    raise NotImplementedError("Help, I'm virtual! Need my own implementation")

  def get_end_pos(self):
    raise NotImplementedError("Help, I'm virtual! Need my own implementation")

  def get_start_pos(self):
    raise NotImplementedError("Help, I'm virtual! Need my own implementation")
