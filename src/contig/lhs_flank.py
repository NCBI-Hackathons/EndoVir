#!/usr/bin/env python3
#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------


import io
import os
import sys


from . import contig_flank

class LhsContigFlank(contig_flank.ContigFlank):

  def __init__(self, ctg_sequence, start=0, flank_len=500):
    super().__init__('lhs', ctg_sequence, start, flank_len)
    self.sequence = self.setup_flank(start, flank_len, ctg_sequence)

  def setup_flank(self, start, flank_len, ctg_sequence):
    self.start = start
    return ctg_sequence.get_subseq(name=self.name, start=self.start, length=flank_len)

  def get_end_pos(self):
    return self.start + self.flank_len

  def get_start_pos(self):
    return self.start
