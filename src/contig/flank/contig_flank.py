#-------------------------------------------------------------------------------
# \author Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
# \copyright 2017,2018 The University of Sydney
# \description
#-------------------------------------------------------------------------------

import os
import sys


class ContigFlank:

  def __init__(self, sequence, start=0, end=0):
    self.sequence = sequence
    self.start = start
    self.end = end
